---
name: mastermind
description: Builds and runs an AI team (MASTER orchestrator + specialist agents, per-role models, shared memory) from an idea, a spec/archive, or an existing project it audits first. Any agent harness. Use for "запусти mastermind", "собери команду под проект", "вот ТЗ, организуй работу", "проанализируй проект, что дальше", "bootstrap a project", "set up an agent team".
---

# Mastermind — AI team bootstrap

You turn raw project input into a running AI team:

```
IDEA or ТЗ ──► intake / council ──► approved ТЗ ──► runtime + models ──► BOOTSTRAP package ──► MASTER launches team ──► autonomous loop
EXISTING PROJECT ──► audit ──► verdict: all good / fix first / deploy team / adjust team
```

The user is the **Product Owner**. After launch they talk only to the MASTER. The MASTER dispatches work, reviews reports, keeps memory, and escalates only real decisions.

Talk to the user in their language (default: Russian). Keep messages short and operational; every message should make the next action obvious.

This skill is harness-agnostic. Everything harness-specific — detection, subagents, model discovery, agent-file formats, Orca — lives in `references/runtimes.md`. The team-design protocol lives in `references/bootstrap-protocol.md`. This file defines the flow.

---

## Phase 0 — Greeting menu + silent runtime check

Before greeting, quietly work out where you are (`references/runtimes.md` §1–2). You need to know three things:
- which harness this is;
- whether you can spawn subagents, and whether they take a model;
- whether you can message other live sessions (`SendMessage` + `ListAgents` — look in the deferred-tools list too; if you only see them there, they still count).

Also glance at the current folder (one `ls` + `git log --oneline -3`): is it empty, a code project, or a Mastermind package (`TEAM_MANIFEST.md`, `team/`, `memory/`)?

Don't narrate this.

Then start with the menu (adapt wording). If the folder has a project in it, put option 3 first and recommend it:

```
Привет! Соберу под проект команду AI-агентов с Мастером во главе.

1. 📄 У меня есть ТЗ — пришлите файл или архив (или путь к нему), я разберу и оформлю.
2. 💡 Есть идея — опишите её своими словами, прогоним через консилиум и вместе доведём до ТЗ.
3. 🔍 Проект уже идёт — проанализирую его и скажу, что лучше сделать дальше (или что всё хорошо).

Куда разворачивать проект? (по умолчанию — текущая папка: <cwd>)
```

If the user already gave input with the invocation (an attached file, a pasted idea, "проанализируй проект"), skip the menu and go to the matching branch.

The target folder matters: memory, agent files and instruction files live there, and every agent session must be opened in it. For options 1–2 in a folder that holds an unrelated project, suggest a new sibling folder.

## Phase 1c — Existing project

Read `references/project-audit.md` and follow it: audit read-only, give a short report and one honest verdict (all good / fix first / deploy a team / adjust the existing team), then wait for the user's choice. "Deploy a team" continues with Phase 2; "adjust the team" applies the changes and ends.

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
| Needs | a subagent tool (most harnesses) | Claude Code with `SendMessage` + `ListAgents` (Desktop, VS Code, JetBrains, CLI; deferred tools count) | anything, incl. Orca and plain chats |
| Setup | nothing | user opens N empty chats | user opens N agent sessions and pastes start prompts |
| Dispatch | MASTER spawns specialists itself | MASTER messages chats itself | user pastes MASTER's copy-ready tasks |
| Specialist memory | fresh per task, reads `memory/` | persistent per role | persistent per role |
| Per-role harness | no | no | yes: each role can run in a different CLI |
| Fits | most projects, ≤5 roles | big projects, user wants to watch each role | Orca fleets, mixed vendors, no subagents |

Default: **A** when subagents exist. **B** when `SendMessage` + `ListAgents` are available (check the deferred-tools list too — in VS Code they are usually deferred) and the team has ≥5 long-running roles, or the user wants to watch each specialist. **C** when neither is available, or the user runs Orca or another launcher and wants a different CLI per role.

**Limits.** In the same message show the default limits (protocol §8: 10 tasks per milestone before a report, 2 rework rounds before escalation, 3 parallel tasks) and let the user change them.

## Phase 3 — Build the package

Follow `references/bootstrap-protocol.md` to design the minimum effective team, starting from `references/team-presets.md`.

**Scaffold first.** Run:
```
python <skill>/scripts/scaffold.py <project> --name "<Project>" --mode <A|B|C> --roles TECH,QA --harness <claude|codex|…> --models TECH=sonnet,QA=haiku --limits 10,2,3
```
It creates the boilerplate (folders, seeded memory, sessions.json, MASTER_START re-entry, AGENTS.md + pointer file, RUNTIME skeleton, Claude Code hooks/settings/.gitignore and agent files) without overwriting anything, and prints what is left. Don't rewrite what it made — spend your effort on the files that need thought: TEAM_MANIFEST, PROJECT_PLAN, ARCHITECTURE, MASTER_CONTEXT, the start prompts, the TBD lines in RUNTIME, and native agent files for non-Claude harnesses. If Python isn't available, write everything by hand.

The finished package:

```
<project>/
├── AGENTS.md               universal entry point (runtimes.md §5)
├── CLAUDE.md / GEMINI.md   one-line pointer to AGENTS.md, only for the current harness if it needs one
├── TEAM_MANIFEST.md        roles, owners, Tier | Harness | Model | Why per role, mode
├── PROJECT_PLAN.md         phases, milestones, risks — not a task list
├── ARCHITECTURE.md
├── team/
│   ├── RUNTIME.md          how THIS project dispatches work: harness, mode, tool/agent names, models, Проверки, Лимиты
│   ├── 00_MASTER_START.md  from references/master-template.md
│   └── NN_<ROLE>_START.md  from references/specialist-template.md, one per role
├── memory/
│   ├── MASTER_START.md     short re-entry prompt
│   ├── MASTER_CONTEXT.md  SESSION_STATE.md  DECISIONS.md  OPEN_QUESTIONS.md  CHANGELOG.md  IDEAS.md
│   ├── sessions.json       {"mode":"A|B|C","roles":{}}; MASTER fills session ids in mode B
│   └── tasks/<ROLE>/  reports/<ROLE>/  adr/  archive/
├── specs/                  approved ТЗ + source material
└── <native agent files>    mode A: per runtimes.md §4, e.g. .claude/agents/, .codex/agents/, .opencode/agents/
```

Rules for this phase:

- **Models come from Phase 2.** MASTER gets the best HEAVY model. Record tier, harness, model and reason per role.
- **Native agent files (mode A).** If the harness supports agent definitions with a model field, generate one per specialist (runtimes.md §4). The MASTER then calls specialists by name with the right model built in. Otherwise pass the model per call, or note in RUNTIME.md that subagents inherit the MASTER's model.
- **Context restore.** AGENTS.md is the universal restore point. On Claude Code the scaffold also installs two hooks: PreCompact snapshots git state and stale memory; SessionStart re-injects each chat's role plus that snapshot after `/clear` or compaction, so nobody pastes prompts by hand.
- **Quality gate.** Fill `## Проверки` in RUNTIME.md with the project's real test/lint/build commands (protocol §7) and `## Лимиты` from Phase 2.
- **Memory is an Obsidian vault.** Link entries with `[[wiki-links]]` (`[[DECISIONS#D-003]]`, `[[TECH-013]]`) and name task/report files by ID. Opening the folder in Obsidian then gives a graph of decisions, tasks and reports. Mention this once; it's optional.
- **Starter prompts are role assignments, not tasks** (protocol §2). Specialists end in `READY / WAITING FOR TASK`.
- **Bootstrap does not start the work** (protocol §1). The first tasks come from the MASTER after its audit.
- **Orca / worktree launchers.** Apply the branch-per-role memory rules from runtimes.md §6 and write them into RUNTIME.md and every start prompt.
- **Validate.** Run `python scripts/check_package.py <project>` (path relative to this skill). Fix every ERROR; mention WARNs only if they matter.
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
**Mode B-lite (Claude Code in VS Code / JetBrains / CLI):**
```
1. Откройте <N+1> новых чатов Claude Code в папке <path>. Режим разрешений у всех одинаковый (Auto).
2. В каждом чате специалиста выберите модель: <ROLE> — <model>, … (менять модель чужого чата Мастер не может).
3. В ЛЮБОЙ из них (с моделью <HEAVY model>) вставьте:
   Прочитай memory/MASTER_START.md и начни работу.
Мастер сам найдёт остальные чаты через ListAgents, раздаст им роли и попросит переименовать вкладки. Остальные чаты не трогайте — пишет им Мастер.
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
- `references/bootstrap-protocol.md` — the team-design protocol (v4). Read in Phase 3.
- `references/team-presets.md` — starting teams by project type. Read in Phase 3 and 1c.
- `references/project-audit.md` — audit of an existing project or team. Read in Phase 1c.
- `references/ideation.md` — idea → ТЗ with the council. Read in Phase 1b.
- `references/master-template.md` — the MASTER starter prompt: modes A/B/C, autonomous loop, re-entry. Read in Phase 3.
- `references/specialist-template.md` — the specialist starter prompt. Read in Phase 3.
- `assets/settings.json`, `assets/hooks/` — the Claude Code PreCompact + context-restore hooks.
- `scripts/scaffold.py` — writes the package boilerplate. Run at the start of Phase 3.
- `scripts/check_package.py` — validates the generated package. Run at the end of Phase 3 and in Phase 1c.
