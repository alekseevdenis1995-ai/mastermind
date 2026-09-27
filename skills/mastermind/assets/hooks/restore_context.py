"""SessionStart hook (clear/compact): re-inject the chat's role so nobody pastes prompts by hand.

Specialist chats are listed in memory/sessions.json by MASTER; any other chat in the
project folder is treated as MASTER and gets memory/MASTER_START.md.
"""
import json
import os
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

try:
    sessions = json.loads((memory / "sessions.json").read_text(encoding="utf-8"))
except Exception:
    sessions = {}
roles = sessions.get("roles", {}) or {}
session_id = event.get("session_id", "")

start_file = roles.get(session_id)
if isinstance(start_file, str) and start_file.endswith(".md"):
    role = Path(start_file).stem.replace("_START", "")
    print(
        f"Контекст этого чата был очищен или сжат. Ты — {role} в AI-команде проекта.\n"
        f"Перечитай {start_file} (твоя роль) и свои отчёты в memory/reports/.\n"
        "Если задача была в работе — доведи её и отправь отчёт MASTER. Иначе — READY / WAITING FOR TASK."
    )
elif roles and not str(sessions.get("mode", "A")).startswith("A") and sessions.get("master") != session_id:
    print(
        "Контекст этого чата был очищен или сжат. Этот чат не найден в memory/sessions.json.\n"
        "Если ты специалист (NN <ROLE>) — перечитай свой team/NN_<ROLE>_START.md и свои отчёты в memory/reports/.\n"
        "Если ты MASTER — прочитай memory/MASTER_START.md."
    )
else:
    master_start = memory / "MASTER_START.md"
    if master_start.is_file():
        print("Контекст этого чата был очищен или сжат.\n")
        print(master_start.read_text(encoding="utf-8"))

snapshot = root / ".claude" / "compact" / f"{event.get('session_id', 'unknown')}.md"
if snapshot.is_file():
    text = snapshot.read_text(encoding="utf-8").strip()
    if text:
        print("\nСнимок перед сжатием:\n" + text)
    snapshot.unlink()
