# Idea → ТЗ

Goal: turn a raw idea into a ТЗ the user has explicitly approved, without inventing requirements.

## 1. Capture

Let the user describe the idea freely. Then ask at most 5 short questions that most change the product — typically: who it's for, platform, the one core scenario, monetization/goal, hard constraints (deadline, budget, stack). Accept "не знаю" — it becomes UNKNOWN.

## 2. Council

Invoke the `llm-council` skill (Skill tool, name `llm-council`) with a framed question, for example:

> Pressure-test this product idea and shape it into an MVP. Idea: <idea>. Known: <answers>. Unknown: <list>. I need: the strongest version of the concept, the MVP scope (must / should / later), the riskiest assumptions, and what to cut.

The council runs its advisors and returns a synthesis. Keep its verdict; don't re-run it silently.

**Fallback if `llm-council` isn't installed:** spawn 3–5 subagents in parallel, each with one lens — *Skeptic* (why this fails), *User advocate* (what the user actually needs), *Builder* (the simplest thing that works technically), *Business* (value, monetization, market), optionally *Wildcard* (a bolder angle). Each returns ≤200 words. You synthesize: agreements, clashes, recommendation.

## 3. Sketch

Show the user a compact sketch (fits on one screen):

```
## <Рабочее название>
Суть: <1–2 предложения>
Для кого: …
Платформа: …
Ключевой сценарий: …
MVP — must: … / should: … / later: …
Риски: …
Неизвестно: …
Консилиум сказал: <2–3 главных тезиса, включая несогласия>

Дальше: (1) подтвердить  (2) поправить — напишите что  (3) ещё раунд консилиума по <вопрос>
```

Loop until the user confirms. Another council round is worth it only for a specific open question, not the whole idea again.

## 4. Write the ТЗ

Write `<project>/specs/TZ.md`: vision, audience, platform, scenarios, MVP scope (must/should/later), non-functional requirements, constraints, KNOWN/ASSUMED/UNKNOWN, open questions, council summary. Mark anything the user didn't confirm as ASSUMED. Then continue to Phase 2 of SKILL.md.
