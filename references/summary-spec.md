# Summary Page Specification

Read this file when building or updating the course summary page.

## Overview

The summary page is INCREMENTALLY UPDATED — it grows with each chapter. It is never empty and never "generated after all chapters." Even if only Ch1 is done, it shows Ch1's summary.

## Stat Cards

**Stat cards** at the top: reference items count, chapters completed, examples count, assignments count — updated every time content is added.

## Per-Chapter Summaries — Concept-Map + What/Why/How Format

Each chapter is added as it's completed; pending chapters shown as muted placeholders.

Structure for each chapter summary:

1. **One-line chapter overview** — a single sentence capturing the chapter's purpose in the course arc.

2. **Topic clusters** — group related concepts into named clusters (e.g. "Vector Products" containing dot product, cross product, triple product). Each cluster gets:
   - **What:** one sentence defining the concept or operation.
   - **Why:** one sentence on why it matters — geometric meaning, physical interpretation, or what it unlocks.
   - **How:** the key formula or computation step, kept to one line. Use inline LaTeX.
   - **Trap:** one common mistake or misconception (optional — include only when there's a genuine, frequent pitfall).

3. **Cross-chapter connections** — 2-3 bullets showing how this chapter's ideas link to previous or upcoming chapters (e.g. "Dot product → projections in Ch3 → work integrals in Ch6").

**NEVER write summaries as dense paragraph walls.** Each concept must be its own visible, scannable item. If a summary section looks like a single block of text listing terms with commas, it is wrong — break it into the cluster structure above.

## Quick Reference Table

Sits at the bottom of the summary page, AFTER all chapter summaries. A compact `Test | Formula | Result` table of the most useful quick-check tests and shortcuts across all chapters. Expanded incrementally as each chapter is added (e.g. Ch1 adds perpendicularity/parallelism/coplanarity tests, Ch2 might add line-plane intersection tests, etc.). Keep it to the highest-value "is this true? → plug in formula → yes/no" items only.

## Styling

Use the course theme's accent colors to visually distinguish cluster headings. The What/Why/How/Trap labels on each line MUST each be a different color to stand out — use `<dt class="wh-what">`, `<dt class="wh-why">`, `<dt class="wh-how">`, `<dt class="wh-trap">` with corresponding CSS using a deep-to-bright gradient palette (e.g. What = #142850 dark navy, Why = #27496D steel blue, How = #0C7B93 teal, Trap = #00A8CC bright cyan — adapt to the theme's palette). 

All equations (KaTeX) inside summary clusters MUST be highlighted with a red highlighter effect:

```css
.cluster .katex{color:var(--eq)!important;background:rgba(139,26,26,.1);padding:1px 4px;border-radius:3px;}
```

Every formula from the formula sheet must appear in at least one cluster's How line — cross-check before finalizing. Keep each What/Why/How line short enough to read without horizontal scrolling.

## Equations in Summary — Red Highlighter Effect

Not just colored text, but a visible background highlight like a marker on paper:

```css
.cluster .katex{color:var(--eq)!important;background:rgba(139,26,26,.1);padding:1px 4px;border-radius:3px;}
```
