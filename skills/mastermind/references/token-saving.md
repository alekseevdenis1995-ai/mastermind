# Token saving — optional

- **Terminal output.** [tokenjuice](https://github.com/vincentkoc/tokenjuice) (MIT, Node) compacts noisy command output (tests, git, docker, rg) with deterministic rules before it reaches the agent's context — no LLM involved; `--raw` bypasses it. Offer once at hand-off if `node` exists: `npx tokenjuice install claude-code` (other hosts: `tokenjuice install <host>`, then `tokenjuice doctor`). It edits the user's hook config, so install only on a clear "да". Complements the PreCompact/restore hooks: they preserve context, this shrinks what enters it.
- **Without it,** the specialist rule is enough: run tests/builds with output limited to failures and a tail (`| tail -40`, `--quiet`, `-x`), never paste full logs into reports.
- **Don't** put this file's content in start prompts; it is read once at Phase 3.
