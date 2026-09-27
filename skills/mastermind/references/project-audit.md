# Existing project — audit and recommendation

Used when the target folder already has work in it: code, docs, or a Mastermind package. The user wants to know where the project stands and what to do next — not an automatic team.

Read-only until the user picks an option. Don't change files, don't run installs or migrations.

## 1. What is here

Survey cheaply: tree to depth 2–3, README / docs, manifests (`package.json`, `pyproject.toml`, `go.mod`, `*.csproj`, …), CI configs, test folders, `git log --oneline -30`, `git status`, open TODO/FIXME count. For big repos fan out read-only subagents per top-level area if you have them. Don't read every source file.

Classify:
- **A. Code project without a team** — the usual case.
- **B. Mastermind package exists** (`TEAM_MANIFEST.md`, `team/`, `memory/`) — the team is running or stalled.
- **C. Only docs / specs, little or no code** → treat as Phase 1a (ready ТЗ).

## 2. Assess

**For A (code project):**
- Goal and state: what it is, how far along (prototype / MVP / production), what works.
- Health: do tests / lint / build exist and pass (run them only if they are fast and side-effect free; otherwise say "не запускал")? Test coverage in rough terms, CI present?
- Structure: clear modules or a tangle, obvious duplication, dead code, secrets in the repo (report only the path, never the value).
- Momentum: recent commits, abandoned branches, unfinished features, TODOs.
- Risks: missing tests around critical parts, outdated deps with known issues, no backups/migrations for data.
- Team fit: how many independent domains there really are (protocol §3, §5; presets in `team-presets.md`).

**For B (existing package):**
- Run `scripts/check_package.py <project>`.
- Read `SESSION_STATE.md`, top of `CHANGELOG.md`, `TEAM_MANIFEST.md`, `team/RUNTIME.md`, recent reports.
- Look for: stalled work (no CHANGELOG entries lately, tasks stuck IN_PROGRESS/BLOCKED), roles with no tasks, roles that got most FAILs, bloated memory (SESSION_STATE > 40 lines, huge CHANGELOG), models too strong/weak for what a role does, a ТЗ that has moved on from the plan, missing «Проверки» / «Лимиты».

## 3. Recommend

Show one short report in the user's language:

```
**Проект:** <что это, стадия>
**Состояние:** <3–6 пунктов: что хорошо, что плохо — с фактами (файлы, цифры)>
**Главные риски:** <1–3>
**Вердикт:** <одно из ниже>
**Предлагаю:** <1–3 конкретных шага>
```

Verdicts — pick one honestly; "всё хорошо" is a valid answer:
1. **Всё в порядке, команда не нужна** — small or healthy project; give 1–3 next steps and stop.
2. **Навести порядок сначала** — no tests/CI, broken build, secrets, chaos. List the fixes; offer a team with a first milestone "stabilise" if it's bigger than a few hours.
3. **Развернуть команду** — enough independent work for specialists. Go to Phase 2 with this analysis as input: the codebase counts as KNOWN, the ТЗ is reconstructed from code + README (write `specs/TZ.md` marked "восстановлено из кода", user confirms).
4. **(B) Поправить команду** — concrete changes: merge/add/remove roles, change models, archive memory, update the plan to the current ТЗ, fix package errors. After "да", apply them to TEAM_MANIFEST, RUNTIME, start files, agent files and memory, record a decision in DECISIONS.md, commit. If the package is outdated, include the upgrade (§4).
5. **(B) Команда в порядке** — say so, give the MASTER re-entry line to continue. If the package is outdated, still offer the upgrade (§4).

Ask which option they want; do nothing before that.

## 4. Upgrading a package built by an older Mastermind

A package is outdated when `team/RUNTIME.md` is missing, has no `## Проверки` / `## Лимиты`, has no `Пакет: mastermind v…` line, or `.claude/hooks/pre_compact.py` is missing. Offer the upgrade as part of verdict 4 or 5. Ask the user to stop the project's MASTER and specialist sessions first — they write the same files.

Show the plan, then after "да":
1. `python scripts/scaffold.py <project> --name … --mode <from sessions.json or RUNTIME> --roles <from team/NN_*_START.md> --harness …` — adds only what's missing (RUNTIME skeleton, archive/, sessions.json, hooks, settings merge, .gitignore).
2. Replace `.claude/hooks/restore_context.py` and `pre_compact.py` with the skill's current `assets/hooks/` versions (they belong to the skill, not the project).
3. `team/RUNTIME.md`: add `## Проверки` with the project's real test/lint/build commands (look in package.json, pyproject, Makefile, CI) and `## Лимиты`; add `Пакет: mastermind v<version>` at the top.
4. `team/00_MASTER_START.md`: insert the sections from the current `master-template.md` that it lacks — «Проверки перед PASS», «Ревью другой моделью», «Лимиты», «Ретро после milestone», «Экономия контекста», and the Проверки hint in «Старт». Fill them for this project. Don't rewrite the project-specific parts.
5. Each specialist start file: add the two lines from `specialist-template.md` about reading only the task's files and not writing PASS without checks.
6. If SESSION_STATE > 40 lines or CHANGELOG > 150 lines — propose trimming into `memory/archive/`, don't do it silently.
7. `memory/DECISIONS.md`: record `D-NNN Mastermind upgraded to v<version>`; CHANGELOG line; `check_package.py`; commit `memory: mastermind upgrade v<version>`.

Tell the user to restart MASTER afterwards («Прочитай memory/MASTER_START.md и продолжай»), so it re-reads the new rules.

## 5. Deploying into an existing repo

When the user chooses to deploy a team:
- Never overwrite existing files. If `AGENTS.md` / `CLAUDE.md` / `.claude/settings.json` exist, **append** a Mastermind section or merge hooks — show what you'll change first.
- Put the package next to the code (`team/`, `memory/`, `specs/`, root docs); don't move source files.
- The existing test/lint/build commands become `## Проверки` in RUNTIME.md.
- Existing conventions (branching, commit style, CI) go into every start prompt.
