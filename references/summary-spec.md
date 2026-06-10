# Summary Page Specification

Read this file when building or updating the course summary page.

## Overview

The summary page is INCREMENTALLY UPDATED — it grows with each chapter. It is never empty and never "generated after all chapters." Even if only Ch1 is done, it shows Ch1's summary.

## Stat Cards

**Stat cards** at the top: reference items count, chapters completed, examples count, assignments count — updated every time content is added.

## Section Order (top to bottom)

1. Stat cards
2. **Decision trees** — interactive flowcharts for "which tool / which theorem / which method"
3. **Per-chapter cards** — three-part structure (Key Ideas / When to Use What / Traps)
4. **Quick Reference Table** — sortable by problem type across all chapters

The summary is built for **practice-problem lookup**, not for re-reading the course. The decision trees come first because that's how a student under time pressure actually uses the summary: "I see this problem — which tool applies?"

## Decision Trees — Always At Top

For subjects where problem-solving has clear method selection (most engineering / math / physics / stats):

Each tree is a card with a question header and nested branches.

```html
<div class="decision-tree">
  <h3>Which Tool Do I Use?</h3>
  <div class="tree">
    <div class="branch">
      <strong>Single variable, definite bounds?</strong>
      → standard integral (Ch 5)
    </div>
    <div class="branch">
      <strong>Vector field along a curve?</strong>
      → line integral (Ch 6)
      <div class="sub-branch">
        <strong>Closed curve, F = ∇f?</strong> → FTCLI gives zero
      </div>
    </div>
    <div class="branch">
      <strong>Surface flux of F?</strong>
      → surface integral (Ch 7) — consider Stokes' or Divergence
    </div>
  </div>
</div>
```

Typical trees per subject:
- **Math (calc):** Which integral type? Which theorem (Green's / Stokes' / Divergence)? Which optimization method (unconstrained / constrained / bounded)?
- **Dynamics:** Which coordinate system (rectangular / n-t / r-θ)? Energy or momentum?
- **Stats:** Which hypothesis test? Which distribution?
- **CS:** Which data structure? Which algorithm family?

Add trees incrementally — by the final chapter you should have ~3 decision trees covering the major problem-type splits.

## Per-Chapter Cards — Three-Part Structure

Each chapter is added as it's completed. Pending chapters shown as muted placeholders. Each card has a colored left border in the chapter's title color.

```html
<div class="card-bracket" style="border-left:3.5px solid var(--ch1-title);">
  <div class="eq-name" style="color:var(--ch1-title);">Ch 1 — Vectors</div>

  <p><strong style="color:var(--ch1-title)">Key ideas:</strong></p>
  <ul>
    <li>→ Vectors have magnitude AND direction</li>
    <li>→ Dot product measures alignment; cross product measures perpendicularity</li>
    <li>→ Vector projection isolates one direction's contribution</li>
  </ul>

  <p><strong style="color:var(--ch1-title)">When to use what:</strong></p>
  <ul>
    <li>→ Need an angle? — dot product: \(\cos\theta = \frac{\vec u\cdot\vec v}{\|\vec u\|\|\vec v\|}\)</li>
    <li>→ Need a perpendicular vector? — cross product: \(\vec u \times \vec v\)</li>
    <li>→ Need parallel test? — cross product = 0</li>
    <li>→ Need coplanarity? — scalar triple product = 0</li>
  </ul>

  <p><strong style="color:var(--ch1-title)">⚠ Traps:</strong></p>
  <ol>
    <li>Cross product is NOT commutative: \(\vec u\times\vec v = -\vec v\times\vec u\)</li>
    <li>Dot product result is a scalar; cross product result is a vector</li>
    <li>Don't forget magnitude in projection denominator</li>
  </ol>
</div>
```

**Three sections per chapter card:**
- **Key ideas:** 3–4 conceptual anchors that capture the chapter's *worldview*. Not formulas — ideas. Use → as bullet markers.
- **When to use what:** 6–8 decision rules in "Need X? — Method Y" format, each with the key formula inline. This is the most-used part of the card during prep.
- **⚠ Traps:** 3–4 common mistakes / misconceptions. Numbered list with warning icon.

**No dense paragraphs.** Each item must be its own scannable line.

## Quick Reference Table — Sortable By Problem Type

Sits at the bottom, AFTER chapter cards. Compact table organized by **problem type**, with color-coded left borders showing which chapter each row belongs to. This is the "I can't remember which formula" rescue table.

```html
<table class="quick-ref">
  <thead><tr><th>Problem Type</th><th>Formula / Method</th><th>Key Detail</th></tr></thead>
  <tbody>
    <tr style="border-left:3px solid var(--ch1-title)">
      <td>Perpendicular?</td>
      <td>\(\vec u\cdot\vec v = 0\)</td>
      <td>⊥ test</td>
    </tr>
    <tr style="border-left:3px solid var(--ch1-title)">
      <td>Parallel?</td>
      <td>\(\vec u\times\vec v = 0\)</td>
      <td>∥ test</td>
    </tr>
    <tr style="border-left:3px solid var(--ch2-title)">
      <td>Line through two points</td>
      <td>\(\vec r = \vec r_0 + t(\vec r_1 - \vec r_0)\)</td>
      <td>parametric form</td>
    </tr>
  </tbody>
</table>
```

Grouped by problem type (NOT by chapter) so a student facing an unfamiliar problem can scan by what they're being asked, not where it came from. The chapter color border preserves the chapter origin without ordering by it.

Keep it to the highest-value "is this true? → plug in formula → yes/no" or "I need X → use Y" items only. Aim for ~15-25 rows by the end of the course.

## Styling

Use the course theme's accent slots to visually distinguish the What/Why/How/Trap labels — each MUST be a different color to stand out. Use `<dt class="wh-what">`, `<dt class="wh-why">`, `<dt class="wh-how">`, `<dt class="wh-trap">` mapped to four of the theme's content-type accents:

```css
.wh-what { color: var(--def); }   /* definition accent */
.wh-why  { color: var(--der); }   /* derivation accent */
.wh-how  { color: var(--eq);  }   /* equation accent */
.wh-trap { color: var(--tip); }   /* tip accent */
```

The exact hex values come from the active theme. Never hardcode hex codes in the spec — themes are customizable.

Every formula from the formula sheet must appear in at least one cluster's How line — cross-check before finalizing. Keep each What/Why/How line short enough to read without horizontal scrolling.

## Equations in Summary — Highlighter Effect

Equations inside summary clusters get a subtle background highlight (like a marker on paper) so they pop without needing extra color:

```css
.cluster .katex {
  color: var(--eq) !important;
  background: var(--eq-highlight);    /* theme provides a translucent tint of --eq */
  padding: 1px 4px;
  border-radius: 3px;
}
```

Each theme defines `--eq-highlight` as a low-opacity version of its equation accent (typically the same hue at 8–12% alpha). The hue follows the theme; the spec only mandates that there IS a highlight.
