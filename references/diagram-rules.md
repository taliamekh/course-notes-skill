# Diagram Generation Rules

Read this file when generating SVG diagrams for problems or concepts that lack an uploaded image.

## When to Generate Diagrams

Generate an SVG when:
- A problem has a visual/geometric setup but no image was provided
- An uploaded image is too blurry to use
- A solution references "see diagram" with none provided
- CS/stats/business problems need flowcharts, trees, or curves
- The user explicitly asks for a diagram

## Theme Palette for Diagrams

Use the chosen theme's palette for all diagram elements:
- Outlines: primary and secondary accent colors
- Force arrows: color by type (use accent colors mapped to categories — e.g., gravity=warm accent, normal=cool accent, friction=gold/tertiary, applied=primary)
- Labels: text color from theme, chosen font
- Dimensions: muted color, dashed
- Axes: secondary accent or definition color
- Background: transparent

## Subject-Type Diagram Mapping

| Subject | Diagram Types |
|---|---|
| Engineering | FBDs, mechanisms, circuit schematics |
| Math | Plots, geometric constructions, function graphs |
| Statistics | Probability trees, normal curves, scatter plots |
| CS | Flowcharts, data structures, state diagrams |
| Business | Supply/demand curves, process flows |

## Label Placement — NEVER on Top of Diagram Elements

Labels overlapping diagram lines is the single most reported visual bug — the collision check below catches it every time.

Labels must be placed in nearby open space, not overlapping lines, arrows, shapes, or other labels. Follow these rules:

1. **Perpendicular offset method:** For every label on a line/arrow, calculate the perpendicular direction from the line and offset the label at least 15px in that direction toward the side with more open space. Never place a label at the midpoint of a line without an offset.

2. **Collision check (mandatory — DO THIS BEFORE OUTPUTTING):** For EVERY label at position (lx, ly), compute the y-value of EVERY line in the diagram at x=lx using `y = y1 + (lx-x1)/(x2-x1) * (y2-y1)` (only if x1 ≤ lx ≤ x2). If any line's y-value is within 18px of ly, the label WILL overlap — move it. Show this arithmetic in your thinking to prove each label is clear.

3. **Spread the geometry:** If a diagram has many lines close together (like a parallelogram), increase the viewBox size and spread vertices apart so lines have 40+ px vertical separation. A cramped diagram with overlapping labels is worse than a larger diagram with clear spacing.

4. **Point labels:** Adjacent to the dot, offset toward the quadrant with the most open space.

5. **Axis labels:** Past the arrowhead, never overlapping the axis line.

6. **Font size:** 14–18px for labels (smaller than body text). Never larger than 18px in diagrams.

7. **Captions:** Always below the diagram in `.figure-caption`, never inside the SVG.

8. **Multiple labels near same endpoint:** Stagger vertically or use leader lines. Never stack two labels at the same position.

## SVG Diagram Rule for Problems

When a problem references a figure, diagram, or geometric setup and the source image cannot be embedded (blurry, not uploaded, described in text only, or the solution says "see figure"), you MUST create an SVG that reproduces it faithfully. Use the theme's palette, follow all label collision rules above, and match the original's geometry as closely as possible. Missing diagrams make solutions incomplete.
