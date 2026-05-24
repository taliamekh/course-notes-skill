# Solution Pipeline & Assessment Reference

Read this file when solving problems (any type), building assessment prep sections, or updating the progress tracker.

## Solution Pipeline — FULL DETAIL REQUIRED

This is the default format for ALL problems: chapter examples, textbook worked examples, recommended problems, PAs, homework, problem sets, labs, exam prep practice. Solutions are NOT reformatting — BUILD complete, teachable solutions from scratch.

For every problem:

1. **Problem statement** — rewrite clearly, embed uploaded image if provided. If no image is available but the problem has a visual/geometric setup, CREATE an SVG diagram (read `references/diagram-rules.md` for specs).

2. **Thought process** — plain language: what type of problem, WHY this approach, what clues indicate it, what alternative approaches exist and why they're less ideal. Subject-specific: CS → data structure/algorithm choice; stats → which test/method; business → which framework.

3. **Setup** — given info, what to find, diagram/framework, coordinate system, assumptions.

4. **Solution** — every step shown, every step annotated in plain english, substitutions shown explicitly. Subject-specific: math → every algebraic step; CS → trace + commented code; stats → formula + substitution + interpretation; business → systematic framework application.

5. **Answer** — final answer boxed with units/interpretation/conclusion.

6. **Tips & tricks** — exam shortcuts, common mistakes, pattern-matching ("if you see X, think Y"), CS → edge cases, stats → interpretation pitfalls.

7. **Concept bridge** — which reference sheet items were used, linked by name.

## Recommended Problems — SEPARATE PAGE PER CHAPTER

Each chapter gets its own dedicated Recommended Problems page, accessible via a sub-link nested under the chapter in the sidebar menu. These are NOT inline within the chapter.

**Sidebar structure:**
```
Ch 1 – Vectors
└ Problems          ← sub-link, indented, links to id="ch1prob"
Ch 2 – Lines & Curves
└ Problems          ← sub-link, links to id="ch2prob"
```

**Page ID convention:** `ch{N}prob` (e.g. `ch1prob`, `ch2prob`)

**File convention:** Each problems page lives in its own fragment file: `chapters/ch{N}-prob.html`.

**When to populate:** Problems are added when the chapter is written, or when the user provides a problem set separately. If the course outline specifies suggested problems (e.g. "§2.3 #1-5, 7, 12"), solve all of them using the full solution pipeline.

---

## Assessment Prep Sections — PRACTICE-FOCUSED

Generated DYNAMICALLY based on the course configuration. If the course has 3 tests and a final, there are 4 prep sections. If it has 1 midterm and a final, there are 2.

**For each assessment (Test 1, Test 2, Midterm, Final, etc.):**

1. **Scope banner** — which chapters/lectures this assessment covers
2. **Topic checklist** — every testable topic with confidence checkboxes
3. **Condensed concept review** — key ideas per chapter, explained (not just terms)
4. **Must-know reference items** — subset of reference sheet with assessment-specific tips
5. **Practice problems** — full worked problems with the complete solution pipeline
6. **Example exams** — the user may provide past exams, practice exams, or professor-provided examples. When provided:
   - Solve EVERY question with the full solution pipeline
   - Embed original exam images/pages
   - Tag each question with chapter/concept tested
   - "Exam debrief" after each example exam: topics that appeared, patterns, time allocation
   - Cross-exam analysis: if multiple example exams provided, identify recurring question types and high-probability topics
   - For later assessments: note which topics from earlier assessments reappear and which are new
7. **Diagrams** — generated SVGs for problems with visual setups
8. **Common traps** — mistakes students make under time pressure
9. **Strategy guide** — approach for unseen problems: identify type → choose method → execute → verify

**For the Final specifically, also include:**
- "What's new since last assessment" — focused review of new content
- Integration problems combining concepts across chapters
- Cumulative reference sheet

---

## Progress Tracker — INTERACTIVE (INCREMENTALLY UPDATED)

A dedicated section with hierarchical checkboxes that persist via localStorage (keyed by course name). Items are added dynamically as content is added.

### Structure

```
Progress for MECH 2005 — Dynamics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[overall progress bar — auto-calculated from sub-items]

▼ Chapter 1 — Kinematics of Particles          [■■■■■■■■░░] 80%
  ☑ Chapter notes reviewed
  ☑ Chapter examples completed
    ☑ Example 1.1 — Rectilinear motion
    ☑ Example 1.2 — Projectile
    ☐ Example 1.3 — Curvilinear
  ☐ Chapter reference items memorized

═══════════════════════════════════════════════════════════
 ⚑ TEST 1 CHECKPOINT — Ch 1–3               [■■░░░░░░░░] 20%
═══════════════════════════════════════════════════════════

▼ Test 1 Prep                                  [■■░░░░░░░░] 20%
  ☐ Concept review done
  ☐ Must-know equations memorized
  ☐ Practice problems completed
  ▼ Example exam 1
    ☐ Q1 — projectile motion
  ☐ Common traps reviewed

▼ Assignments (up to Test 1)                   [■■■■■░░░░░] 50%
  ☑ PA 1 — completed & reviewed
  ☐ PA 3

...more chapters and checkpoints...

═══════════════════════════════════════════════════════════
 ⚑ FINAL CHECKPOINT — Cumulative             [░░░░░░░░░░] 0%
═══════════════════════════════════════════════════════════
```

### Assessment Checkpoints Break Progress Into Phases

The tracker is organized chronologically:
1. Chapters and assignments that fall BEFORE a test/midterm are grouped above that checkpoint
2. The checkpoint itself is a bold, visually distinct divider showing the assessment name, what it covers, and its aggregate completion percentage
3. Chapters and assignments AFTER that checkpoint but before the next one are grouped in the next phase
4. The final checkpoint sits at the bottom covering everything

### Checkpoint Styling (uses chosen theme)

- Checkpoint divider: full-width bar with gradient using the theme's equation and definition accent colors at low opacity
- Flag icon (⚑): theme's example/gold accent for upcoming, theme's definition/teal accent for completed
- Assessment name: bold, large text in the equation accent color
- Scope label ("Ch 1–3"): muted text color
- Checkpoint progress: aggregates ALL items in that phase

### Implementation Rules

1. Each checkbox is an `<input type="checkbox">` with a unique ID based on course + section + item
2. State saved to localStorage on every change: `localStorage.setItem('{course}-progress', JSON.stringify(state))`
3. Loaded from localStorage on page open
4. Parent items auto-calculate: all children checked → parent checked, some → indeterminate
5. Progress bars per section: auto-calculated from checkbox completion
6. Checkpoint progress bars: aggregate all items in that phase
7. Overall progress bar at top: weighted average across all checkpoints
8. Sub-items collapsible (click header to expand/collapse)
9. Items added dynamically as content is added
10. Example exams appear as sub-items under their prep section, with individual questions as checkable items
11. Assignments are grouped by which checkpoint they fall under (based on chapter coverage)

### Styling (uses chosen theme)

- Checked: equation accent color checkbox fill
- Unchecked: surface color with border color
- Progress bar fill: gradient from equation accent to definition accent
- Section headers: text color with chevron toggle
- Percentage labels: muted color
