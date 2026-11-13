#!/usr/bin/env python3
"""Refresh the frontend's embedded, validated sample snapshot using the local manager."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "examples" / "sample-run"
DEST = Path(__file__).resolve().parent / "sample-data.js"


def manager(command: str):
    run = subprocess.run(
        [sys.executable, "-B", str(ROOT / "ghostagent.py"), "--topic", str(SAMPLE), "--json", command],
        capture_output=True, text=True, encoding="utf-8", timeout=30, cwd=ROOT,
    )
    if run.returncode:
        raise RuntimeError(run.stdout or run.stderr or "Manager rejected sample")
    return json.loads(run.stdout)


def main():
    validation = manager("validate")
    report = validation["workflow"]
    state = json.loads((SAMPLE / ".ghostagent-state.json").read_text(encoding="utf-8-sig"))
    names = ["input.md", "topic-brief.md", "research-spec/requirements.md", "research-spec/design.md",
             "research-spec/tasks.md", "literature-review-framework.md", "diagrams.md", "session-log.md"]
    snapshot = {
        "title": "AI Tools & Students’ Learning Habits",
        "sample": True,
        "verified": True,
        "report": report,
        "events": state["events"],
        "documents": {p: (SAMPLE / p).read_text(encoding="utf-8-sig") for p in names},
        "validation": {"ok": validation["ok"], "warnings": validation["warnings"]},
    }
    DEST.write_text("window.GHOST_SAMPLE = " + json.dumps(snapshot, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(f"Updated {DEST.name}: {len(names)} files, {len(state['events'])} events, {len(report['stages'])} stages")


if __name__ == "__main__":
    main()
