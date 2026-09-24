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
    roles = json.loads((memory / "sessions.json").read_text(encoding="utf-8")).get("roles", {})
except Exception:
    roles = {}

start_file = roles.get(event.get("session_id", ""))
if start_file:
    role = Path(start_file).stem.replace("_START", "")
    print(
        f"Контекст этого чата был очищен или сжат. Ты — {role} в AI-команде проекта.\n"
        f"Перечитай {start_file} (твоя роль) и свои отчёты в memory/reports/.\n"
        "Если задача была в работе — доведи её и отправь отчёт MASTER. Иначе — READY / WAITING FOR TASK."
    )
else:
    master_start = memory / "MASTER_START.md"
    if master_start.is_file():
        print("Контекст этого чата был очищен или сжат.\n")
        print(master_start.read_text(encoding="utf-8"))
