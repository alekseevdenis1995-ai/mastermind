# Security audit — opt-in, on request

Run only when the user asks ("проверь безопасность", "security audit") or the audit verdict flags secrets / auth / untrusted input. Adapted from [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) (MIT). For a deep multi-agent audit of one repo, suggest installing that skill: `npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit`.

## Phases (each by a fresh, isolated agent where subagents exist)

1. **Recon.** Map architecture, trust boundaries and input surfaces (HTTP, CLI, files, queues, env, third-party data). Write `memory/security/architecture.md` and `memory/security/coverage.md` — a list of units (module / endpoint / parser) with status `todo | hunted | clean`.
2. **Hunt.** One hunter per coverage unit, read-only. Pick attack classes by target: web/auth (injection, authz, SSRF, sessions), secrets, supply chain (deps, install scripts, CI), data isolation (tenants), resource exhaustion, AI/LLM (prompt injection, tool abuse), memory safety (native code). Output: candidates with file:line, attacker input, impact.
3. **Disprove.** A fresh verifier gets one candidate and tries to prove it is NOT exploitable (reachability, guards upstream, config). Survivors only.
4. **Record.** `memory/security/findings.md`, each finding in one status:
   - `confirmed` — traced source → sink, or reproduced;
   - `needs_validation` — plausible, but not executed;
   - `rejected` — with the reason it fails.
5. **Re-check claims.** A second fresh agent re-reads the cited lines of every `confirmed` finding. Drop what doesn't match the code.
6. **Report.** Short list sorted by severity: what, where, fix. Never print secret values — path only.

## Rules

- **Never run target code outside an OS-level sandbox** (container / VM). No sandbox → findings stay `needs_validation`; say so.
- Hunters don't see each other's candidates (no anchoring). Re-runs reuse `coverage.md` and only revisit changed or `todo` units.
- Fixes are separate tasks routed through the MASTER to the owner of that area; the audit itself changes no code.
- Cost: roughly one agent per coverage unit plus one verifier per candidate. For a small project use one pass: recon → hunt (one agent) → disprove.
