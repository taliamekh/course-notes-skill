# Deep Space Theme Reference

## Color Tokens

```
--ds-bg: #0B0E14
--ds-surface: #141820
--ds-surface-hover: #1A2030
--ds-accent: #AD8CFF        (purple — equations, primary highlights)
--ds-accent2: #56D6C1       (teal — definitions, secondary highlights)
--ds-accent3: #FFD866       (gold — warnings, tips, important callouts)
--ds-text: #D4D4E8
--ds-muted: #6E7191
--ds-border: #1E2433
--ds-code-bg: #0F1219
```

## Font

Google Font: `Space Grotesk` weights 400, 500, 600, 700.

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

All text uses `font-family: 'Space Grotesk', sans-serif`.

## Color Coding System

Content is color-coded by TYPE — every element gets a left-border or badge color:

| Type | Color | Token | Use |
|------|-------|-------|-----|
| Equations / Formulas | Purple | `--ds-accent` (#AD8CFF) | Equation cards, formula highlights |
| Definitions / Concepts | Teal | `--ds-accent2` (#56D6C1) | Definition blocks, concept explanations |
| Tips / Warnings / Important | Gold | `--ds-accent3` (#FFD866) | Tip callouts, exam warnings, key insights |
| Derivations / Proofs | Soft blue | #5B9DFF | Step-by-step derivation chains |
| Examples / Solved problems | Soft green | #7EE8B4 | Worked examples, PA solutions |
| Units / Dimensions | Soft pink | #F0A0C0 | Unit analysis blocks |

## Variable Pills

Variables inside equations use colored pills to distinguish them. Each variable in an equation gets a pill with:
- Background: `{color}15` (very translucent)
- Text: the full color
- Content: `symbol — name (unit)`

When a variable is a compound quantity (like KE = kinetic energy, PE = potential energy), append a tag showing what it represents:

```html
<span class="var-pill" style="background:#AD8CFF15;color:#AD8CFF">
  KE — kinetic energy (J)
  <span class="var-derives">= ½mv²</span>
</span>
```

## Equation Card Template

```html
<div class="eq-card" style="border-left-color: {type_color}">
  <div class="eq-label" style="color: {type_color}">{CATEGORY LABEL}</div>
  <div class="eq-name">{Equation Name}</div>
  <div class="eq-formula">{Formula in plain text or KaTeX}</div>
  <div class="eq-desc">{One-line plain-english description}</div>
  <div class="eq-conditions">{When to use / conditions / assumptions}</div>
  <div class="var-row">
    <!-- one pill per variable -->
  </div>
</div>
```

## Tip / Warning Callout Template

```html
<div class="callout callout-{type}" style="border-color:{color};background:{color}10">
  <div class="callout-icon" style="color:{color}">
    <!-- ti-bulb for tips, ti-alert-triangle for warnings, ti-star for exam-important -->
  </div>
  <div class="callout-body">
    <div class="callout-title" style="color:{color}">{Title}</div>
    <div class="callout-text">{Content}</div>
  </div>
</div>
```

Types:
- `tip` → gold (#FFD866), icon: ti-bulb
- `warning` → #FF6B6B, icon: ti-alert-triangle  
- `exam` → #AD8CFF, icon: ti-star
- `remember` → #56D6C1, icon: ti-bookmark

## PA Solution Step Template

Each PA question gets a collapsible card. Each step inside has:

```html
<div class="step">
  <div class="step-num" style="background:{accent}22;color:{accent}">{n}</div>
  <div class="step-body">
    <div class="step-title">{What this step does}</div>
    <div class="step-work">{The math / substitution}</div>
    <div class="step-tip">{Optional tip for this step}</div>
  </div>
</div>
```

Color-code steps:
- Setup / given info → teal border
- Core calculation → purple border  
- Final answer → gold border + highlight background

## Menu / Navigation

The top nav menu uses pill-shaped tabs:

```html
<div class="menu-bar">
  <button class="menu-tab active" data-section="chapters">
    <i class="ti ti-book" aria-hidden="true"></i> Chapters
  </button>
  <button class="menu-tab" data-section="midterm">
    <i class="ti ti-clipboard-check" aria-hidden="true"></i> Midterm prep
  </button>
  <button class="menu-tab" data-section="final">
    <i class="ti ti-award" aria-hidden="true"></i> Final prep
  </button>
  <button class="menu-tab" data-section="pa">
    <i class="ti ti-math-function" aria-hidden="true"></i> PA solutions
  </button>
  <button class="menu-tab" data-section="equations">
    <i class="ti ti-variable" aria-hidden="true"></i> Equations
  </button>
  <button class="menu-tab" data-section="summary">
    <i class="ti ti-list-details" aria-hidden="true"></i> Summary
  </button>
</div>
```

Active tab: `background: {accent}18; color: {accent}; border: 1px solid {accent}`
Inactive tab: `color: {muted}; border: 1px solid transparent`

## Summary Page Structure

The summary section contains:
1. **Stats bar** — total equations, chapters covered, PA sets completed
2. **Key concepts** — bullet list of the most important ideas per chapter
3. **Must-know equations** — subset of equations tagged as exam-critical
4. **Common mistakes** — pitfalls collected from PA solutions and tips
5. **Quick reference** — compressed formula table (no explanations, just formula + name)

## KaTeX Integration

Load KaTeX from CDN for proper equation rendering:

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
```

Wrap inline math in `\( ... \)` and display math in `\[ ... \]`. Call `renderMathInElement(document.body)` after DOM is ready.

## Figure / Image Containers

Uploaded images (textbook figures, problem diagrams, handwritten notes) are embedded as base64 in styled containers:

```css
.figure-box {
  background: #141820;
  border: 1px solid #1E2433;
  border-radius: 10px;
  padding: 12px;
  margin: 16px 0;
  text-align: center;
}
.figure-box img {
  max-width: 100%;
  border-radius: 6px;
}
.figure-caption {
  font-size: 12px;
  color: #6E7191;
  margin-top: 8px;
  font-style: italic;
}
```

For side-by-side figures (e.g., before/after in a collision):
```css
.figure-row {
  display: flex;
  gap: 12px;
  margin: 16px 0;
}
.figure-row .figure-box { flex: 1; }
```

## SVG Diagram Palette

When generating inline SVG diagrams (FBDs, mechanisms, setups), use:

| Element | Color | Hex |
|---------|-------|-----|
| Object outlines | Purple accent | #AD8CFF |
| Support / ground | Teal accent | #56D6C1 |
| Gravity arrows | Soft red | #FF6B6B |
| Normal force arrows | Teal | #56D6C1 |
| Friction arrows | Gold | #FFD866 |
| Applied force arrows | Purple | #AD8CFF |
| Velocity vectors | Soft blue | #5B9DFF |
| Acceleration vectors | Soft green | #7EE8B4 |
| Labels / text | Text color | #D4D4E8 |
| Dimension lines | Muted dashed | #6E7191 |
| Angles | Gold | #FFD866 |
| Coordinate axes | Blue | #5B9DFF |
| Background | Transparent or surface | transparent / #141820 |

Arrow style: solid stroke, 2px width, pointed head. Use distinct arrow head shapes for forces vs velocities (triangle for force, open chevron for velocity).

## Thought Process Block

A special callout for the "thinking before solving" section in PA solutions and examples:

```html
<div class="thought-block">
  <div class="thought-header">
    <i class="ti ti-brain"></i> Thought process
  </div>
  <div class="thought-body">
    <p>This is a [problem type] problem. I know because...</p>
    <p>The approach: ...</p>
    <p>Why not [alternative]? Because...</p>
  </div>
</div>
```

```css
.thought-block {
  background: rgba(173, 140, 255, 0.06);
  border: 1px solid rgba(173, 140, 255, 0.15);
  border-radius: 10px;
  padding: 16px 18px;
  margin: 16px 0;
}
.thought-header {
  color: #AD8CFF;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.thought-header i { font-size: 16px; }
.thought-body p {
  font-size: 13px;
  color: #D4D4E8;
  margin: 6px 0;
  line-height: 1.6;
}
```

## Responsive Layout

The note viewer is a single-page app with:
- Fixed sidebar (chapter list) on left — 220px wide
- Main content area fills remaining width
- On smaller viewports, sidebar collapses to a hamburger menu

## Dark Mode Consistency

Everything uses the Deep Space palette — no light mode variant needed. All backgrounds are dark, all text is light. The `--ds-bg` is the page background, `--ds-surface` is for cards and panels, `--ds-surface-hover` for hover states.
