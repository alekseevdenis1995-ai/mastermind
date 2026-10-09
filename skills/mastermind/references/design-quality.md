# Design quality — for FRONTEND / DESIGN / MOBILE roles

Read when the task builds or restyles UI. Distilled from Anthropic's `frontend-design` skill; for depth, use the skills below if installed (`npx skills add <repo>`): [emilkowalski/skills](https://github.com/emilkowalski/skills) (animation, MIT), [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (colors, layout, polish, MIT), Anthropic `frontend-design` (anti-generic).

## Anti-slop: don't ship the default
- Stock look: cream + serif + terracotta, or near-black + one acid accent; identical rounded cards with one radius and one soft grey shadow; gradient washes as decoration.
- Template chrome: all-caps tracked eyebrows, "01/02/03" markers on non-sequences, accenting one headline word, trailing arrows on every link, labels above content that needs none.
- Default hero (big number + small label + stats + gradient), fade-and-slide-up on every section, hover effects on every card.

## Do
- **Type:** 1–2 families chosen for the brief, a deliberate scale, lines ≤ ~80 chars.
- **Color:** a small named palette derived from the subject; build in OKLCH, check contrast (AA minimum); no stock accent by habit.
- **Layout:** group, align, order by reading flow; borders and dividers carry information, not decoration; decide alignment on purpose; sketch a short token set + ASCII wireframe before code.
- **Motion:** one orchestrated moment (load/reveal); elsewhere motion only answers user action. Enter = ease-out; never animate layout properties when transform/opacity will do; honor `prefers-reduced-motion`.
- **Icons:** one set (Lucide / Phosphor), SVG, one size grid and stroke width, `currentColor`.
- **Restraint:** spend boldness in one place; remove one element before finishing.
- **Floor:** responsive, visible focus, all states (empty / loading / error), a11y.

Before PASS, the role reviews its own result against the "don't ship the default" list and says what it changed.
