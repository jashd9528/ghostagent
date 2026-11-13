#!/usr/bin/env python3
"""GhostAgent's dependency-free, local workflow state manager (Python 3.10+)."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from datetime import datetime

STAGES = {
    "topic": ("topic-brief.md",),
    "spec": ("research-spec/requirements.md", "research-spec/design.md", "research-spec/tasks.md"),
    "literature": ("literature-review-framework.md",),
    "diagrams": ("diagrams.md",),
}
DEPS = {"topic": (), "spec": ("topic",), "literature": ("topic", "spec"), "diagrams": ("topic", "spec")}
HEADINGS = {
    "topic-brief.md": ("Refined topic statement", "Scope", "Research questions", "Key terms"),
    "research-spec/requirements.md": ("Requirements",),
    "research-spec/design.md": ("Chapter plan", "Method outline", "Procedure"),
    "research-spec/tasks.md": ("Tasks",),
    "literature-review-framework.md": ("Reading plan",),
    "diagrams.md": ("Study architecture", "Research procedure"),
}
STATE = ".ghostagent-state.json"
JOURNAL = ".ghostagent-pending.json"
MANAGED = {"input.md", "session-log.md", *(p for paths in STAGES.values() for p in paths)}


class WorkflowError(Exception):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def stamp() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def checked_path(root: Path, relative: str) -> Path:
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise WorkflowError(f"Path escapes topic folder: {relative}")
    if path.is_symlink():
        raise WorkflowError(f"Symlink is not a workflow document: {relative}")
    return path


def file_hash(root: Path, relative: str):
    path = checked_path(root, relative)
    return digest(path.read_bytes()) if path.is_file() else None


def atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".ghostagent-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextlib.contextmanager
def topic_lock(root: Path):
    """OS-released process lock; the small lock file persists intentionally."""
    root.mkdir(parents=True, exist_ok=True)
    lock_path = checked_path(root, ".ghostagent.lock")
    with lock_path.open("a+b") as handle:
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise WorkflowError("Another GhostAgent command is using this topic.") from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def log_text(state) -> str:
    lines = ["# Session Log", "", "Managed workflow events. Research content and student review remain separate.", ""]
    for event in state["events"]:
        lines.extend([f"## {event['revision']} — {event['time']} — {event['action']}", "",
                      event["detail"], ""])
    return "\n".join(lines)


def recover(root: Path):
    journal = checked_path(root, JOURNAL)
    if not journal.exists():
        return
    pending = json.loads(journal.read_text(encoding="utf-8"))
    current = file_hash(root, STATE)
    after_state = canonical(pending["state"])
    if current not in (pending["before_state"], digest(after_state)):
        raise WorkflowError("Interrupted transaction conflicts with state edits; preserve the folder and resolve manually.")
    for relative, item in pending["writes"].items():
        if relative not in MANAGED:
            raise WorkflowError("Invalid transaction document name.")
        actual = file_hash(root, relative)
        after = digest(item["text"].encode("utf-8"))
        if actual not in (item["before"], after):
            raise WorkflowError(f"Interrupted transaction conflicts with edits to {relative}; no files were overwritten.")
    # Validate every precondition before rolling forward any file.
    for relative, item in pending["writes"].items():
        atomic_write(checked_path(root, relative), item["text"].encode("utf-8"))
    atomic_write(checked_path(root, STATE), after_state)
    journal.unlink()


def save(root: Path, state, texts: dict[str, str], action: str, detail: str):
    old_hash = file_hash(root, STATE)
    state["revision"] += 1
    state["events"].append({"revision": state["revision"], "time": stamp(), "action": action, "detail": detail})
    texts = dict(texts)
    texts["session-log.md"] = log_text(state)
    pending = {"before_state": old_hash, "state": state, "writes": {
        p: {"before": file_hash(root, p), "text": text} for p, text in texts.items()
    }}
    atomic_write(checked_path(root, JOURNAL), canonical(pending))
    recover(root)


def load(root: Path):
    recover(root)
    path = checked_path(root, STATE)
    if not path.exists():
        raise WorkflowError("Topic is not initialized. Run init first.")
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("schema") != 1:
        raise WorkflowError("Unsupported workflow state schema.")
    return state


def blocks(text: str):
    """Protected blocks are identified by explicit id, or their enclosing heading."""
    marker = re.compile(r"<!--\s*(/?)student-edit(?::([a-z0-9-]+))?\s*-->")
    found, active = {}, None
    for match in marker.finditer(text):
        closing, identifier = match.groups()
        if not closing:
            if active is not None:
                raise WorkflowError("Nested student-edit blocks are not supported.")
            headings = re.findall(r"^#{1,6}\s+(.+)$", text[:match.start()], re.M)
            key = "id:" + identifier if identifier else "heading:" + (headings[-1] if headings else "document")
            if key in found:
                raise WorkflowError(f"Ambiguous student-edit block {key}; use unique named markers.")
            active = (key, match.end())
        else:
            if active is None or identifier is not None:
                raise WorkflowError("Unmatched student-edit closing marker.")
            key, start = active
            found[key] = (start, match.start(), text[start:match.start()])
            active = None
    if active is not None:
        raise WorkflowError("Unclosed student-edit block.")
    # Fail on malformed marker-like comments instead of silently losing edits.
    if len(re.findall(r"<!--\s*/?student-edit\b", text)) != len(list(marker.finditer(text))):
        raise WorkflowError("Malformed student-edit marker.")
    return found


def preserve(old: str, candidate: str) -> str:
    original, replacements = blocks(old), blocks(candidate)
    if not original.keys() <= replacements.keys():
        raise WorkflowError("Candidate removed or renamed protected sections: " + ", ".join(original.keys() - replacements.keys()))
    for key, (start, end, _) in sorted(replacements.items(), key=lambda item: item[1][0], reverse=True):
        if key in original:
            candidate = candidate[:start] + original[key][2] + candidate[end:]
    return candidate


def question_ids(text: str) -> set[str]:
    return set(re.findall(r"\bRQ[1-9][0-9]*\b", text))


def mermaid_issues(text: str, minimum: int) -> list[str]:
    issues = []
    diagrams = re.findall(r"^```mermaid[^\S\n]*\n(.*?)^```[^\S\n]*$", text, re.M | re.S)
    if len(diagrams) < minimum:
        issues.append(f"Expected at least {minimum} fenced Mermaid diagram(s).")
    for diagram in diagrams:
        first = next((s.strip() for s in diagram.splitlines() if s.strip()), "")
        if not re.fullmatch(r"(?:flowchart|graph)\s+(?:TD|TB|BT|RL|LR)", first):
            issues.append("Mermaid must start with a flowchart/graph direction header.")
    return issues


def structural(stage: str, texts: dict[str, str], brief: str) -> list[str]:
    errors = []
    ids = question_ids(brief)
    for relative, text in texts.items():
        if not text.strip() or not text.startswith("# ") or len(re.findall(r"^# ", text, re.M)) != 1:
            errors.append(f"{relative}: expected one top-level title and nonempty Markdown.")
        for heading in HEADINGS[relative]:
            if not re.search(r"^##\s+" + re.escape(heading) + r"\s*$", text, re.M | re.I):
                errors.append(f"{relative}: missing section '{heading}'.")
        if len(re.findall(r"^```", text, re.M)) % 2:
            errors.append(f"{relative}: unclosed fenced code block.")
        blocks(text)
        mentioned = question_ids(text)
        if ids and mentioned - ids:
            errors.append(f"{relative}: unknown research questions {sorted(mentioned - ids)}.")
    if stage == "topic":
        topic = texts["topic-brief.md"]
        if not 3 <= len(ids) <= 5 or ids != {f"RQ{i}" for i in range(1, len(ids) + 1)}:
            errors.append("Topic requires 3–5 consecutively numbered research questions.")
        if not re.search(r"\bin scope\b", topic, re.I) or not re.search(r"\bout of scope\b", topic, re.I):
            errors.append("Topic must include in-scope and out-of-scope lists.")
    if stage == "spec":
        req = texts["research-spec/requirements.md"]
        if not ids <= question_ids(req):
            errors.append("Research requirements must reference every RQ.")
        if not re.search(r"\bSHALL\b", req):
            errors.append("Research requirements need EARS-style SHALL criteria.")
        errors.extend(mermaid_issues(texts["research-spec/design.md"], 1))
        tasks = texts["research-spec/tasks.md"]
        tasks_seen = set()
        for line in tasks.splitlines():
            match = re.match(r"- \[[ xX]\] (T\d+)\b", line)
            if not match:
                continue
            task = match[1]
            dependencies = re.findall(r"\bT\d+\b", line[match.end():])
            if task in tasks_seen or any(d not in tasks_seen for d in dependencies):
                errors.append(f"Task {task} is duplicate or depends on a missing/later task.")
            if line.startswith(("- [x]", "- [X]")):
                for dependency in dependencies:
                    if not re.search(r"^- \[[xX]\] " + dependency + r"\b", tasks, re.M):
                        errors.append(f"Completed task {task} has unfinished dependency {dependency}.")
            tasks_seen.add(task)
        if not tasks_seen:
            errors.append("Tasks need ordered checkboxes named T1, T2, ... with 'Depends on: Tn' where relevant.")
    if stage == "literature":
        framework = texts["literature-review-framework.md"]
        if not ids <= question_ids(framework):
            errors.append("Literature framework must cover every RQ.")
        themes = re.split(r"^## Theme[^\n]*\n", framework, flags=re.M)[1:]
        if not themes:
            errors.append("Literature framework needs '## Theme ...' sections.")
        for index, theme in enumerate(themes, 1):
            for label in ("Main debate", "Established", "Gap", "This thesis"):
                if not re.search(r"\*\*" + label + r":?\*\*", theme, re.I):
                    errors.append(f"Theme {index}: missing {label}.")
    if stage == "diagrams":
        diagram = texts["diagrams.md"]
        errors.extend(mermaid_issues(diagram, 2))
        if len(re.findall(r"Caption:", diagram, re.I)) < 2 or "research-spec/design.md" not in diagram:
            errors.append("Each diagram needs a caption pointing to research-spec/design.md.")
    return errors


def inputs(root: Path, stage: str):
    paths = ["input.md"] if stage == "topic" else [p for d in DEPS[stage] for p in STAGES[d]]
    return {p: file_hash(root, p) for p in paths}


def fingerprint(root: Path, state, stage: str):
    return digest(canonical({"topic": state["topic"], "stage": stage, "inputs": inputs(root, stage),
                             "outputs": {p: file_hash(root, p) for p in STAGES[stage]},
                             "confirmation": state["confirmed_brief"] if stage != "topic" else None}))


def stage_states(root: Path, state):
    result = {}
    for stage, paths in STAGES.items():
        saved = state["stages"].get(stage)
        actual = {p: file_hash(root, p) for p in paths}
        if not all(actual.values()):
            status = "missing"
        elif not saved:
            status = "untracked"
        elif actual != saved["outputs"]:
            status = "modified"
        elif inputs(root, stage) != saved["inputs"] or any(result[d] != "ready" for d in DEPS[stage]):
            status = "stale"
        elif stage != "topic" and state["confirmed_brief"] != file_hash(root, "topic-brief.md"):
            status = "stale"
        else:
            status = "ready"
        result[stage] = status
    return result


def status_report(root: Path, state):
    statuses = stage_states(root, state)
    confirmed = statuses["topic"] == "ready" and state["confirmed_brief"] == file_hash(root, "topic-brief.md")
    next_step = "complete"
    for stage, status in statuses.items():
        if stage != "topic" and not confirmed:
            next_step = "confirm" if statuses["topic"] == "ready" else "topic"
            break
        if status != "ready":
            next_step = stage
            break
    return {"topic": state["topic"], "revision": state["revision"], "confirmed": confirmed,
            "brief_hash": file_hash(root, "topic-brief.md"), "next": next_step,
            "stages": {s: {"status": v, "based_on": fingerprint(root, state, s)} for s, v in statuses.items()}}


def initialize(root: Path, idea: str):
    recover(root)
    if checked_path(root, STATE).exists():
        raise WorkflowError("Topic already initialized; use status to resume.")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", root.name):
        raise WorkflowError("Topic folder name must be a kebab-case slug.")
    occupied = [p for p in MANAGED if checked_path(root, p).exists()]
    if occupied:
        raise WorkflowError("Refusing to initialize over existing documents: " + ", ".join(sorted(occupied)))
    if not idea.strip():
        raise WorkflowError("A nonempty research idea is required.")
    state = {"schema": 1, "topic": root.name, "revision": 0, "confirmed_brief": None, "stages": {}, "events": []}
    save(root, state, {"input.md": "# Research Input\n\n" + idea.strip() + "\n"}, "init", "Recorded the student's research idea; no research content generated.")
    return status_report(root, state)


def commit(root: Path, state, stage: str, source: Path, based_on: str, reason: str):
    if based_on != fingerprint(root, state, stage):
        raise WorkflowError("Candidate base is outdated. Read status, reconcile current files, then regenerate/review candidates.")
    statuses = stage_states(root, state)
    for dependency in DEPS[stage]:
        if statuses[dependency] != "ready":
            raise WorkflowError(f"Dependency {dependency} is {statuses[dependency]}; commit it first.")
    if stage != "topic" and state["confirmed_brief"] != file_hash(root, "topic-brief.md"):
        raise WorkflowError("The current topic brief has not been confirmed. Student review is required.")
    texts = {}
    for relative in STAGES[stage]:
        candidate = checked_path(source, relative)
        target = checked_path(root, relative)
        if not candidate.is_file():
            raise WorkflowError(f"Candidate missing: {relative}")
        text = candidate.read_text(encoding="utf-8-sig")
        if target.is_file():
            text = preserve(target.read_text(encoding="utf-8-sig"), text)
        texts[relative] = text
    brief = texts["topic-brief.md"] if stage == "topic" else checked_path(root, "topic-brief.md").read_text(encoding="utf-8-sig")
    errors = structural(stage, texts, brief)
    if errors:
        raise WorkflowError("Candidate validation failed:\n- " + "\n- ".join(errors))
    if stage == "topic" and state["confirmed_brief"] != digest(brief.encode("utf-8")):
        state["confirmed_brief"] = None
    state["stages"][stage] = {"inputs": inputs(root, stage), "outputs": {p: digest(t.encode("utf-8")) for p, t in texts.items()}}
    save(root, state, texts, "commit:" + stage, reason)
    return status_report(root, state)


def confirm(root: Path, state, reviewed_hash: str):
    if stage_states(root, state)["topic"] != "ready":
        raise WorkflowError("Commit a current topic brief before confirmation.")
    current = file_hash(root, "topic-brief.md")
    if reviewed_hash != current:
        raise WorkflowError("Reviewed hash differs from the current brief. Review the latest brief.")
    if state["confirmed_brief"] != current:
        state["confirmed_brief"] = current
        save(root, state, {}, "confirm", "Student confirmation recorded for topic brief SHA256 " + current + ".")
    return status_report(root, state)


def validate(root: Path, state):
    report = status_report(root, state)
    errors, warnings = [], []
    if not report["confirmed"]:
        errors.append("Current topic brief is not confirmed.")
    brief_path = checked_path(root, "topic-brief.md")
    brief = brief_path.read_text(encoding="utf-8-sig") if brief_path.exists() else ""
    for stage, item in report["stages"].items():
        if item["status"] != "ready":
            errors.append(f"Stage {stage} is {item['status']}.")
        if all(checked_path(root, p).is_file() for p in STAGES[stage]):
            texts = {p: checked_path(root, p).read_text(encoding="utf-8-sig") for p in STAGES[stage]}
            errors.extend(structural(stage, texts, brief))
            for relative, text in texts.items():
                if "[source needed]" in text:
                    warnings.append(f"{relative}: unverified source slots remain (expected for a planning framework).")
                if re.search(r"\b10\.\d{4,9}/\S+|\([A-Z][A-Za-z-]+,?\s+(?:19|20)\d{2}\)", text):
                    warnings.append(f"{relative}: citation-like strings require human provenance review.")
    if checked_path(root, "session-log.md").read_text(encoding="utf-8") != log_text(state):
        errors.append("Session log differs from managed event history; resolve the edit before continuing.")
    warnings.append("Mermaid checks are structural only; rendering is not verified by this command.")
    warnings.append("Academic validity, source truth and actual Kiro execution require human/runtime review.")
    return {"ok": not errors, "errors": errors, "warnings": warnings, "workflow": report}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", type=Path, required=True, help="Per-topic folder, e.g. output/my-topic")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Initialize a new topic without overwriting files")
    init.add_argument("--idea", required=True)
    commands.add_parser("status", help="Inspect content hashes and identify the next stage")
    review = commands.add_parser("confirm", help="Record the student's explicit scope approval")
    review.add_argument("--hash", required=True, dest="reviewed_hash")
    submit = commands.add_parser("commit", help="Validate and atomically publish a candidate stage")
    submit.add_argument("stage", choices=STAGES)
    submit.add_argument("--source", type=Path, required=True, help="Candidate folder with the same relative file layout")
    submit.add_argument("--based-on", required=True, help="Stage fingerprint from status before generation")
    submit.add_argument("--reason", required=True, help="Triggering change for the session log")
    commands.add_parser("validate", help="Check complete state, structures and task dependencies")
    args = parser.parse_args(argv)
    root = args.topic.absolute()
    try:
        if args.command != "init" and not root.is_dir():
            raise WorkflowError("Topic folder does not exist. Run init first.")
        if root.is_symlink():
            raise WorkflowError("Topic root must not be a symlink.")
        with topic_lock(root):
            if args.command == "init":
                result = initialize(root, args.idea)
            else:
                state = load(root)
                # Never silently overwrite a student's manually edited event log.
                if file_hash(root, "session-log.md") != digest(log_text(state).encode("utf-8")):
                    raise WorkflowError("Managed session log was edited; reconcile it with state.events before continuing.")
                if args.command == "status":
                    result = status_report(root, state)
                elif args.command == "confirm":
                    result = confirm(root, state, args.reviewed_hash)
                elif args.command == "commit":
                    if not args.reason.strip():
                        raise WorkflowError("A nonempty change reason is required.")
                    result = commit(root, state, args.stage, args.source.absolute(), args.based_on, args.reason)
                else:
                    result = validate(root, state)
        if args.json:
            print(json.dumps(result, ensure_ascii=True, indent=2))
        elif "ok" in result:
            print("PASS" if result["ok"] else "FAIL")
            for error in result["errors"]:
                print("ERROR: " + error)
            for warning in result["warnings"]:
                print("NOTE: " + warning)
        else:
            print(f"Topic: {result['topic']} | revision: {result['revision']} | next: {result['next']}")
            print(f"Confirmed: {result['confirmed']} | brief SHA256: {result['brief_hash']}")
            for stage, item in result["stages"].items():
                print(f"{stage}: {item['status']} | --based-on {item['based_on']}")
        return 0 if result.get("ok", True) else 1
    except (WorkflowError, OSError, ValueError, KeyError, TypeError) as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True))
        else:
            print("ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
