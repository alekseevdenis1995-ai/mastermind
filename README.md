# Mastermind 🧠

**Одна команда — и у вашего проекта есть AI-команда: Мастер-оркестратор, специалисты с ролями и моделями, общая память и автономный цикл работы в Claude Code.**

[English below](#english)

```
Идея или ТЗ ──► консилиум ──► ТЗ ──► команда + архитектура + память ──► MASTER ──► задачи ──► отчёты ──► релиз
```

Вы — владелец продукта. Вы говорите только с Мастером. Мастер проводит аудит, ставит задачи специалистам, принимает отчёты, ведёт память и приходит к вам только за решениями.

## Что умеет

- **Два входа:** готовое ТЗ (файл или архив) или сырая идея, которую прогоняет консилиум из 5 советников (скилл `llm-council`) и доводит с вами до ТЗ.
- **Минимальная эффективная команда:** роли, зоны ответственности, модель для каждой роли (Opus / Sonnet / Haiku) с обоснованием.
- **Два режима работы:**
  - **A — сабагенты:** всё в одном чате, Мастер сам запускает специалистов под задачу. Дёшево и полностью автоматически.
  - **B — отдельные чаты (Claude Code Desktop):** вы открываете N пустых чатов, Мастер сам их находит, переименовывает, выставляет модели, раздаёт роли и общается с ними.
- **Память проекта** в Markdown со ссылками `[[...]]`: откройте папку в Obsidian и получите граф решений, задач и отчётов.
- **Без ручного «вставь промпт после /clear»:** хук восстанавливает роль чата после очистки или сжатия контекста.

## Установка

```bash
git clone https://github.com/alekseevdenis1995-ai/mastermind ~/.claude/skills/mastermind
```

Windows (PowerShell):

```powershell
git clone https://github.com/alekseevdenis1995-ai/mastermind "$HOME\.claude\skills\mastermind"
```

Или скачайте ZIP и распакуйте в `~/.claude/skills/`, чтобы получилось `~/.claude/skills/mastermind/SKILL.md`.

**Нужно:** Claude Code, Python 3 (для хука). **Желательно:** скилл `llm-council` (без него используется встроенный консилиум). Режим B — только Claude Code Desktop.

## Запуск

Откройте Claude Code в пустой папке проекта и напишите:

```
/mastermind
```

или просто: «у меня идея проекта, собери команду».

## Что появится в проекте

```
TEAM_MANIFEST.md  PROJECT_PLAN.md  ARCHITECTURE.md  CLAUDE.md
team/        стартовые промпты Мастера и специалистов
memory/      контекст, состояние, решения, вопросы, идеи, задачи, отчёты, ADR
specs/       ТЗ и исходные материалы
.claude/     хук восстановления контекста
```

## Принцип

> **Bootstrap собирает команду. Мастер ведёт проект. Специалисты выполняют задачи Мастера. Память хранит состояние. Пользователь принимает решения.**

---

## English

**One command gives your project an AI team: a Master orchestrator, role-based specialists with the right model each, shared project memory, and an autonomous work loop in Claude Code.**

- **Input:** a ready spec (file/archive) or a raw idea, pressure-tested by a 5-advisor council and refined with you into a spec.
- **Team design:** the smallest effective team, clear ownership, Opus/Sonnet/Haiku per role.
- **Modes:** **A** — subagents inside one chat (cheap, fully automatic); **B** — real chats in Claude Code Desktop that the Master discovers, renames, assigns models and roles to, and messages directly.
- **Memory** as linked Markdown — open it in Obsidian for a graph of decisions, tasks and reports.
- **Context restore hook** — a cleared or compacted chat re-reads its role automatically.

**Install:** `git clone https://github.com/alekseevdenis1995-ai/mastermind ~/.claude/skills/mastermind` — then run `/mastermind` in an empty project folder. Requires Claude Code and Python 3; `llm-council` skill optional; mode B requires Claude Code Desktop.

## License

MIT
