# Formula Sheet Specification

Read this file when building or updating the formula/reference sheet. It covers the 3-view toggle, variable color-coding, KaTeX popup system, and card styling specific to the formula sheet.

## Formula Sheet Cards (distinct from chapter cards)

Formula sheet cards use a DIFFERENT design from chapter note cards to avoid repetitive color. No colored left border. Instead: a clean card with a subtle header bar containing the formula name, and a body area for the formula and details. The colored variables inside the formula ARE the visual interest.

```css
.fs-card {
  background: var(--surface);          /* theme-provided card surface */
  border-radius: 8px;
  border: 1px solid var(--border);
  overflow: visible; /* CRITICAL: never hidden — popups must not be clipped */
}
.fs-card .fs-top {
  padding: 6px 14px;
  background: var(--surface-alt);      /* theme-provided slightly contrasting header strip */
  border-bottom: 1px solid var(--border);
  border-radius: 8px 8px 0 0;
}
.fs-card .fs-name { font-weight: 700; color: var(--text); }
```

Every theme defines `--surface` (the card body color) and `--surface-alt` (a subtly different shade for headers/strips) on `:root`. Dark themes use semi-transparent whites at low opacity; light themes use semi-transparent blacks. Never hardcode a specific opacity or color here.

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

## Live Search Bar

Render a search input ABOVE the view-toggle row. Once a formula sheet has 30+ items, scrolling to find one mid-prep is painful — typed search is the difference between the sheet being useful or not.

```html
<input type="text" id="fs-search"
       placeholder="🔍  Jump to equation... (name, #number, or chapter)" />
```

Filter cards in real time against four signals: formula **name**, formula **number** (e.g. typing `#12`), **chapter** tag (e.g. typing `ch3`), and any keyword in the "when to use" or summary text. Cards expose number and chapter via `data-` attributes so the filter is fast and unambiguous:

```html
<div class="fs-card" data-num="12" data-ch="3" data-name="Polar Arc Length">…</div>
```

```js
document.getElementById('fs-search').addEventListener('input', e => {
  const q = e.target.value.toLowerCase().trim();
  document.querySelectorAll('.fs-card').forEach(card => {
    if (!q) { card.style.display = ''; return; }
    const hay = (card.dataset.name + ' #' + card.dataset.num + ' ch' + card.dataset.ch + ' ' + card.textContent).toLowerCase();
    card.style.display = hay.includes(q) ? '' : 'none';
  });
});
```

Search works across all 3 views — the toggle controls density, the search controls scope.

## On-Sheet vs Off-Sheet Tagging (when the instructor provides an exam formula sheet)

If the course has an official exam formula sheet (often the case in math/engineering courses), tag every card with its exam-sheet status. This lets the exam-prep pages tell the student which formulas they need to memorize vs which they get for free during the test.

```html
<div class="fs-card" data-num="12" data-ch="3" data-exam="on" data-exam-num="12">…</div>
<div class="fs-card" data-num="44" data-ch="7" data-exam="off">…</div>
```

Render a small badge on each card: `[Exam #12]` (theme's `def` accent) when on-sheet, `[Off-sheet]` (muted) when off. Also add a filter toggle: "Show: All / On exam sheet only / Off-sheet only" — useful in the final push before a test.

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

2. Each variable in the formula is wrapped with `\htmlData{t=description}{\color{HEX}{content}}` — where `HEX` is the resolved value of the appropriate theme variable category (`var(--vc-primary)`, `var(--vc-secondary)`, etc.). KaTeX's `\color{}` needs a literal hex, so the value is the theme's current resolved value, NOT a hardcoded constant. If the theme switches, the embedded hex must be regenerated.
```latex
\htmlData{t=v₁ — x-component of v}{\color{HEX_FROM_VC_PRIMARY}{v_1}}
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

## Color Legend — Category-Based, Not Per-Variable

A legend bar at the top of the formula sheet maps colors to **variable categories**, not to individual variables. Pick a category schema that fits the subject. Default schema slots (works for most engineering / math / physics):

| CSS variable | Category | Examples |
|---|---|---|
| `var(--vc-primary)` | Primary / x-direction | `x`, `vₓ`, `u`, `i` |
| `var(--vc-secondary)` | Secondary / y-direction | `y`, `v_y`, `j` |
| `var(--vc-tertiary)` | Tertiary / z-direction | `z`, `v_z`, `k` |
| `var(--vc-angle)` | Angles & sweeps | `θ`, `φ`, `α`, `ω` |
| `var(--vc-scale)` | Magnitudes & scale | `‖v‖`, `r`, `R`, `L` |
| `var(--vc-field)` | Fields & operators | `∇`, `F`, `E`, `B` |

**Concrete hex values come from the active theme, NOT this spec.** Each of the 30 themes provides its own 6-slot variable palette via CSS custom properties on `:root`. Theme designers pick hex values that are distinct from each other AND distinct from the theme's content-type accents (`--eq`, `--def`, `--tip`, `--der`, `--ex`, `--unit`) so the variable colors don't collide with the equation/definition/tip semantics in chapter notes.

Example theme block (for the active theme — every theme provides its own):
```css
:root {
  /* content-type accents — set by theme */
  --eq:  /* theme equation color */;
  --def: /* theme definition color */;
  /* …etc */

  /* variable palette — set by theme, distinct from content accents */
  --vc-primary:   /* theme value */;
  --vc-secondary: /* theme value */;
  --vc-tertiary:  /* theme value */;
  --vc-angle:     /* theme value */;
  --vc-scale:     /* theme value */;
  --vc-field:     /* theme value */;
}
```

The legend appears as a horizontal row of color-dot + label chips at the top, between the search bar and the view toggle. The dots read their color from the theme variables, so the same legend HTML works across all 30 themes. Adapt category *names* to the subject — stats might use Distribution Parameters / Test Statistics / Sample Stats; CS might use Inputs / State / Outputs. Adapt the *number* of slots too if the subject needs more or fewer than 6 — the schema is a default, not a contract.

This color-coding applies ONLY in the formula sheet. In chapter notes, variables use neutral pills below the formula instead.

## Grouping — By Chapter, Not One Flat List

Once the sheet exceeds ~10 formulas, browsing a flat list is painful. Group formulas by chapter using an `<h2>` header above each chapter's section, wrapping each chapter's cards in a `.fs-chapter` div for layout:

```html
<h2 class="fs-chapter-title">Ch 1 — Vectors</h2>
<div class="fs-chapter" data-ch="1">
  <div class="fs-card" id="fs-magnitude" data-num="1" data-ch="1" data-name="Magnitude" data-exam="on" data-exam-num="7">…</div>
  <div class="fs-card" id="fs-dot-product" data-num="2" data-ch="1" data-name="Dot Product" data-exam="on" data-exam-num="8">…</div>
</div>

<h2 class="fs-chapter-title">Ch 2 — Lines & Planes</h2>
<div class="fs-chapter" data-ch="2">…</div>
```

Style chapter headers with that chapter's title color (matches `progress.md` chapter palette). Sticky-position them so they pin to the top while you scroll within a chapter's section.

## Search Results — Dropdown, Not Filter

Replace the filter behavior with a **dropdown of matching results** that the user can click to jump to. Filtering hides cards (loses context); a dropdown lets the user keep the full sheet visible and just scroll-to-target.

```html
<div class="fs-search-wrap">
  <input type="text" id="fs-search" placeholder="🔍  Jump to equation... (name, #number, or chapter)" />
  <ul id="fs-results" hidden></ul>
</div>
```

```js
const cards = Array.from(document.querySelectorAll('.fs-card'));
const results = document.getElementById('fs-results');
document.getElementById('fs-search').addEventListener('input', e => {
  const q = e.target.value.toLowerCase().trim();
  results.innerHTML = '';
  if (!q) { results.hidden = true; return; }
  cards
    .filter(c => (c.dataset.name + ' #' + c.dataset.num + ' ch' + c.dataset.ch).toLowerCase().includes(q))
    .slice(0, 8)
    .forEach(c => {
      const li = document.createElement('li');
      li.textContent = `#${c.dataset.num} — ${c.dataset.name} (Ch ${c.dataset.ch})`;
      li.onclick = () => { c.scrollIntoView({behavior:'smooth', block:'center'}); c.classList.add('fs-flash'); setTimeout(()=>c.classList.remove('fs-flash'), 1500); results.hidden = true; e.target.value=''; };
      results.appendChild(li);
    });
  results.hidden = results.children.length === 0;
});
```

`.fs-flash` briefly highlights the target card with a fading outline in the theme's equation accent (`var(--eq)`) so the user's eye lands on it after the scroll. The hue comes from the theme — never hardcode yellow or any specific color.

## Numbered Badges — Display Prominently

Every formula card shows its number as a visible badge next to the name, not just as a `data-num` attribute. The badge is what the search dropdown matches and what the per-problem "📋 Formulas Needed" block (see `solution-pipeline.md`) anchors to.

```html
<div class="fs-name">Magnitude <span class="fs-num">#1</span></div>
```

Style `.fs-num` with the theme's equation accent color, small and subtle but legible.
