# Team presets

Starting points for protocol §5. Pick the closest, then add, merge or drop roles to fit the ТЗ. MASTER (HEAVY) is always there and is not listed. Tiers map to models via `runtimes.md` §3.

| Project type | Roles (tier) | Merge when small | Typical checks |
|---|---|---|---|
| **Web app / SaaS** | 01 TECH — backend, DB, API, deploy (STANDARD) · 02 FRONTEND — UI, state, a11y (STANDARD) · 03 QA — e2e, regressions (LIGHT) | FRONTEND into TECH for ≤5 screens | test, lint, typecheck, build |
| **Landing / marketing site** | 01 WEB — layout, SEO, forms (STANDARD) · 02 CONTENT — copy, structure (STANDARD) | CONTENT into WEB if copy is given | build, lighthouse, link check |
| **Bot (Telegram, Discord…)** | 01 TECH — handlers, DB, integrations, deploy (STANDARD) · 02 CONTENT — dialogs, texts (LIGHT) | CONTENT into TECH for simple bots | test, lint |
| **Mobile app** | 01 TECH — backend/API (STANDARD) · 02 MOBILE — screens, platform APIs (STANDARD) · 03 DESIGN — UX, UI kit (STANDARD) · 04 QA (LIGHT) | DESIGN into MOBILE if a design is given; no TECH if no backend | test, lint, build per platform |
| **Game** | 01 GAMEPLAY — mechanics, balance (HEAVY) · 02 TECH — engine, systems, build (STANDARD) · 03 ART — sprites, UI, VFX specs (STANDARD) · 04 QA (LIGHT) | ART into GAMEPLAY for prototypes; add ECONOMY for F2P | build, playtest checklist |
| **Data / parser / automation** | 01 TECH — pipeline, storage, scheduling (STANDARD) · 02 DATA — sources, schemas, quality (STANDARD) | one TECH role for a single script | test, sample run, data checks |
| **AI / LLM product** | 01 TECH — app, API, infra (STANDARD) · 02 AI — prompts, evals, model choice (HEAVY) · 03 QA — eval runs, regressions (LIGHT) | QA into AI early on | test, eval suite |
| **Library / CLI tool** | 01 TECH — code, API design (STANDARD) · 02 DOCS — README, examples (LIGHT) | DOCS into TECH | test, lint, typecheck |

Rules:
- ≤3 specialists is normal for an MVP. More needs a reason in TEAM_MANIFEST.
- Add SECURITY only for payments, personal data or auth-heavy products; add DESIGN only when no design exists and UX matters.
- A QA role on LIGHT is cheap insurance once there is more than one implementer.
