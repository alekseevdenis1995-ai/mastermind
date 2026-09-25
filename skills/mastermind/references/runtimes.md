# Runtimes: harnesses, capabilities, models

Mastermind must work in whatever agent harness it is running in: Claude Code, Codex CLI, Cursor, OpenCode, Gemini CLI, GitHub Copilot, Windsurf/Devin, Kilo, Kiro, Factory Droid, Amp, Goose. It must also work inside multi-agent launchers such as Orca. This file tells you how to detect where you are, what you can do there, and which models to give each role.

Facts here were checked in late 2026. Harnesses change fast: when a format below is rejected or a command doesn't exist, trust the harness over this file, adapt, and tell the user in one line.

## Contents
1. Detect the harness
2. Capability → mode
3. Discover models and map them to tiers
4. Native agent definitions per harness
5. Instruction files and context restore
6. Orca and other multi-agent launchers

---

## 1. Detect the harness

Check these in order; stop at the first confident match. Don't ask the user unless nothing matches.

| Signal | Harness |
|---|---|
| You have an `Agent`/`Task` tool with a `model` parameter and `CLAUDECODE=1` in env | Claude Code |
| …plus `mcp__ccd_session_mgmt__*` / `SendMessage` to other sessions in your tool list | Claude Code **Desktop** (mode B possible) |
| env `CODEX_*`, or you are told you are Codex; `~/.codex/config.toml` exists | Codex CLI |
| env `GEMINI_CLI`/`GEMINI_*`, or GEMINI.md conventions in your system prompt | Gemini CLI |
| env `OPENCODE*`, `opencode.json` in project or `~/.config/opencode/` | OpenCode |
| Cursor tool names / system prompt mentions Cursor | Cursor |
| Copilot system prompt / `.github/copilot-instructions.md` workflow | GitHub Copilot |
| env `GOOSE_*` | Goose |
| env or prompt mentions Orca / you run inside an Orca worktree (`orca` CLI on PATH) | Orca-launched agent — see §6 |

Your own system prompt usually names the product. Use that first.

## 2. Capability → mode

| Capability | How to check | Enables |
|---|---|---|
| Spawn subagents | a Task/Agent/subagent tool is in your tool list | mode **A** |
| Choose model per subagent | the tool has a `model` param, or the harness supports agent files with `model:` (§4) | per-role models in A |
| Message other live sessions | Claude Code Desktop session tools (`list_sessions`, `SendMessage`) | mode **B** |
| None of the above | — | mode **C** (manual relay), always available |

Mode C works everywhere, including plain chat UIs and Orca. It is also the fallback when A or B break mid-project.

## 3. Discover models and map them to tiers

Roles need **tiers**, not model names:

| Tier | Used for | Examples by vendor (verify availability) |
|---|---|---|
| **HEAVY** | MASTER, architecture, cross-domain reasoning, hard debugging | Claude `opus` · OpenAI GPT-5.x high reasoning · Gemini Pro |
| **STANDARD** | most implementation, content, design | Claude `sonnet` · GPT-5.x medium / codex models · Gemini Pro/Flash |
| **LIGHT** | mechanical edits, checklists, bulk transforms, QA scripts | Claude `haiku` · GPT-5.x mini / low reasoning · Gemini Flash / Flash-Lite |

**Discovery, by harness:**
- **Claude Code:** the aliases `opus`, `sonnet` and `haiku` are always accepted by the Agent tool and agent files. Your own model is in your system prompt.
- **Codex:** read `~/.codex/config.toml` (`model`, `[profiles.*]`, `model_reasoning_effort`). If only one model is configured, vary `model_reasoning_effort` (high / medium / low) as the tier.
- **OpenCode:** run `opencode models`; ids look like `provider/model`. Prefer models from providers that already have credentials.
- **Gemini CLI:** `~/.gemini/settings.json` → `model.name`. Pro and Flash are normally both available on the same key.
- **Goose:** env `GOOSE_MODEL` / `GOOSE_PROVIDER`, `~/.config/goose/config.yaml`.
- **Cursor, Copilot, Windsurf, Kiro, Amp:** models come from the user's subscription and can't be listed reliably from inside. Use `inherit` / the harness's "fast" option where it exists, or ask once.
- **Unknown:** ask once, as a multiple choice where possible: «Какие модели у вас подключены? (например: Claude Opus/Sonnet/Haiku, GPT-5, Gemini Pro/Flash, локальные)».

**Mapping rules:**
- MASTER gets the best HEAVY model available.
- If only one model exists, every role uses it. Differentiate with reasoning effort where the harness supports it; otherwise don't pretend there are tiers.
- If several vendors are connected (OpenCode, Goose, Orca), you may mix: e.g. TECH on a strong coding model, CONTENT on a cheaper one. Record why.
- Write the result to `TEAM_MANIFEST.md` as `Role | Tier | Harness | Model | Why`, and a copy in `team/RUNTIME.md`.

## 4. Native agent definitions per harness

When the harness supports agent files with a model field, generate one per specialist. The specialist then becomes a first-class subagent with the right model, and the MASTER only has to name it. Keep the role in one place: the agent file's body points at `team/NN_<ROLE>_START.md`.

Body, the same for all formats:

```
Your permanent role is defined in team/<NN>_<ROLE>_START.md — read it first and follow it.
You are being called as a subagent: skip the READY step and execute the TASK you were given.
Finish with a TASK REPORT and save it to memory/reports/<ROLE>/<TASK-ID>.md.
```

| Harness | File | Frontmatter / keys |
|---|---|---|
| Claude Code | `.claude/agents/<role>.md` | `name`, `description`, `model: opus\|sonnet\|haiku\|inherit` |
| Codex CLI | `.codex/agents/<role>.toml` (UNSURE: may be user-level only, `~/.codex/agents/`) | `name`, `description`, `model`, `model_reasoning_effort`, instructions key per current Codex docs |
| Cursor | `.cursor/agents/<role>.md` | `name`, `description`, `model: inherit\|fast\|<id>` |
| OpenCode | `.opencode/agents/<role>.md` | `description`, `mode: subagent`, `model: provider/id` |
| Gemini CLI | `.gemini/agents/<role>.md` | `name`, `description`, `model` |
| GitHub Copilot | `.github/agents/<role>.agent.md` | `description`, `model` |
| Kilo Code | `.kilo/agents/<role>.md` | `model: provider/id` |
| Factory Droid | `.factory/droids/<role>.md` | `model` (droids can't spawn sub-droids) |

`description` should say when to use the agent, e.g. "TECH lead for <Project>: backend, DB, integrations. Use for tasks with Owner: TECH." Generate files only for the harness you're in, plus Claude Code's if `.claude/` is already used. Don't litter the repo with eight formats.

If there is no agent-file support but the subagent tool takes a `model` param, pass the model per call. If neither exists, subagents inherit the MASTER's model. Say so in RUNTIME.md.

## 5. Instruction files and context restore

Every harness re-reads its project instruction file at session start. That file is the universal way to restore context after `/clear`, compaction or a restart.

- Always write **`AGENTS.md`**. It is read by Codex, Cursor, OpenCode, Copilot, Amp, Factory, Goose and others.
- Also write a one-line pointer file for the current harness when it doesn't read AGENTS.md: `CLAUDE.md` (Claude Code), `GEMINI.md` (Gemini CLI). Content: `See AGENTS.md.` plus nothing else project-specific. On Claude Code, `@AGENTS.md` imports it.

AGENTS.md content (short):

```markdown
# <Project> — AI team
This project is run by an AI team. Roles, memory and protocols live in this repo.
- If you were given a role (NN <ROLE>), your role is in team/NN_<ROLE>_START.md. Re-read it and continue.
- If you have no role and the user talks to you directly, you are MASTER: read memory/MASTER_START.md and follow it.
- Team, models and runtime: TEAM_MANIFEST.md, team/RUNTIME.md. State: memory/SESSION_STATE.md.
```

**Claude Code only:** also install the SessionStart hook (`assets/settings.json` + `assets/hooks/restore_context.py`). It injects the exact role on clear/compact, including per-chat roles in mode B.

## 6. Orca and other multi-agent launchers

Orca (Stably) is not a model harness. It runs many agent CLIs (Claude Code, Codex, OpenCode, Cursor CLI, Copilot…) in parallel, **each in its own git worktree and branch**, on the user's own subscriptions. For Mastermind this means:

- **Mode C, with per-role harness choice.** Each specialist can run in a different CLI: e.g. TECH in Codex, DESIGN in Claude Code, QA in a cheap OpenCode model. Put `Harness` per role in the manifest. The user launches one Orca agent per role and pastes its start prompt.
- **Worktrees change the memory rules.** Each agent sees its own branch, so a shared `memory/` would diverge.
  - `main` is owned by MASTER: tasks, decisions, state.
  - Each specialist works on `role/<ROLE>`, commits code plus `memory/reports/<ROLE>/<ID>.md`, and never edits other memory files.
  - MASTER reviews with `git diff main...role/<ROLE>`, reads reports with `git show role/<ROLE>:memory/reports/<ROLE>/<ID>.md`, and merges accepted work into `main`. That merge is the integration step.
  - Specialists read tasks from the pasted TASK block, or `git show main:memory/tasks/<ROLE>/<ID>.md`.
- **Automatic dispatch.** If the `orca` CLI is on PATH, run `orca --help` and `orca skills get orchestration`. If it can create worker tasks programmatically (Runs, tasks, supervised workers), use that instead of manual relay, and describe the actual commands in RUNTIME.md. If you're unsure it works, fall back to mode C and say so.
- Tell the user to launch all Orca agents from the same repo, and to leave the MASTER on `main`.

Other launchers that isolate agents in worktrees (Conductor, Claude Squad, and similar) follow the same rules.
