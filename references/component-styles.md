# Component Styles Reference

Read this file when generating or editing HTML output — it contains the definitive CSS for all visual components.

## Menu / Sidebar Specification

**Location:** Left side of the viewport, full height.

**Dimensions:** Width approximately 168px. Menu item font size: 14px.

**Font:** All sidebar text (header and items) uses the chosen theme font — system font is only used for tiny metadata like pill labels and percentage indicators.

**Header:** "Contents" in the theme font, uppercase, letter-spaced (~1.8px). Color: the theme's `mt` (muted text) value. NOT the active accent color.

**Toggle:** The toggle arrow lives inside the sidebar header row, next to the "Contents" label, as part of the same flex container. Shows ◀ when open. When the sidebar is closed, a small floating ▶ button appears at the top-left of the content area to reopen it.

**Colors — use the Theme Menu & UI Specs table in `references/themes.md`.** Look up the theme by name. Set `--sidebar-bg` to `sb`, `--sidebar-text` to `mt`, `--menu-active` to `ma`. The `ma` value is the STANDARD theme accent — it does NOT change when a user customizes content colors.

- Active item: text `ma`, background `ma` at ~8% opacity, glow `box-shadow: 0 0 8px {ma at 12%}, inset 0 0 0 1px {ma at 10%}`
- Inactive item: text `mt`
- "Contents" header: `mt`
- Hover: `rgba(0,0,0,.05)` background (light themes) or `rgba(255,255,255,.05)` (dark)

**Pending items — NEVER use opacity.** Use a lighter color than `mt` instead (e.g. `#7A7A70` when `mt` is `#5A5A50`). Once content is added, switch to `mt`.

**Separators:** Thin 1px horizontal lines in the theme's border color between logical groups:
- Group 1: Chapters / Lectures / Modules
- Group 2: Formula/Reference Sheet
- Group 3: Test/Midterm Prep sections + Final Prep
- Group 4: Summary + Progress

**Behavior:** Clicking a menu item switches the visible page and scrolls to top. Only one page is visible at a time.

## Card & Component Styling

**Cards are for KEY content that needs to stand out — not everything.** The majority of chapter notes are regular prose text: explanations, context, intuition, transitions between topics, setup for examples. This prose has NO colored styling — it uses the theme's normal text color on the page background, just like handwritten notes on paper. Colored cards are reserved for content that a student would highlight, box, or star in their own notes:

- **Equation cards** — named formulas and their variable pills
- **Definition cards** — formal definitions of new terms/concepts
- **Tip cards** — exam warnings, key insights, common mistakes
- **Derivation cards** — proof steps, derivation chains
- **Example cards** — worked problems with collapsible solutions

Everything else (introductions, paragraph explanations, connecting text, context, "here's why this matters", transitions) is plain prose.

### Chapter Note Cards

Chapter cards use `border-left: 3.5px solid {accent-color}` directly on the card element with `border-radius: 6px`. This matches the theme preview's `.ec` class. Do NOT use a `::before` pseudo-element or SVG path — a simple `border-left` with the card's own `border-radius` creates the correct visual. Each card type sets its accent via a CSS variable `--bracket-c`.

```css
.card-bracket {
  background: rgba(255,255,255,.5);
  border-radius: 6px;
  padding: 12px 16px 10px 14px;
  border: 1px solid var(--border);
  border-left: 3.5px solid var(--bracket-c, var(--eq));
}
.eq-card  { --bracket-c: var(--eq); }
.def-card { --bracket-c: var(--def); }
.tip-card { --bracket-c: var(--tip); }
.drv-card { --bracket-c: var(--deriv); }
.ex-card  { --bracket-c: var(--example); }
```

**No type labels.** Cards do NOT have "EQUATION" / "DEFINITION" labels. The colored border identifies the type. The card title (e.g. "Work-Energy Theorem") is styled in the card's accent color.

**Title underline:** Matches the title's accent color, not the generic border color.

**Tip labels:** Prefixed with a filled star: "★ Tip", "★ Exam Warning", "★ Key Insight".

### Variable Pills (chapter notes only)

Pills appear below formulas in chapter notes to explain variables. They match the theme preview's `.vpi` style:

```css
.pill {
  font-size: 12px;
  color: rgba(0,0,0,.50);
  background: rgba(0,0,0,.02);
  border: 1px solid rgba(0,0,0,.10);
  border-radius: 4px;
  padding: 2px 8px;
}
```

No heavy borders, no dark backgrounds. For dark themes, invert: `background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.10); color: rgba(255,255,255,.55);`

## Chapter Title Colors

Each chapter gets its own `--chN-title` CSS variable (e.g. `--ch1-title:#03346E`). When the user provides a chapter title color, apply it to ALL FIVE locations:

1. The chapter's `<h3>` heading in the **summary** page
2. The chapter's **concept cluster titles** (`.cluster-title`) in the summary — all clusters for that chapter use the same title color
3. The chapter's `<h1>`, `page-title`, and section `<h2>` headings in the **notes** page via `#chN h2{color:var(--chN-title);}`
4. The chapter's `<h2>` heading in the **formula sheet**
5. The **formula card titles** (`.fs-name`) for that chapter's cards — wrap each chapter's formula cards in `<div class="fs-chapter" style="--fs-ch-title:var(--chN-title)">` and use `.fs-chapter .fs-card .fs-name{color:var(--fs-ch-title);}`

Pending/empty chapters use `var(--muted)`.

## Bold Text Inside Content Cards

Bold (`<strong>`) text within each card type MUST inherit the card's accent color:

```css
.def-card strong{color:var(--def);}
.tip-card strong{color:var(--tip);}
.ex-card strong{color:var(--example);}
.drv-card strong{color:var(--deriv);}
.eq-card strong{color:var(--eq);}
```

This makes bolded terms inside definitions match the left border color of the card.

## HTML Generation Rules

1. Always load: KaTeX (cdnjs), chosen theme font (Google Fonts)
2. For CS: also load Prism.js for syntax highlighting
3. Chosen theme palette exclusively (see `references/theme.md` for component templates, substitute chosen theme colors)
4. KaTeX: `\( inline \)` and `\[ display \]`. Render with `trust: true, strict: false` (required for `\htmlData` in formula sheet)
5. Interactive pills (click to expand), collapsible solutions/examples
6. Fixed sidebar (left, full-course view) — no separate top bar
7. Embedded images in `.figure-box` containers with captions
8. SVG diagrams inline using theme colors
9. Sections as `<section id="{name}">` for anchor nav
10. Progress checkboxes persist via localStorage keyed by course name
11. Sidebar is DYNAMIC — only shows sections relevant to course config
12. For notebook-style themes (7, 8, 9): add CSS background patterns with `background-attachment: local` and grid-aligned line-height
13. Formula containers: `overflow-x: auto; overflow-y: hidden;` for responsive equations. Add media queries at ~700px and ~500px for reduced padding and font sizes
14. Formula sheet cards: `overflow: visible` (NEVER `hidden` — popups must not be clipped)

## Image CSS

Use CSS variables derived from the chosen theme:

```css
.figure-box { background: var(--surface); border:1px solid var(--border); border-radius:10px; padding:12px; margin:16px 0; text-align:center; }
.figure-box img { max-width:100%; border-radius:6px; }
.figure-caption { font-size:12px; color: var(--muted); margin-top:8px; font-style:italic; }
```

Every theme should define these CSS variables at minimum: `--bg`, `--surface`, `--border`, `--text`, `--muted`, `--accent1` (equations), `--accent2` (definitions), `--accent3` (tips), `--accent4` (derivations), `--accent5` (examples), `--accent6` (units).

## Recommended Problems Sub-Link CSS

```css
.sidebar a.sub-link{padding-left:22px;font-size:12.5px;opacity:.85;}
.sidebar a.sub-link::before{content:'└ ';color:var(--border);}
```
