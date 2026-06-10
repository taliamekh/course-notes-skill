# Solution Pipeline & Assessment Reference

Read this file when solving problems (any type), building assessment prep sections, or updating the progress tracker.

## Solution Pipeline — FULL DETAIL REQUIRED

This is the default format for ALL problems: chapter examples, textbook worked examples, recommended problems, PAs, homework, problem sets, labs, exam prep practice. Solutions are NOT reformatting — BUILD complete, teachable solutions from scratch.

For every problem:

1. **Problem statement** — rewrite clearly, embed uploaded image if provided. If no image is available but the problem has a visual/geometric setup, CREATE an SVG diagram (read `references/diagram-rules.md` for specs).

2. **Thought process** — plain language: what type of problem, WHY this approach, what clues indicate it, what alternative approaches exist and why they're less ideal. Subject-specific: CS → data structure/algorithm choice; stats → which test/method; business → which framework.

3. **Setup** — given info, what to find, diagram/framework, coordinate system, assumptions.

4. **Formulas needed** — explicit list, BEFORE the solution. For every problem, render a `📋 Formulas Needed` block that names each formula the solution will use, shows its KaTeX, and tags its status on the official exam sheet (if the course has one). This is what makes prep pages actually usable: the student learns "this kind of problem uses these formulas" without re-reading the full solution.

   ```html
   <div class="formulas-needed">
     <h4>📋 Formulas Needed</h4>
     <ol>
       <li>
         <strong>Polar Arc Length</strong> — <span class="katex">L = ∫√(r² + r'²) dθ</span>
         <span class="exam-tag on">Exam Sheet #12</span>
         <a href="#fs-12">→ formula sheet</a>
       </li>
       <li>
         <strong>Chain rule (polar)</strong> — <span class="katex">dr/dθ</span>
         <span class="exam-tag off">Off-sheet — see Ch 3 notes</span>
         <a href="#fs-44">→ formula sheet</a>
       </li>
     </ol>
   </div>
   ```

   Tag styling: `.exam-tag.on` uses the theme's definition accent (it's a freebie during the exam); `.exam-tag.off` uses muted text (student must memorize). If the course has no official exam formula sheet, omit the tags but keep the block — the formula list is still useful as a per-problem index.

5. **Solution** — every step shown, every step annotated in plain english, substitutions shown explicitly. Subject-specific: math → every algebraic step; CS → trace + commented code; stats → formula + substitution + interpretation; business → systematic framework application.

6. **Answer** — final answer boxed with units/interpretation/conclusion.

7. **Tips & tricks** — exam shortcuts, common mistakes, pattern-matching ("if you see X, think Y"), CS → edge cases, stats → interpretation pitfalls.

8. **Concept bridge** — recap which reference sheet items were used (same names as in step 4) with anchor links to each. Step 4 tells the student what's *coming*; step 8 confirms what was *used* and points back to the deeper explanation in the formula sheet.

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

**For each assessment (Test 1, Test 2, Midterm, Final, etc.), use this section order top-to-bottom:**

1. **Scope banner** — which chapters/lectures this assessment covers (e.g. "Ch 1 (1.1–1.10) & Ch 2 (2.1–2.7)").

2. **Past exam cards at the top** — if past exams or practice exams are available, render clickable navigation cards FIRST so the student can jump straight to them. Each card shows the exam name, semester, question count, and topic keywords.

   ```html
   <div class="past-exam-grid">
     <a class="past-exam-card" href="#exam-w19">
       <div class="ex-name">Winter 2019 Final</div>
       <div class="ex-meta">4 LA + 15 MCQ · Stokes', divergence, Lagrange</div>
     </a>
     <a class="past-exam-card" href="#exam-f17">
       <div class="ex-name">Fall 2017 Final</div>
       <div class="ex-meta">5 LA · Green's, line integrals, optimization</div>
     </a>
   </div>
   ```

3. **🔍 What This Exam Looks Like** — exam format details from the syllabus or student intel:
   - Number and type of questions (MCQ count + marks, long-answer count + marks)
   - Time allowed
   - What's provided (formula sheet? calculator? scrap paper?)
   - Stylistic notes ("MCQs are heavy formula-sheet lookup — fluency matters")

   When student intel is available (from past cohorts, professor announcements, etc.), include a "Confirmed Topics" table:

   ```html
   <table class="confirmed-topics">
     <thead><tr><th>Q#</th><th>Topic</th><th>Specifics</th><th>Source</th></tr></thead>
     <tbody>
       <tr><td>Q1</td><td>Critical points / SDT</td><td>§3.1, find & classify</td><td>W26 cohort</td></tr>
     </tbody>
   </table>
   ```

4. **High / Medium / Low priority tiers** — three tables, color-coded by urgency, each row cross-referencing chapter section and formula sheet item number. This is the "where to spend your study time" allocation, NOT a topic-coverage list.

   ```html
   <h3 class="prio-high">🔴 High priority — study these first</h3>
   <table class="prio-table">
     <thead><tr><th>Topic</th><th>Where</th><th>Formula sheet</th><th>Why high</th></tr></thead>
     <tbody>
       <tr><td>Line integrals (scalar & vector)</td><td>Ch 6, §6.1–6.3</td><td>#29–#32</td><td>Appeared every past exam</td></tr>
       <tr><td>Divergence Theorem</td><td>Ch 7, §7.4</td><td>#41</td><td>Confirmed W26 LA</td></tr>
     </tbody>
   </table>

   <h3 class="prio-med">🟡 Medium priority</h3>
   <table class="prio-table">…</table>

   <h3 class="prio-low">🟢 Low priority — skip if time-constrained</h3>
   <table class="prio-table">…</table>
   ```

5. **🚫 Explicit deprioritization list** — what to actively SKIP. Most prep guides only tell you what to study; this tells you what NOT to. Students under time pressure benefit from being told "do not bother with X."

   ```html
   <div class="skip-list">
     <h3>🚫 Don't waste time on these</h3>
     <ul>
       <li>3D plotting by hand — won't be tested</li>
       <li>Derivations of the theorems — only their application is tested</li>
       <li>Standalone triple integrals without a vector field</li>
     </ul>
   </div>
   ```

6. **💡 Insider tips** — bulleted shortcuts and gotchas, ideally framed as student-sourced intel ("from students who wrote the W26 final"). Include things like: "if div F is constant, don't bother integrating — just multiply by volume," or "Lagrange always has 2 critical points, both worth checking."

7. **Problem Type → Theorem / Technique decision table** — the closing strategy table. Each row maps a problem pattern to the theorem/technique that solves it and the key formula. This is the "I have 30 seconds to figure out what to do" rescue table.

   ```html
   <table class="strategy-table">
     <thead><tr><th>Problem looks like…</th><th>Use…</th><th>Key formula</th></tr></thead>
     <tbody>
       <tr><td>Vector field over a closed curve in the plane</td><td>Green's Theorem</td><td>\(\oint \vec F\cdot d\vec r = \iint (\partial_x Q - \partial_y P) dA\)</td></tr>
       <tr><td>Flux through a closed surface</td><td>Divergence Theorem</td><td>\(\iint \vec F\cdot d\vec S = \iiint \nabla\cdot\vec F\, dV\)</td></tr>
     </tbody>
   </table>
   ```

8. **Topic checklist with confidence checkboxes** — every testable topic, persistent via localStorage, so the student can mark what they've reviewed.

9. **Must-know reference items** — subset of reference sheet with assessment-specific tips. Cross-link to formula sheet items by `#fs-N`.

10. **Practice problems** — full worked problems with the complete solution pipeline (including the "📋 Formulas Needed" upfront block).

11. **Example exams** — when the user provides past exams or practice exams:
    - Solve EVERY question with the full solution pipeline
    - Embed original exam images/pages
    - Tag each question with chapter/concept tested
    - "Exam debrief" after each example exam: topics that appeared, patterns, time allocation
    - Cross-exam analysis: if multiple exams provided, identify recurring question types and high-probability topics
    - For later assessments: note which topics from earlier assessments reappear and which are new

12. **Diagrams** — generated SVGs for problems with visual setups (read `references/diagram-rules.md`).

13. **Common traps** — mistakes students make under time pressure.

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
