"""Create the boilerplate of a Mastermind package so the model only writes what needs thought.

Usage:
  python scaffold.py <project_dir> --name "<Project>" --mode A|B|C --roles TECH,QA
                     [--harness claude|codex|cursor|opencode|gemini|antigravity|copilot|other]
                     [--models TECH=sonnet,QA=haiku] [--limits 10,2,3]

Never overwrites an existing file. Prints what was created and what the model still has to write.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VERSION = "1.2.0"

ap = argparse.ArgumentParser()
ap.add_argument("project")
ap.add_argument("--name", required=True)
ap.add_argument("--mode", required=True, choices=["A", "B", "C"])
ap.add_argument("--roles", required=True, help="comma-separated, in team order: TECH,QA")
ap.add_argument("--harness", default="claude")
ap.add_argument("--models", default="", help="ROLE=model pairs, used for Claude Code agent files")
ap.add_argument("--limits", default="10,2,3", help="tasks per milestone, rework rounds, parallel tasks")
args = ap.parse_args()

root = Path(args.project).resolve()
skill = Path(__file__).resolve().parent.parent
roles = [r.strip().upper() for r in args.roles.split(",") if r.strip()]
models = dict(p.split("=", 1) for p in args.models.split(",") if "=" in p)
per_milestone, rework, parallel = (args.limits.split(",") + ["10", "2", "3"])[:3]
name = args.name
created, skipped = [], []


def write(rel, text):
    p = root / rel
    if p.exists():
        skipped.append(rel)
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.lstrip("\n"), encoding="utf-8")
    created.append(rel)


def keep(rel):
    d = root / rel
    d.mkdir(parents=True, exist_ok=True)
    if not any(d.iterdir()):
        (d / ".gitkeep").write_text("", encoding="utf-8")


for rel in ["specs", "memory/adr", "memory/archive"] + [f"memory/{k}/{r}" for k in ("tasks", "reports") for r in roles]:
    keep(rel)

write("AGENTS.md", f"""
# {name} — AI team
This project is run by an AI team. Roles, memory and protocols live in this repo.
- If you were given a role (NN <ROLE>), your role is in team/NN_<ROLE>_START.md. Re-read it and continue.
- If you have no role and the user talks to you directly, you are MASTER: read memory/MASTER_START.md and follow it.
- Team, models and runtime: TEAM_MANIFEST.md, team/RUNTIME.md. State: memory/SESSION_STATE.md.
""")

pointer = {"claude": ("CLAUDE.md", "@AGENTS.md\n"), "gemini": ("GEMINI.md", "See AGENTS.md.\n"),
           "antigravity": ("GEMINI.md", "See AGENTS.md.\n")}.get(args.harness)
if pointer:
    p = root / pointer[0]
    if p.exists():
        if "AGENTS.md" not in p.read_text(encoding="utf-8"):
            with p.open("a", encoding="utf-8") as f:
                f.write("\n\n## AI team\n" + pointer[1])
            created.append(pointer[0] + " (appended)")
        else:
            skipped.append(pointer[0])
    else:
        write(pointer[0], pointer[1])

reentry_b = "проверь связь с командой (ListAgents / list_sessions), " if args.mode == "B" else ""
write("memory/MASTER_START.md", f"""
Ты — MASTER проекта «{name}». Прочитай team/00_MASTER_START.md (твоя роль и протоколы), затем memory/SESSION_STATE.md, memory/sessions.json и последние записи CHANGELOG.
Если это первый запуск (SESSION_STATE пуст) — выполни раздел «Старт».
Иначе — {reentry_b}продолжи с места, указанного в SESSION_STATE, и коротко напиши пользователю, где мы и что делаешь дальше.
""")
write("memory/sessions.json", json.dumps({"mode": args.mode, "roles": {}}, ensure_ascii=False, indent=2) + "\n")
write("memory/SESSION_STATE.md", """
# SESSION_STATE
<!-- ≤40 строк. Переписывай целиком, не дописывай в конец. -->
Фаза: старт, аудит MASTER не проводился
Milestone: —
В работе: —
Заблокировано: —
Следующий шаг: MASTER — аудит и граф первых задач
Риски: —
""")
write("memory/DECISIONS.md", """
# DECISIONS
<!-- ## D-NNN <название>
Status: PROPOSED | ACCEPTED | IMPLEMENTED | SUPERSEDED | REJECTED
Date / Owner / Decision / Reason / Affects
Закрытые (SUPERSEDED / REJECTED) переноси в archive/. -->
""")
write("memory/OPEN_QUESTIONS.md", """
# OPEN_QUESTIONS
<!-- ## Q-NNN <вопрос>
Why it matters / Options / Recommendation / Owner / Blocking / Status: OPEN | RESOLVED | DEFERRED
Закрытые переноси в archive/. -->
""")
write("memory/CHANGELOG.md", f"""
# CHANGELOG
<!-- Новые сверху, одна строка на событие. Длиннее ~150 строк — старое в archive/. -->
- Bootstrap: команда MASTER + {", ".join(roles)}, режим {args.mode}
""")
write("memory/IDEAS.md", "# IDEAS\n<!-- Идеи пользователя, ещё не в плане. -->\n")

model_rows = "\n".join(f"| {i:02d} {r} | {models.get(r, 'TBD')} |" for i, r in enumerate(roles, 1))
write("team/RUNTIME.md", f"""
# RUNTIME — {name}
Пакет: mastermind v{VERSION}

## Среда и режим
Среда: {args.harness}. Режим: {args.mode}.
TBD — как именно MASTER вызывает специалистов (runtimes.md §4 / блок режима в 00_MASTER_START.md).

## Модели
| Роль | Модель |
|------|--------|
| 00 MASTER | TBD |
{model_rows}

## Проверки
TBD — TECH defines in first task

## Лимиты
- Задач за milestone без отчёта пользователю: {per_milestone}
- Доработок одной задачи до эскалации: {rework}
- Параллельных задач: {parallel}
""")

if args.harness == "claude":
    for f in ("pre_compact.py", "restore_context.py"):
        dst = root / ".claude" / "hooks" / f
        if dst.exists():
            skipped.append(f".claude/hooks/{f}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(skill / "assets" / "hooks" / f, dst)
            created.append(f".claude/hooks/{f}")
    settings = root / ".claude" / "settings.json"
    ours = json.loads((skill / "assets" / "settings.json").read_text(encoding="utf-8"))
    if settings.exists():
        cur = json.loads(settings.read_text(encoding="utf-8") or "{}")
        hooks = cur.setdefault("hooks", {})
        changed = False
        for event, entries in ours["hooks"].items():
            have = " ".join(h.get("command", "") for x in hooks.get(event, []) for h in x.get("hooks", []))
            for e in entries:
                script = e["hooks"][0]["command"].split("/.claude/hooks/")[1].split('"')[0]
                if script not in have:
                    hooks.setdefault(event, []).append(e)
                    changed = True
        if changed:
            settings.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            created.append(".claude/settings.json (hooks merged)")
        else:
            skipped.append(".claude/settings.json")
    else:
        write(".claude/settings.json", json.dumps(ours, ensure_ascii=False, indent=2) + "\n")

    gi = root / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if ".claude/compact/" not in text.splitlines():
        with gi.open("a", encoding="utf-8") as f:
            f.write(("\n" if text and not text.endswith("\n") else "") + ".claude/compact/\n")
        created.append(".gitignore (+ .claude/compact/)")

    if args.mode == "A":
        for i, r in enumerate(roles, 1):
            write(f".claude/agents/{r.lower()}.md", f"""
---
name: {r.lower()}
description: {r} specialist for {name}. Use for tasks with Owner: {r}.
model: {models.get(r, "inherit")}
---
Your permanent role is defined in team/{i:02d}_{r}_START.md — read it first and follow it.
You are being called as a subagent: skip the READY step and execute the TASK you were given.
Finish with a TASK REPORT and save it to memory/reports/{r}/<TASK-ID>.md.
""")

for c in created:
    print(f"+ {c}")
for s in skipped:
    print(f"= {s} (exists, kept)")
todo = ["TEAM_MANIFEST.md", "PROJECT_PLAN.md", "ARCHITECTURE.md", "memory/MASTER_CONTEXT.md",
        "team/00_MASTER_START.md"] + [f"team/{i:02d}_{r}_START.md" for i, r in enumerate(roles, 1)]
todo = [t for t in todo if not (root / t).exists()]
print("\nStill to write:", ", ".join(todo))
note = f"; write native agent files for {args.harness} (runtimes.md §4)" if args.mode == "A" and args.harness != "claude" else ""
print(f"Also fill TBD in team/RUNTIME.md{note}.")
