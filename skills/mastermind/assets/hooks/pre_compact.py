"""PreCompact hook: snapshot what the chat was doing, so restore_context.py can hand it back.

The model can't be asked to save state before compaction, so this records the facts
mechanically: recent commits, uncommitted files, and files changed after SESSION_STATE.md.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    event = json.load(sys.stdin)
except Exception:
    event = {}

root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".")
memory = root / "memory"
if not memory.is_dir():
    sys.exit(0)


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                              encoding="utf-8", timeout=10).stdout.strip()
    except Exception:
        return ""


lines = []
log = git("log", "--oneline", "-5")
if log:
    lines += ["Последние коммиты:", log, ""]
status = git("status", "--short")
if status:
    lines += ["Незакоммиченные файлы:", "\n".join(status.splitlines()[:30]), ""]

state = memory / "SESSION_STATE.md"
if state.is_file():
    since = state.stat().st_mtime
    newer = sorted(
        p.relative_to(root).as_posix() for p in memory.rglob("*.md")
        if p != state and p.stat().st_mtime > since
    )
    if newer:
        lines += ["SESSION_STATE.md старше этих файлов памяти — сверь и обнови его первым делом:",
                  "\n".join(newer[:20]), ""]

snapshot_dir = root / ".claude" / "compact"
snapshot_dir.mkdir(parents=True, exist_ok=True)
(snapshot_dir / f"{event.get('session_id', 'unknown')}.md").write_text("\n".join(lines), encoding="utf-8")
