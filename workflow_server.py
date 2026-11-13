#!/usr/bin/env python3
"""Serve the GhostAgent workspace and its local, manager-backed workflow API."""
from __future__ import annotations

import argparse
import hmac
import json
import secrets
import re
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

import ghostagent as manager
from kiro_generation import KiroJobs

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"
SAMPLE = ROOT / "examples" / "sample-run"
MAX_BODY = 2 * 1024 * 1024


class LocalWorkflow:
    def __init__(self, output: Path):
        self.output = output.resolve()
        self.lock = threading.RLock()

    def locate(self, identifier):
        if identifier == "sample":
            return SAMPLE
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            raise manager.WorkflowError("无效的研究标识，请使用小写字母、数字和连字符。")
        root = self.output / identifier
        if root.is_symlink() or not root.resolve().is_relative_to(self.output):
            raise manager.WorkflowError("研究目录超出允许范围。")
        return root

    def list_projects(self):
        result = [{"id": "sample", "title": "内置完整样例", "read_only": True}]
        if self.output.exists():
            for path in sorted(self.output.iterdir()):
                if path.is_dir() and not path.is_symlink() and (path / manager.STATE).is_file():
                    result.append({"id": path.name, "title": path.name, "read_only": False})
        return result

    def checked_state(self, root):
        state = manager.load(root)
        if manager.file_hash(root, "session-log.md") != manager.digest(manager.log_text(state).encode("utf-8")):
            raise manager.WorkflowError("会话日志与管理器事件不一致，请先核对外部编辑；没有覆盖文件。")
        return state

    def snapshot(self, identifier, root, state):
        report = manager.status_report(root, state)
        validation = manager.validate(root, state)
        documents = {}
        for name in sorted(manager.MANAGED):
            path = manager.checked_path(root, name)
            if path.is_file():
                documents[name] = path.read_text(encoding="utf-8-sig")
        title = documents.get("topic-brief.md", "").splitlines()
        title = title[0].removeprefix("# ") if title else state["topic"]
        return {"workspace_id": identifier, "live": True, "read_only": identifier == "sample",
                "title": title, "sample": identifier == "sample", "verified": validation["ok"],
                "report": report, "events": state["events"], "documents": documents,
                "validation": validation}

    def read(self, identifier):
        root = self.locate(identifier)
        if not root.is_dir():
            raise manager.WorkflowError("研究不存在，请先新建研究。")
        with self.lock, manager.topic_lock(root):
            return self.snapshot(identifier, root, self.checked_state(root))

    def create(self, slug, idea, from_sample=False):
        if slug == "sample":
            raise manager.WorkflowError("sample 是保留标识，请另取研究名称。")
        root = self.locate(slug)
        if not isinstance(idea, str) or not idea.strip():
            raise manager.WorkflowError("请输入研究想法。")
        with self.lock:
            root.parent.mkdir(parents=True, exist_ok=True)
            try:
                root.mkdir(exist_ok=False)
            except FileExistsError as exc:
                raise manager.WorkflowError("这个研究目录已经存在，请打开它或换一个名称。") from exc
            with manager.topic_lock(root):
                manager.initialize(root, idea)
                state = self.checked_state(root)
                if from_sample:
                    # Only seed a topic candidate; sample approval is never inherited.
                    with manager.topic_lock(SAMPLE):
                        self.checked_state(SAMPLE)
                        brief = (SAMPLE / "topic-brief.md").read_text(encoding="utf-8-sig")
                    with tempfile.TemporaryDirectory(prefix="ghostagent-candidate-") as temp:
                        source = Path(temp)
                        (source / "topic-brief.md").write_text(brief, encoding="utf-8", newline="\n")
                        manager.commit(root, state, "topic", source, manager.fingerprint(root, state, "topic"),
                                       "Copied illustrative topic for a new workspace; no scope approval inherited.")
                return self.snapshot(slug, root, state)

    def operate(self, operation, data):
        if operation == "init":
            return self.create(data.get("slug"), data.get("idea"))
        if operation == "copy-sample":
            idea = (SAMPLE / "input.md").read_text(encoding="utf-8-sig")
            return self.create(data.get("slug"), idea, from_sample=True)
        identifier = data.get("id")
        root = self.locate(identifier)
        if operation != "validate" and identifier == "sample":
            raise manager.WorkflowError("内置样例只读，请先复制为独立研究。")
        if not root.is_dir():
            raise manager.WorkflowError("研究不存在。")
        with self.lock, manager.topic_lock(root):
            state = self.checked_state(root)
            if operation == "confirm":
                if data.get("reviewed") is not True:
                    raise manager.WorkflowError("请先阅读当前正式选题并明确勾选确认。")
                manager.confirm(root, state, data.get("hash"))
            elif operation == "commit":
                stage = data.get("stage")
                if stage not in manager.STAGES:
                    raise manager.WorkflowError("无效的阶段。")
                docs = data.get("documents")
                if not isinstance(docs, dict) or set(docs) != set(manager.STAGES[stage]) or any(not isinstance(t, str) for t in docs.values()):
                    raise manager.WorkflowError("必须提交该阶段的完整文档集合。")
                reason = data.get("reason")
                if not isinstance(reason, str) or not reason.strip():
                    raise manager.WorkflowError("请填写本次变更原因。")
                with tempfile.TemporaryDirectory(prefix="ghostagent-candidate-") as temp:
                    source = Path(temp)
                    for name, text in docs.items():
                        path = source / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(text, encoding="utf-8", newline="\n")
                    manager.commit(root, state, stage, source, data.get("based_on"), reason.strip())
            elif operation != "validate":
                raise manager.WorkflowError("未知操作。")
            return self.snapshot(identifier, root, state)


class WorkflowServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, workflow, kiro_executable=None, kiro_wsl=None, generation_timeout=600):
        super().__init__(address, Handler)
        self.workflow = workflow
        self.generation = KiroJobs(workflow, kiro_executable, kiro_wsl, generation_timeout)
        self.token = secrets.token_urlsafe(32)
        self.allowed_hosts = {f"127.0.0.1:{self.server_port}", f"localhost:{self.server_port}"}


class Handler(BaseHTTPRequestHandler):
    server_version = "GhostAgent/1"

    def log_message(self, *_args):
        pass

    def send_bytes(self, status, data, mime):
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "frame-ancestors 'self'")
        self.end_headers()
        self.wfile.write(data)

    def respond(self, status, value):
        self.send_bytes(status, json.dumps(value, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def allowed(self):
        if self.headers.get("Host") not in self.server.allowed_hosts:
            self.respond(403, {"error": "仅允许本机工作台访问。"})
            return False
        origin = self.headers.get("Origin")
        if origin and origin != "http://" + self.headers.get("Host", ""):
            self.respond(403, {"error": "拒绝跨站请求。"})
            return False
        if self.headers.get("Sec-Fetch-Site") == "cross-site":
            self.respond(403, {"error": "拒绝跨站请求。"})
            return False
        return True

    def do_GET(self):
        if not self.allowed():
            return
        request = urlsplit(self.path)
        try:
            if request.path == "/api/session":
                self.respond(200, {"token": self.server.token, "projects": self.server.workflow.list_projects()})
            elif request.path == "/api/projects":
                self.respond(200, {"projects": self.server.workflow.list_projects()})
            elif request.path == "/api/snapshot":
                identifier = parse_qs(request.query).get("id", ["sample"])[0]
                self.respond(200, {"project": self.server.workflow.read(identifier)})
            elif request.path == "/api/kiro/runtime":
                refresh = parse_qs(request.query).get("refresh", [""])[0] == "1"
                self.respond(200, {"runtime": self.server.generation.info(refresh)})
            elif request.path == "/api/kiro/jobs":
                identifier = parse_qs(request.query).get("id", ["sample"])[0]
                self.respond(200, {"jobs": self.server.generation.list(identifier)})
            elif request.path == "/api/kiro/job":
                identifier = parse_qs(request.query).get("job", [""])[0]
                self.respond(200, {"job": self.server.generation.get(identifier)})
            elif request.path.startswith("/api/"):
                self.respond(404, {"error": "接口不存在。"})
            else:
                relative = unquote(request.path).lstrip("/") or "index.html"
                path = FRONTEND / relative
                if not path.resolve().is_relative_to(FRONTEND.resolve()) or not path.is_file() or path.suffix not in {".html", ".css", ".js", ".svg"}:
                    self.respond(404, {"error": "页面不存在。"})
                    return
                mime = {".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".svg": "image/svg+xml"}[path.suffix]
                self.send_bytes(200, path.read_bytes(), mime + "; charset=utf-8")
        except (manager.WorkflowError, OSError, ValueError, KeyError, TypeError) as exc:
            self.respond(409, {"error": str(exc)})

    def do_POST(self):
        if not self.allowed():
            return
        if not hmac.compare_digest(self.headers.get("X-GhostAgent-Token", ""), self.server.token):
            self.respond(403, {"error": "连接凭据已失效，请重新打开工作台。"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= MAX_BODY:
                self.respond(413, {"error": "请求为空或超过 2 MB。"})
                return
            if self.headers.get_content_type() != "application/json":
                self.respond(415, {"error": "需要 JSON 请求。"})
                return
            self.connection.settimeout(20)
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError("请求必须为对象。")
            operation = urlsplit(self.path).path.removeprefix("/api/")
            if operation == "kiro/generate":
                self.respond(202, {"job": self.server.generation.start(data)})
                return
            if operation == "kiro/cancel":
                self.respond(200, {"job": self.server.generation.cancel(data.get("job"))})
                return
            if operation not in {"init", "copy-sample", "confirm", "commit", "validate"}:
                self.respond(404, {"error": "接口不存在。"})
                return
            self.respond(200, {"project": self.server.workflow.operate(operation, data)})
        except (manager.WorkflowError, OSError, ValueError, KeyError, TypeError) as exc:
            self.respond(409, {"error": str(exc)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--kiro-executable", default=None, help="Native CLI executable, or Linux executable path with --kiro-wsl")
    parser.add_argument("--kiro-wsl", default=None, help="Explicit WSL distribution containing Kiro CLI")
    parser.add_argument("--generation-timeout", type=int, default=600, help="Generation timeout in seconds (10–1800)")
    args = parser.parse_args()
    server = WorkflowServer(("127.0.0.1", args.port), LocalWorkflow(ROOT / "output"),
                            args.kiro_executable, args.kiro_wsl, args.generation_timeout)
    print(f"GhostAgent workspace: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.generation.close()
        server.server_close()


if __name__ == "__main__":
    main()
