# Design quality — for every role that builds UI

Read before any task that builds or restyles UI. If a screen could belong to any product, it isn't done. The principle: the chrome stays quiet, the richness goes into one or two moments of content. Scaffold copies this file to `specs/design-quality.md` in the project.

Condensed and rewritten from [unslop](https://github.com/heydamir/unslop) by Damir Sokolovsky ([@heydamir](https://x.com/heydamir)), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — this file stays under that license, keep the credit in copies — plus Anthropic's `frontend-design`. For depth, use these if installed (`npx skills add <repo>`): [heydamir/unslop](https://github.com/heydamir/unslop) (full redline pass over an existing screen), [emilkowalski/skills](https://github.com/emilkowalski/skills) (animation, MIT), [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (colors, layout, polish, MIT).

## 1. Direction — once per project, before the first screen
Five lines, from the ТЗ and the product, never from trends:
- **Product:** what it does, for whom.
- **Character:** 2–3 concrete words. Banned, because they fit anything: clean, modern, sleek, minimal, premium.
- **World:** the place or material the product belongs to. It sets the neutral tint, the accent and the imagery.
- **Moments:** the 1–2 spots that get rich color and detail, taken from what the product shows (a carefully drawn chart, a rendered object, real photos).
- **Signature:** one small detail only this product would have, used consistently.

A real brand (logo, color, typeface) is kept and built around; a violet gradient with sparkles is not a brand. The direction goes to MASTER and becomes a D-NNN in `memory/DECISIONS.md`. Later UI tasks follow it; nobody invents a new one per screen.

**Existing UI:** a mostly designed screen gets only its signs fixed, in its own palette and type. A good screen stays as it is, with at most 2–3 suggestions in the report. Never restyle for the sake of change.

## 2. Signs of slop → what replaces them
- **Surfaces:** hue-to-hue gradients (especially purple→blue), gradient text, colored glows and shadows, blurred blobs, neon borders, glass cards → one neutral ramp; depth from surface steps and hairlines.
- **Stock looks:** cream + serif + terracotta; near-black + one acid accent; identical rounded cards with one radius and one soft grey shadow → what the direction says.
- **Type:** 700–900 headings, all-caps tracked labels, many sizes, mixed number formats, tight tracking on small text, italics for emphasis → size and color carry hierarchy, sentence case, tabular numbers in one format.
- **Icons:** emoji as icons or label decoration, sparkles for anything AI, mixed sizes and colors → one line set, or none.
- **Spacing:** one-off values like `mt-[13px]`, uneven rows or sibling padding, groups closer to their neighbours than to their own items → the grid in §4.
- **Copy:** greeting headlines, `!`, hype (supercharge, seamless, unlock, magic), "AI-powered" everywhere, a change with no baseline, periods on labels, `123,456` or `[X]` as data → plain words with this product's nouns, "+12% vs last month", plausible data. Claims nobody can check ("Trusted by 10,000+") get confirmed by the user or removed.
- **Components:** glowing pills, `New ✨` / `PRO` badges, everything a pill, a sparkline in every stat card, rows of equal cards, rainbow charts, "01/02/03" on non-sequences, one accented headline word, trailing arrows on every link, labels above content that needs none → quiet text, varied sizes, one lead element.
- **Hero:** a badge above the headline, everything stacked and centered, 3+ buttons, avatar rows, big number + stats + gradient, a headline that fits any product → a split, or text over a large product view; one primary and at most one secondary action.
- **Visuals:** glossy orbs, nebulas, robots, glowing brains, text baked into images, a visual on every section, labeled empty placeholders → the product itself with plausible data, or one real object from the world.
- **Motion:** looping pulses on things that aren't live, `transition-all`, `hover:scale` on cards, bounce, fade-and-slide on every section, parallax → motion answers user action; at most one entrance on load.

## 3. Order of work
Spacing → color → icons → copy → type → layout → details → visuals → motion. Finish a layer across the whole screen before the next: rhythm changes how everything else reads, copy length decides type size and layout, visuals and motion must fit a screen that already works. Sketch a short token set + ASCII wireframe before code.

## 4. Starting values
A good existing design system wins; the direction may move these.
- **Spacing:** 4px grid. Rows 32–36 (touch 40–44), card padding 20–24, page edge 24–32, sections 32–64 (landing 80–128). Gaps inside a group are smaller than between groups. Equal things get equal sizes.
- **Color:** build in OKLCH, a small named palette. One neutral ramp: apps stay near-grey so content carries the color, landings may tint further toward the world. Three text roles. One accent on a few percent of the screen, from the brand or the world, never by habit. Contrast AA (4.5:1). Semantic colors only carry meaning. Hairlines: text color at 6–10%.
- **Type:** 1 family + at most 1 partner, chosen for the character; a few sizes; weights 400/500, 600 rarely; lines ≤ ~80 chars; negative tracking only on large display text.
- **Shape:** controls 8–10, cards 12–16, panels 14–20; inner radius = outer − padding, minimum 4.
- **Icons:** one set (Lucide / Phosphor), SVG, 16–18px, stroke 1.5, `currentColor` of the text role.
- **Data:** chart type follows the data; one main chart is clearly the largest, others are smaller and different in kind; the accent marks the one thing that matters; a stat card is a label, a number and a change.
- **Motion:** one ease-out curve; 120–180ms feedback, 160–220ms menus, 300–500ms entrances; animate only transform, opacity and color; honor `prefers-reduced-motion`.

## 5. Don't
Change features, content or section order unless the task says so. Invent features, claims or data. Replace old decoration with a new trend (glass, grain, neon, bento). Give every product the same look.

## 6. Before PASS
1. Floor: responsive, visible focus, all states (empty / loading / error), a11y.
2. Render the screen and look at it if the environment allows; code alone hides most of this.
3. Go through §2 and say in the report what you found and changed.
4. Template test: swap in a competitor's name. If the screen still fits, push the copy, the moments and the signature harder.
5. Spend boldness in one place; remove one element before finishing.
