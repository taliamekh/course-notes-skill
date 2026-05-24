# Formula Sheet Specification

Read this file when building or updating the formula/reference sheet. It covers the 3-view toggle, variable color-coding, KaTeX popup system, and card styling specific to the formula sheet.

## Formula Sheet Cards (distinct from chapter cards)

Formula sheet cards use a DIFFERENT design from chapter note cards to avoid repetitive color. No colored left border. Instead: a clean card with a subtle header bar containing the formula name, and a body area for the formula and details. The colored variables inside the formula ARE the visual interest.

```css
.fs-card {
  background: rgba(255,255,255,.6);
  border-radius: 8px;
  border: 1px solid var(--border);
  overflow: visible; /* CRITICAL: never hidden — popups must not be clipped */
}
.fs-card .fs-top {
  padding: 6px 14px;
  background: rgba(0,0,0,.03);
  border-bottom: 1px solid var(--border);
  border-radius: 8px 8px 0 0;
}
.fs-card .fs-name { font-weight: 700; color: var(--text); }
```

No "EQ" / "TEST" badges. No variable pills below formulas (popups handle this). Chapter notes keep their neutral pills.

## Each Reference Item Is a Mini-Lesson

Each item (equation, theorem, algorithm, framework) includes:
1. **Statement / Formula** — KaTeX or code block
2. **Plain-english explanation** — what it MEANS physically/conceptually
3. **Origin** — derivation hint, proof sketch, or context
4. **When to use** — scenarios, signal words in problems
5. **When NOT to use** — misapplications, limitations, assumptions required
6. **Use case examples** — 1-2 one-liner problem → method mappings
7. **Interactive pills** — every variable in every formula gets a pill (symbol + name + unit), even if the same variable appeared in a previous formula. Repetition is intentional.

## Formula Sheet 3-View Toggle

The formula sheet page has 3 toggleable views, controlled by a row of buttons at the top:

1. **Full Detail** (default) — the complete cards: formula with color-coded clickable variables, plain-english explanation, when to use / not use, origin.
2. **Quick Reference** — condensed cards: formula displayed prominently, a short 1-2 sentence summary to the right. No when-to-use blocks, no origin.
3. **Equations Only** — compact vertical list: just the formula name and the KaTeX equation. No explanations. Maximum density for quick scanning.

All three views show the same formulas — just at different detail levels. Implement with JS toggling CSS classes or data attributes. The active button is visually highlighted in the equation accent color.

## Variable Color-Coding (formula sheet only)

In the formula/reference sheet, every variable within a displayed formula is individually color-coded. Each distinct variable gets its own color from a theme-specific variable palette. This palette is COMPLETELY SEPARATE from the 6 content-type colors — none of the variable colors should match equation/definition/tip/derivation/example/unit accent colors. The palette needs to support potentially 20+ distinct variable colors that all look good together on the theme's background.

### Implementation — KaTeX `\htmlData` approach

1. KaTeX MUST be rendered with `trust: true, strict: false` — both options are required for HTML extensions:
```js
renderMathInElement(el, {
  delimiters: [{left:"\\[",right:"\\]",display:true},{left:"\\(",right:"\\)",display:false}],
  throwOnError: false, trust: true, strict: false
});
```

2. Each variable in the formula is wrapped with `\htmlData{t=description}{\color{#HEX}{content}}`:
```latex
\htmlData{t=v₁ — x-component of v}{\color{#D45D00}{v_1}}
```
This renders as `<span data-t="v₁ — x-component of v"><span style="color:...">v₁</span></span>`.

3. Descriptions are SPECIFIC to each variable in each formula — not generic. "x-component of v" not "vector v or components". Format: `symbol — explanation`.

## Popup Implementation — Body-Level Fixed Div (CRITICAL)

The popup MUST be a single `<div id="varpop">` appended to `<body>` and positioned with `position: fixed` using `getBoundingClientRect()`. NEVER use child tooltips appended inside the variable span — they WILL be clipped by parent containers with `overflow: auto` (formula containers need overflow-x:auto for responsive equations, and CSS spec forces overflow-y:auto when overflow-x is set).

```js
// On variable click:
var pop = document.getElementById('varpop');
var rect = el.getBoundingClientRect();
pop.style.display = 'block';
pop.style.left = (rect.left + rect.width/2 - pop.offsetWidth/2) + 'px';
pop.style.top = (rect.top - pop.offsetHeight - 10) + 'px';
```

**Symbol display in popup:** Use `el.innerHTML` wrapped in KaTeX CSS context so it renders identically to the formula:
```js
var symHtml = '<span class="katex"><span class="katex-html" aria-hidden="true"><span class="base">' + el.innerHTML + '</span></span></span>';
```
Never use `textContent` (loses formatting) or `cloneNode` (breaks KaTeX positioning context).

## Click Targets — KaTeX Overlay Elements Block Clicks

KaTeX renders fraction bars (`.frac-line`), square root lines (`.sqrt-sign`, `.sqrt-line`), and other decorative elements as positioned spans that sit ON TOP of variables. These must be made click-through:

```css
#formulas .katex .frac-line,
#formulas .katex .sqrt-sign,
#formulas .katex .sqrt-line,
#formulas .katex .overline-line,
#formulas .katex .svg-align,
#formulas .katex .hide-tail,
#formulas .katex .rule { pointer-events: none; }

.vc {
  cursor: pointer;
  padding: 6px 3px; margin: -6px -3px; /* expand click target */
  display: inline-block;
  position: relative; z-index: 2; pointer-events: auto;
}
```

## Color Legend

A legend bar at the top of the formula sheet shows each variable color as a dot with its meaning.

This color-coding applies ONLY in the formula sheet. In chapter notes, variables use neutral pills below the formula instead.
