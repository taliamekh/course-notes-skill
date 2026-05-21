---
name: course-notes
description: >
  Interactive course notes with the Deep Space dark theme. Supports engineering, math, stats, CS, business, physics,
  and any university course. Trigger on: class notes, lecture notes, chapter notes, equation sheets, formula sheets,
  theorem references, algorithm references, assignment solutions (PA, homework, labs), test/midterm/final exam prep,
  course progress tracking, study notes, practice problems, chapter examples, worked examples, proofs, derivations,
  code walkthroughs, case studies, quiz prep, diagrams, or uploading images of notes, textbook pages, lecture slides,
  or handwritten work. Also trigger when updating or viewing previously created notes.
  Pairs with NotebookLM MCP for cloud storage and AI-powered querying. Always use this skill for academic note-taking
  even if the user doesn't name a specific subject — if they mention a course, class, or studying, this skill applies.
---

# Course Notes System

A structured note-taking system that creates interactive, color-coded HTML note pages for university courses, backed by NotebookLM for persistent storage. Every solution, concept, and reference item is explained from scratch for someone learning the material for the first time.

## Theme

**Deep Space** — dark background (#0B0E14), purple (#AD8CFF), teal (#56D6C1), gold (#FFD866). Font: Space Grotesk.

Read `references/theme.md` before generating any HTML output for color tokens, component templates, and the full color-coding system.

---

## Subject Detection and Adaptation

When the user names a course, detect the subject category and adapt the note structure. The menu bar, theme, image pipeline, NotebookLM workflow, and solution detail level are the same across ALL subjects. What changes is vocabulary and specialized content blocks.

### Subject → Content Mapping

| Menu Section | Engineering | Math | Statistics | Computer Science | Business / Econ |
|---|---|---|---|---|---|
| **Reference sheet** | Equation sheet | Theorem & formula sheet | Distribution & formula sheet | Algorithm & syntax reference | Framework & model sheet |
| **Solutions** | PA / homework solutions | Proof walkthroughs & problem solutions | Problem solutions & data interpretations | Coding solutions & algorithm analyses | Case study analyses & problem solutions |
| **Key blocks** | FBDs, diagrams, unit analysis | Proofs, lemmas, corollaries | Distribution tables, hypothesis test flows | Code blocks, Big-O, pseudocode, logic tables | Frameworks, decision matrices, financial models |
| **Diagrams** | Mechanism sketches, FBDs | Geometric constructions, function plots | Probability trees, normal curves, scatter plots | Flowcharts, data structures, state diagrams | Supply/demand curves, process flows |

### Subject-Specific Blocks

**Engineering:** Equation cards with variable pills and unit analysis. SVG free body diagrams. "When to use / when NOT to use" on every equation. Full algebraic step-by-step solutions.

**Mathematics:** Theorem cards with proof sketch and intuition. Proof walkthroughs: claim → setup → key insight → formal steps → QED, each step annotated with WHY. Formula items with geometric/visual intuition and exam tips.

**Statistics:** Distribution cards with parameters, mean/variance, shape, and WHEN to use. Hypothesis test decision tree. Solutions include: state hypotheses → check assumptions → compute test stat → p-value → interpret. R/Python code snippets where relevant.

**Computer Science:** Code blocks with syntax highlighting (Prism.js). Algorithm cards with pseudocode, time/space complexity, when to use/not use. Trace tables. Flowcharts and data structure SVGs. Debugging tips.

**Business / Economics:** Framework cards with components, applications, limitations. Case study template: situation → problem → analysis → recommendation → risks. Financial model breakdowns. Key terms with real-world examples.

---

## Core Workflow

### 0. Course Setup Prompt — RUN ONCE PER NEW COURSE

**The very first time the user creates notes for a new course, prompt them for their course structure BEFORE doing anything else.** This configures the menu bar, progress tracker, and assessment sections.

Ask the user (use the ask_user_input tool where possible, free text for specifics):

**Question 1: "What's the course name and code?"**
Free text — e.g., "MECH 2005 — Dynamics"

**Question 2: "List everything you're graded on and how many of each."**
Free text — the user types something like:
- "8 assignments, 3 tests, 1 final (cumulative)"
- "6 PAs, 1 midterm, 1 final, 4 labs"
- "10 homework sets, 2 midterms, 1 final, weekly quizzes"
- "5 assignments, a project, and a final"

Parse whatever they give you. Extract: assessment type, count, and any notes (cumulative, weighted, etc.). If something is ambiguous ("tests" vs "midterms"), don't ask — just use their terminology. If they mention weights ("assignments 20%, midterm 30%, final 50%"), store those too.

**Question 3: "How is the course content organized?"**
Single-select:
- By chapters (textbook-driven)
- By lectures (lecture-driven)
- By modules/units
- Mix of the above

**Store this configuration.** Save it as a note in the NotebookLM notebook titled `_COURSE_CONFIG` with a structured format:

```
Course: MECH 2005 — Dynamics
Subject: Engineering
Content org: Chapters
Assessments:
  - Assignments: 8 (PA1–PA8)
  - Tests: 3 (Test 1, Test 2, Test 3)
  - Final: yes (cumulative)
  - Labs: 0
  - Quizzes: 0
Chapters: [populated as content is added]
```

**This configuration drives everything:**
- The menu bar shows only relevant sections (no "Midterm prep" if the course has tests instead)
- The progress tracker knows what to list
- Assessment prep sections match the actual course structure

**If the user dives straight in** ("here are my Chapter 1 notes") without doing setup, infer what you can from context and ask the remaining questions in a lightweight way — don't block them from adding content.

### 1. Identify the content being added

For each interaction, determine:
- **Course name** (already configured, or detect from context)
- **Subject category** (engineering / math / stats / CS / business)
- **Content type**: chapter/lecture notes, chapter examples, assignment solutions, exam prep, reference items
- **Chapter/lecture number and title**

### 2. Handle uploaded images and documents

The user will upload lecture slides, textbook pages, handwritten notes, assignment sheets, and exams. These contain critical visual content that MUST appear in the final notes.

**Step 1: Scan the entire upload first.**
Read/view EVERY page. Build an inventory of: diagrams, figures, example problem statements, important derivation steps, tables, code samples — anything visual the professor included.

**Step 2: Extract important images selectively.**
For PDFs: convert specific pages to images using `pdftoppm -f {page} -l {page} -png input.pdf output` or Python (pdf2image / PyMuPDF). Only extract pages with visual content — not every page. For a 40-slide deck, extract maybe 8-15 key images.

For uploaded images: copy from `/mnt/user-data/uploads/`, view each to understand content.

**Step 3: Decide what to embed.**

| Content type | Embed? | Where? |
|---|---|---|
| Problem statement / exam question | YES always | Top of solution card |
| Diagram, FBD, flowchart, sketch | YES always | In setup step or concept section |
| Textbook figure, graph, plot | YES always | Next to concept it illustrates |
| Code output / terminal screenshot | YES always | Next to related code block |
| Derivation or proof diagram | YES always | Inline in explanation |
| Slide with only bullet text | NO — transcribe | Convert to styled note content |
| Table / reference data | YES if complex | Embed or recreate as HTML table |
| Professor handwriting | YES always | Alongside typed clean version |

**Step 4: Convert and embed.**
Base64-encode each image, embed as `<img src="data:image/png;base64,...">` inside a `.figure-box` container with caption.

**Step 5: Generate diagrams when none exist.**
If a problem has a visual setup but no image provided, generate an SVG in the Deep Space palette. Also generate when: uploaded image is blurry, solution says "see diagram" with none provided, or CS/stats/business problems need flowcharts/trees/curves.

### 3. NotebookLM storage

**First time for a course:**
1. `notebook_list` to check for existing notebook
2. `notebook_create` with course name if needed
3. Store course config as `_COURSE_CONFIG` note

**Adding content:**
- `note` (create) for each chapter/section
- Title formats: `Ch{N} — {Title}`, `Lecture {N} — {Title}`, `Ch{N} Examples — {Title}`, `PA{N} / HW{N} / Lab{N} — {Title}`, `Test {N} Prep — {Topic}`, `Final Prep — {Topic}`
- `label` to organize into categories

**Retrieving:** `notebook_get`, `note` (list), `notebook_query`

### 4. Generate the interactive HTML note page

Output to `/mnt/user-data/outputs/`. File naming: `{course-code}-{content-type}.html`.

Full course view → single-page app with sidebar. Single chapter → focused page with menu bar.

---

## Note Page Structure

The menu bar is DYNAMIC — it's built from the course configuration, not hardcoded. Only sections with content or that the course structure calls for are shown.

**Possible menu items (shown only when relevant):**

| Menu item | Shown when |
|---|---|
| Chapters / Lectures / Modules | Always |
| Assignments (PA / HW / Labs) | Course has assignments |
| Reference sheet | Always |
| Test 1 prep, Test 2 prep, etc. | Course has multiple tests |
| Midterm prep | Course has a single midterm |
| Final prep | Course has a final |
| Quiz prep | Course has quizzes |
| Summary | Always |
| Progress | Always |

### Chapters / Lectures / Modules
- Organized by number
- Key concepts with full explanations
- Definitions (teal), theorems/principles (purple)
- Chapter examples (see below)
- Embedded figures and diagrams

### Chapter Examples

In-lecture examples → inline under "Worked examples" subheading.
Separate example sets → dedicated sub-section within the chapter.

Every example: original problem (with embedded image), "why this matters", full step-by-step solution, key takeaway.

### Assignment Solutions — FULL DETAIL REQUIRED

Applies to: PAs, homework, problem sets, labs, or any graded assignment.

Solutions are NOT reformatting. BUILD complete, teachable solutions from scratch.

For every problem:
1. **Problem statement** — rewrite clearly, embed uploaded image if provided
2. **Thought process** — plain language: what type of problem, WHY this approach, what clues indicate it, what alternative approaches exist and why they're less ideal. Subject-specific: CS → data structure/algorithm choice; stats → which test/method; business → which framework.
3. **Setup** (teal steps) — given info, what to find, diagram/framework, coordinate system, assumptions
4. **Solution** (purple steps) — every step shown, every step annotated in plain english, substitutions shown explicitly. Subject-specific: math → every algebraic step; CS → trace + commented code; stats → formula + substitution + interpretation; business → systematic framework application.
5. **Answer** (gold) — final answer boxed with units/interpretation/conclusion
6. **Tips & tricks** — exam shortcuts, common mistakes, pattern-matching ("if you see X, think Y"), CS → edge cases, stats → interpretation pitfalls
7. **Concept bridge** — which reference sheet items were used, linked by name

### Reference Sheet — FULLY EXPLAINED

Each item (equation, theorem, algorithm, framework) is a mini-lesson:
1. **Statement / Formula** — KaTeX or code block
2. **Plain-english explanation** — what it MEANS physically/conceptually
3. **Origin** — derivation hint, proof sketch, or context
4. **When to use** — scenarios, signal words in problems
5. **When NOT to use** — misapplications, limitations, assumptions required
6. **Use case examples** — 1-2 one-liner problem → method mappings
7. **Interactive pills** — variables (symbol + name + unit + relationships), complexity pills (CS), component pills (business)
8. **Color coding**: Purple = core, Teal = definitions, Gold = exam-critical, Blue = derived, Green = special cases, Pink = units/conditions

### Assessment Prep Sections — PRACTICE-FOCUSED

This section is generated DYNAMICALLY based on the course configuration. If the course has 3 tests and a final, there are 4 prep sections. If it has 1 midterm and a final, there are 2. Each one follows the same structure:

**For each assessment (Test 1, Test 2, Midterm, Final, etc.):**

1. **Scope banner** — which chapters/lectures this assessment covers
2. **Topic checklist** — every testable topic with confidence checkboxes
3. **Condensed concept review** — key ideas per chapter, explained (not just terms)
4. **Must-know reference items** — subset of reference sheet with assessment-specific tips
5. **Practice problems** — full worked problems with the complete solution pipeline
6. **Example exams** — the user may provide past exams, practice exams, or professor-provided examples (uploaded images, PDFs, or text). There may be MULTIPLE example exams per assessment. When provided:
   - Solve EVERY question with the full solution pipeline
   - Embed original exam images/pages
   - Tag each question with chapter/concept tested
   - "Exam debrief" after each example exam: topics that appeared, patterns, time allocation
   - Cross-exam analysis: if multiple example exams provided, identify recurring question types and high-probability topics
   - For later assessments (Test 2, Test 3, Final): note which topics from earlier assessments reappear and which are new
7. **Diagrams** — generated SVGs for problems with visual setups
8. **Common traps** — mistakes students make under time pressure
9. **Strategy guide** — approach for unseen problems: identify type → choose method → execute → verify

**For the Final specifically, also include:**
- "What's new since last assessment" — focused review of new content
- Integration problems combining concepts across chapters
- Cumulative reference sheet

### Summary
- Stat cards: reference items, chapters, examples, assignments
- Chapter-by-chapter bullet summary
- Must-know items (compact)
- Common mistakes and pitfalls
- Quick-reference table

### Progress — INTERACTIVE TRACKER

A dedicated section with hierarchical checkboxes that persist via localStorage (keyed by course name). This lets the student track what they've completed across the entire course.

**Structure:**

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

▼ Chapter 2 — Force and Acceleration           [■■■░░░░░░░] 30%
  ☑ Chapter notes reviewed
  ☐ Chapter examples completed
    ☐ Example 2.1 ...
  ☐ Chapter reference items memorized

▼ Chapter 3 — Kinetics of Particles            [░░░░░░░░░░] 0%
  ...

═══════════════════════════════════════════════════════════
 ⚑ TEST 1 CHECKPOINT — Ch 1–3               [■■░░░░░░░░] 20%
═══════════════════════════════════════════════════════════

▼ Test 1 Prep                                  [■■░░░░░░░░] 20%
  ☐ Concept review done
  ☐ Must-know equations memorized
  ☐ Practice problems completed
  ▼ Example exam 1
    ☐ Q1 — projectile motion
    ☐ Q2 — friction on incline
    ☐ Q3 — energy conservation
  ▼ Example exam 2
    ☐ Q1 — work-energy problem
    ☐ Q2 — impulse-momentum
  ☐ Common traps reviewed

▼ Assignments (up to Test 1)                   [■■■■■░░░░░] 50%
  ☑ PA 1 — completed & reviewed
  ☑ PA 2 — completed & reviewed
  ☐ PA 3

▼ Chapter 4 — Work and Energy                  [░░░░░░░░░░] 0%
  ...

▼ Chapter 5 — Impulse and Momentum             [░░░░░░░░░░] 0%
  ...

═══════════════════════════════════════════════════════════
 ⚑ TEST 2 CHECKPOINT — Ch 4–5               [░░░░░░░░░░] 0%
═══════════════════════════════════════════════════════════

▼ Test 2 Prep                                  [░░░░░░░░░░] 0%
  ☐ Concept review done
  ...

▼ Assignments (Test 1 → Test 2)                [░░░░░░░░░░] 0%
  ☐ PA 4
  ☐ PA 5

...more chapters...

═══════════════════════════════════════════════════════════
 ⚑ FINAL CHECKPOINT — Cumulative             [░░░░░░░░░░] 0%
═══════════════════════════════════════════════════════════

▼ Final Prep                                    [░░░░░░░░░░] 0%
  ☐ Concept review done
  ☐ Post-Test 2 content reviewed
  ☐ Cumulative reference sheet memorized
  ▼ Practice final 1
    ☐ Q1 ...
  ☐ Common traps reviewed
```

**Key design: Assessment checkpoints break the progress into phases.**

The tracker is NOT just a flat list. It's organized chronologically as the course unfolds, with assessment checkpoints acting as visual dividers:

1. Chapters and assignments that fall BEFORE a test/midterm are grouped above that checkpoint
2. The checkpoint itself is a bold, visually distinct divider showing the assessment name, what it covers, and its aggregate completion percentage
3. Chapters and assignments AFTER that checkpoint but before the next one are grouped in the next phase
4. The final checkpoint sits at the bottom covering everything

This mirrors how students actually experience a course: learn chapters → prep for test → take test → learn more → prep for next test → final.

**Checkpoint styling (Deep Space):**
- Checkpoint divider: full-width bar with `background: linear-gradient(90deg, #AD8CFF33, #56D6C133)`
- Flag icon (⚑): gold (#FFD866) for upcoming assessments, teal (#56D6C1) for completed ones
- Assessment name: bold, large text in accent purple
- Scope label ("Ch 1–3"): muted text
- Checkpoint progress: aggregates ALL items in that phase (chapters + assignments + prep)

**Implementation rules:**
1. Each checkbox is an `<input type="checkbox">` with a unique ID based on course + section + item
2. State saved to localStorage on every change: `localStorage.setItem('{course}-progress', JSON.stringify(state))`
3. Loaded from localStorage on page open
4. Parent items auto-calculate: all children checked → parent checked, some → indeterminate
5. Progress bars per section: auto-calculated from checkbox completion
6. Checkpoint progress bars: aggregate all items in that phase (chapters above it + assignments in that range + the prep section itself)
7. Overall progress bar at top: weighted average across all checkpoints
8. Sub-items collapsible (click header to expand/collapse)
9. Items added dynamically as content is added
10. Example exams appear as sub-items under their prep section, with individual questions as checkable items
11. Assignments are grouped by which checkpoint they fall under (based on chapter coverage)

**Styling (Deep Space):**
- Checked: accent purple (#AD8CFF) checkbox fill
- Unchecked: surface (#141820) with border (#1E2433)
- Progress bar fill: gradient from purple to teal
- Section headers: text color with chevron toggle
- Percentage labels: muted (#6E7191)
- Checkpoint bars: distinct from regular sections — wider padding, gradient background, flag icon

---

## Diagram Generation

When no image provided, generate SVG with Deep Space palette:
- Outlines: #AD8CFF / #56D6C1
- Force arrows: color by type (gravity=#FF6B6B, normal=#56D6C1, friction=#FFD866, applied=#AD8CFF)
- Labels: #D4D4E8, Space Grotesk
- Dimensions: #6E7191 dashed
- Axes: #5B9DFF
- Background: transparent

Subject types: Engineering → FBDs, mechanisms. Math → plots, constructions. Stats → curves, trees. CS → flowcharts, data structures. Business → supply/demand, process flows.

---

## HTML Generation Rules

1. Always load: KaTeX (cdnjs), Space Grotesk (Google Fonts), Tabler Icons
2. For CS: also load Prism.js for syntax highlighting
3. Deep Space palette exclusively (see `references/theme.md`)
4. KaTeX: `\( inline \)` and `\[ display \]`
5. Interactive pills (click to expand), collapsible solutions/examples
6. Fixed menu bar (top), fixed sidebar (full-course view)
7. Embedded images in `.figure-box` containers with captions
8. SVG diagrams inline using Deep Space colors
9. Sections as `<section id="{name}">` for anchor nav
10. Progress checkboxes persist via localStorage keyed by course name
11. Menu bar is DYNAMIC — only shows sections relevant to course config

## Image CSS

```css
.figure-box { background:#141820; border:1px solid #1E2433; border-radius:10px; padding:12px; margin:16px 0; text-align:center; }
.figure-box img { max-width:100%; border-radius:6px; }
.figure-caption { font-size:12px; color:#6E7191; margin-top:8px; font-style:italic; }
```

---

## Content Quality Standard

**Target reader: a student encountering this material for the first time.** Never assume prior knowledge beyond earlier chapters. If a previous concept is needed, briefly remind the reader.

Before presenting HTML output, verify:
- [ ] Every solution has: thought process, setup, full steps, answer, tips
- [ ] Every reference item has: explanation, when to use, when NOT to use, examples
- [ ] No steps skipped in any solution or proof
- [ ] Every variable/component has an interactive pill
- [ ] Uploaded images embedded and captioned
- [ ] Visual-setup problems have diagrams (uploaded or SVG)
- [ ] Color coding consistent throughout
- [ ] Menu bar matches course configuration (no phantom sections)
- [ ] Progress tracker includes all added content with correct hierarchy
- [ ] Assessment prep sections match course structure (tests/midterms/quizzes/final)
- [ ] KaTeX renders correctly, code blocks highlighted (CS)
- [ ] Space Grotesk + Deep Space palette applied
