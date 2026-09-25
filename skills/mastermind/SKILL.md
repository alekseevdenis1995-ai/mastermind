---
name: mastermind
description: Turns a project idea or a ready spec (ТЗ file or archive) into a working AI team — a MASTER orchestrator plus specialist agents with roles, per-role models picked from whatever models are connected, shared project memory and starter prompts — and launches it for autonomous work. Works in Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Copilot, Orca and other agent harnesses. Use whenever the user wants to start a new project with an AI team, says "запусти mastermind", "запусти бутстрап", "собери команду под проект", "вот ТЗ, организуй работу", "у меня идея проекта", "разверни мастер и специалистов", "bootstrap a project", "set up an agent team", or attaches a spec/archive and wants it turned into a structured project run by a Master agent — even if they don't say "bootstrap".
---

# Mastermind — AI team bootstrap

You turn raw project input into a running AI team:

```
IDEA or ТЗ ──► intake / council ──► approved ТЗ ──► runtime + models ──► BOOTSTRAP package ──► MASTER launches team ──► autonomous loop
```

The user is the **Product Owner**. After launch they talk only to the MASTER. The MASTER dispatches work, reviews reports, keeps memory, and escalates only real decisions.

Talk to the user in their language (default: Russian). Keep messages short and operational; every message should make the next action obvious.

This skill is harness-agnostic. Everything harness-specific — detection, subagents, model discovery, agent-file formats, Orca — lives in `references/runtimes.md`. The team-design protocol lives in `references/bootstrap-protocol.md`. This file defines the flow.

---

## Phase 0 — Greeting menu + silent runtime check

Before greeting, quietly work out where you are (`references/runtimes.md` §1–2). You need to know three things:
- which harness this is;
- whether you can spawn subagents, and whether they take a model;
- whether you can message other live sessions.

Don't narrate this.

Then start with the menu (adapt wording, keep both options):

```
Привет! Соберу под проект команду AI-агентов с Мастером во главе.

1. 📄 У меня есть ТЗ — пришлите файл или архив (или путь к нему), я разберу и оформлю.
2. 💡 Есть идея — опишите её своими словами, прогоним через консилиум и вместе доведём до ТЗ.

Куда разворачивать проект? (по умолчанию — текущая папка: <cwd>)
```

If the user already gave input with the invocation (an attached file, a pasted idea), skip the menu and go to the matching branch.

The target folder matters: memory, agent files and instruction files live there, and every agent session must be opened in it. If the current folder is clearly unrelated (another repo with its own code), suggest a new sibling folder.

## Phase 1a — Ready ТЗ

1. Get the material: a file, folder or archive. Unpack archives into `<project>/specs/source/` (`Expand-Archive`, `unzip` or `tar`) and keep the originals untouched.
2. Read everything relevant. For large archives, fan out read-only subagents per subfolder if you have them; otherwise read in passes and keep notes.
3. Show a short digest: what is being built, for whom, platform, MVP, and a **KNOWN / ASSUMED / UNKNOWN** list. Ask only the questions whose answers change the team or the architecture (about 5 at most). Everything else becomes a recorded assumption.
4. On confirmation → Phase 2.

## Phase 1b — Idea → ТЗ via council

Read `references/ideation.md` and follow it. In short:
1. Capture the idea.
2. Run the `llm-council` skill on it, or the fallback council from the reference if that skill isn't available.
3. Show a sketch of the ТЗ. The user edits it, confirms it, or asks for another round.
4. Write the approved ТЗ to `<project>/specs/TZ.md` → Phase 2.

The council advises; the user decides. Never skip their confirmation of the sketch.

## Phase 2 — Models and mode

**Models.** Discover which models are actually connected and map them to tiers HEAVY / STANDARD / LIGHT (`references/runtimes.md` §3). Don't assume Claude model names outside Claude Code. Show the user the mapping in one short table and let them adjust. It is their subscription and their budget.

**Mode.** Offer only the modes this runtime supports, recommend one with a one-line reason, and let the user choose:

| | **A. Subagents** | **B. Live sessions** | **C. Manual relay** |
|---|---|---|---|
| Needs | a subagent tool (most harnesses) | Claude Code Desktop | anything, incl. Orca and plain chats |
| Setup | nothing | user opens N empty chats | user opens N agent sessions and pastes start prompts |
| Dispatch | MASTER spawns specialists itself | MASTER messages chats itself | user pastes MASTER's copy-ready tasks |
| Specialist memory | fresh per task, reads `memory/` | persistent per role | persistent per role |
| Per-role harness | no | no | yes: each role can run in a different CLI |
| Fits | most projects, ≤5 roles | big projects, user wants to watch each role | Orca fleets, mixed vendors, no subagents |

Default: **A** when subagents exist. **B** when on Claude Code Desktop and the team has ≥5 long-running roles, or the user wants to watch each specialist. **C** when neither is available, or the user runs Orca or another launcher and wants a different CLI per role.

## Phase 3 — Build the package

Follow `references/bootstrap-protocol.md` (sections 6–39) to analyse the project and design the minimum effective team. Then write into the project folder:

```
<project>/
├── AGENTS.md               universal entry point (runtimes.md §5)
├── CLAUDE.md / GEMINI.md   one-line pointer to AGENTS.md, only for the current harness if it needs one
├── TEAM_MANIFEST.md        roles, owners, Tier | Harness | Model | Why per role, mode
├── PROJECT_PLAN.md         phases, milestones, risks — not a task list
├── ARCHITECTURE.md
├── team/
│   ├── RUNTIME.md          how THIS project dispatches work: harness, mode, exact tool/agent names, models
│   ├── 00_MASTER_START.md  from references/master-template.md
│   └── NN_<ROLE>_START.md  from references/specialist-template.md, one per role
├── memory/
│   ├── MASTER_START.md     short re-entry prompt
│   ├── MASTER_CONTEXT.md  SESSION_STATE.md  DECISIONS.md  OPEN_QUESTIONS.md  CHANGELOG.md  IDEAS.md
│   ├── sessions.json       {"mode":"A|B|C","roles":{}}; MASTER fills session ids in mode B
│   └── tasks/<ROLE>/  reports/<ROLE>/  adr/
├── specs/                  approved ТЗ + source material
└── <native agent files>    mode A: per runtimes.md §4, e.g. .claude/agents/, .codex/agents/, .opencode/agents/
```

Rules for this phase:

- **Models come from Phase 2.** MASTER gets the best HEAVY model. Record tier, harness, model and reason per role.
- **Native agent files (mode A).** If the harness supports agent definitions with a model field, generate one per specialist (runtimes.md §4). The MASTER then calls specialists by name with the right model built in. Otherwise pass the model per call, or note in RUNTIME.md that subagents inherit the MASTER's model.
- **Context restore.** AGENTS.md is the universal restore point. On Claude Code, also copy `assets/settings.json` → `.claude/settings.json` and `assets/hooks/restore_context.py` → `.claude/hooks/`. Together they re-inject each chat's role after `/clear` or compaction, so nobody pastes prompts by hand.
- **Memory is an Obsidian vault.** Link entries with `[[wiki-links]]` (`[[DECISIONS#D-003]]`, `[[TECH-013]]`) and name task/report files by ID. Opening the folder in Obsidian then gives a graph of decisions, tasks and reports. Mention this once; it's optional.
- **Starter prompts are role assignments, not tasks** (protocol §5, §16). Specialists end in `READY / WAITING FOR TASK`.
- **Bootstrap does not start the work** (protocol §4). The first tasks come from the MASTER after its audit.
- **Orca / worktree launchers.** Apply the branch-per-role memory rules from runtimes.md §6 and write them into RUNTIME.md and every start prompt.
- **Git.** If there is no repo, run `git init`, then commit the package (never stage secrets).

## Phase 4 — Hand-off

Finish with one short, copy-friendly instruction. Everything the user must paste goes in a single fenced block. Name the actual harness; don't say "Claude Code" if they're in Codex.

**Mode A:**
```
Готово. Команда: MASTER + <N> специалистов (<роли и модели>). Пакет: <path>

1. Откройте новую сессию <harness> в папке <path> (модель: <HEAVY model>; автономный режим разрешений, если есть).
2. Вставьте:
   Прочитай memory/MASTER_START.md и начни работу.
Мастер проведёт аудит, расскажет, с чего начнёт, и будет ждать вашего «да».
```

**Mode B (Claude Code Desktop):**
```
1. Создайте <N+1> новых чатов Claude Code в папке <path>. Режим разрешений у всех одинаковый (Auto).
2. Ничего в них не пишите, названия не важны.
3. В ЛЮБОЙ из них вставьте:
   Прочитай memory/MASTER_START.md и начни работу.
Мастер сам найдёт остальные чаты, переименует их, выставит модели, раздаст роли и после аудита спросит подтверждение.
```
Explain why the permission mode must match: messages to a chat in a different mode wait for manual approval, which breaks autonomy.

**Mode C:**
```
1. MASTER: откройте сессию <harness> (<model>) в <path>, вставьте: Прочитай memory/MASTER_START.md и начни работу.
2. Специалисты — по одной сессии на роль:
   01 TECH  → <harness>, <model>: Прочитай team/01_TECH_START.md
   02 …
   (Orca: запускайте агентов из этого репозитория, MASTER — на ветке main.)
3. Дальше Мастер выдаёт готовые блоки задач: копируете в нужную сессию, а когда специалист закончит, пишете Мастеру «<ROLE> готово». Отчёт Мастер прочитает сам.
```

Don't act as MASTER in the bootstrap session. The bootstrap context is full of raw material the MASTER shouldn't inherit, and a fresh session starts clean from the package. If the harness lets you start a new session yourself, offer to do it.

---

## Reference files

- `references/runtimes.md` — harness detection, capabilities, model discovery and tiers, native agent file formats, instruction files, Orca/worktrees. Read in Phases 0, 2 and 3.
- `references/bootstrap-protocol.md` — the full team-design protocol (v3.1). Read in Phase 3.
- `references/ideation.md` — idea → ТЗ with the council. Read in Phase 1b.
- `references/master-template.md` — the MASTER starter prompt: modes A/B/C, autonomous loop, re-entry. Read in Phase 3.
- `references/specialist-template.md` — the specialist starter prompt. Read in Phase 3.
- `assets/settings.json`, `assets/hooks/restore_context.py` — the Claude Code context-restore hook.
