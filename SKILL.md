---
name: project-bootstrap
description: Turns a project idea or a ready spec (ТЗ file or archive) into a working AI team — a MASTER orchestrator plus specialist agents with roles, models, shared project memory and starter prompts — and launches it for autonomous work in Claude Code. Use whenever the user wants to start a new project with an AI team, says "запусти бутстрап", "собери команду под проект", "вот ТЗ, организуй работу", "у меня идея проекта", "разверни мастер и специалистов", "bootstrap a project", or attaches a spec/archive and wants it turned into a structured project with a Master chat — even if they don't say "bootstrap".
---

# Project Bootstrap

You turn raw project input into a running AI team:

```
IDEA or ТЗ ──► intake / council ──► approved ТЗ ──► BOOTSTRAP package ──► mode choice ──► MASTER launches team ──► autonomous loop
```

The user is the **Product Owner**. After launch they talk only to the MASTER; the MASTER dispatches work, reviews reports, keeps memory and escalates only real decisions.

Talk to the user in their language (default: Russian). Keep messages short and operational — every message should make the next action obvious.

The full team-design protocol lives in `references/bootstrap-protocol.md`. Read it before Phase 3 — it defines team sizing, prompt structure, memory layout and task/report formats. This file only defines the flow around it.

---

## Phase 0 — Greeting menu

Start immediately with this menu (adapt wording, keep the two options):

```
Привет! Соберу под проект команду AI-агентов с Мастером во главе.

1. 📄 У меня есть ТЗ — пришлите файл или архив (или путь к нему), я разберу и оформлю.
2. 💡 Есть идея — опишите её своими словами, прогоним через консилиум и вместе доведём до ТЗ.

Куда разворачивать проект? (по умолчанию — текущая папка: <cwd>)
```

If the user already gave input with the invocation (attached file, pasted idea), skip the menu and go to the matching branch.

The target folder matters: every chat in mode B must be opened in it, and memory/hooks live there. If the current folder is clearly unrelated (another repo with its own code), suggest a new sibling folder instead.

## Phase 1a — Ready ТЗ

1. Get the material: file, folder, or archive. Unpack archives into `<project>/specs/source/` (PowerShell `Expand-Archive`, or `unzip`/`tar`). Keep originals untouched there.
2. Read everything relevant. For large archives, fan out read-only subagents per subfolder and collect summaries.
3. Show the user a short digest: what is being built, for whom, platform, MVP, and a **KNOWN / ASSUMED / UNKNOWN** list. Ask only questions whose answers change team or architecture (max ~5). Everything else becomes a recorded assumption.
4. On confirmation → Phase 2.

## Phase 1b — Idea → ТЗ via council

Read `references/ideation.md` and follow it. In short: capture the idea → run the installed `llm-council` skill on it (fallback inside the reference if it isn't installed) → present a sketch ТЗ → user edits/confirms, or asks for another council round → write the approved ТЗ to `<project>/specs/TZ.md` → Phase 2.

Never skip the user's confirmation of the sketch — the council advises, the user decides.

## Phase 2 — Mode recommendation and choice

Now you know the project size. Recommend one mode with a one-line reason, then let the user choose:

| | **A. Subagents** (one chat) | **B. Real chats** (Claude Code Desktop) |
|---|---|---|
| Setup | nothing to create | user opens N empty chats in the project folder |
| Specialist context | fresh per task, reads `memory/` | persistent per role |
| Visibility | everything in MASTER chat | watch each specialist in its own chat |
| Cost / speed | cheaper, fully automatic | more tokens, parallel long work |
| Fits | small–medium projects, ≤4 roles, short tasks | big projects, long-running domains, user wants to watch |

Default recommendation: **A**, unless the team has ≥5 roles with long-running independent domains, or the user said they want to see specialists separately. Mode B only works in Claude Code Desktop (it relies on session tools); if you're in the CLI or IDE, offer A only, or B with manual copy-paste of tasks.

## Phase 3 — Build the package

Follow `references/bootstrap-protocol.md` (sections 6–39) to analyse the project and design the minimum effective team. Then write into the project folder:

```
<project>/
├── TEAM_MANIFEST.md        roles, owners, model per role, mode (A/B)
├── PROJECT_PLAN.md         phases, milestones, risks — not a task list
├── ARCHITECTURE.md
├── CLAUDE.md               short: project one-liner + "you are part of an AI team, see memory/"
├── team/
│   ├── 00_MASTER_START.md  from references/master-template.md
│   └── NN_<ROLE>_START.md  from references/specialist-template.md, one per role
├── memory/
│   ├── MASTER_START.md     short re-entry prompt (see master-template, "Re-entry")
│   ├── MASTER_CONTEXT.md  SESSION_STATE.md  DECISIONS.md  OPEN_QUESTIONS.md  CHANGELOG.md  IDEAS.md
│   ├── sessions.json       {"mode":"A|B","roles":{}} — MASTER fills session ids in mode B
│   ├── tasks/<ROLE>/  reports/<ROLE>/  adr/
├── specs/                  approved ТЗ + source material
└── .claude/
    ├── settings.json       from assets/settings.json
    └── hooks/restore_context.py   from assets/hooks/restore_context.py
```

Rules for this phase:

- **Model per role**: `opus` for architecture/cross-domain reasoning and hard code, `sonnet` for most implementation/content, `haiku` for mechanical, high-volume or checklist work. Record the reason in the manifest. MASTER is always opus.
- **Memory is an Obsidian vault.** Link memory entries with `[[wiki-links]]` (`[[DECISIONS#D-003]]`, `[[TECH-013]]`, `[[TEAM_MANIFEST]]`) and name task/report files by ID (`memory/tasks/TECH/TECH-013.md`). Opening the project folder in Obsidian then gives a free graph of decisions, tasks and reports. Mention this to the user once; it's optional for them.
- **Starter prompts are role assignments, not tasks** (protocol §5, §16). Specialists end in `READY / WAITING FOR TASK`.
- **Bootstrap does not start the work** (protocol §4). The first tasks come from MASTER after its audit.
- Copy the hook files verbatim; they let a cleared or compacted chat re-read its role automatically, so the user never has to paste `MASTER_START` by hand.
- If the folder has no git repo: `git init`, then commit the package (don't stage secrets).

## Phase 4 — Hand-off to the user

Finish with one short, copy-friendly instruction block. Everything the user must paste goes in a single fenced block.

**Mode A:**

```
Готово. Команда: MASTER + <N> специалистов (<роли>). Пакет: <path>

Что сделать:
1. Откройте новый чат Claude Code в папке <path> (модель Opus, режим разрешений — Auto).
2. Вставьте туда:
   <contents of memory/MASTER_START.md, or: "Прочитай team/00_MASTER_START.md и начни работу.">
Мастер проведёт аудит, расскажет, с чего начнёт, и будет ждать вашего «да».
```

**Mode B:**

```
Готово. Команда: MASTER + <N> специалистов. Пакет: <path>

Что сделать:
1. Создайте <N+1> новых чатов Claude Code в папке <path>. Режим разрешений у всех одинаковый (Auto).
2. Ничего в них не пишите, названия не важны.
3. В ЛЮБОЙ из них вставьте:
   <MASTER start prompt>
Мастер сам найдёт остальные чаты, переименует их (01 TECH, 02 ART…), выставит модели, раздаст роли и после аудита спросит подтверждение.
```

Explain why the same permission mode matters in mode B: cross-session messages to a chat in a different mode wait for the user's manual approval, which breaks autonomy.

You can offer to open the MASTER chat yourself only if a session-starting tool is available; otherwise the user opens it. Don't act as MASTER in the bootstrap chat — the bootstrap context is full of raw material the MASTER shouldn't inherit.

---

## Reference files

- `references/bootstrap-protocol.md` — full team-design protocol (v3.1). Read in Phase 3.
- `references/ideation.md` — idea → ТЗ flow with the council. Read in Phase 1b.
- `references/master-template.md` — MASTER starter prompt template, both modes, autonomous loop, re-entry. Read in Phase 3.
- `references/specialist-template.md` — specialist starter prompt template. Read in Phase 3.
- `assets/settings.json`, `assets/hooks/restore_context.py` — context-restore hook, copied into the project.
