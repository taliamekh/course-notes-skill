---
name: course-notes
description: >
  Interactive course notes with 30 selectable themes. Supports engineering, math, stats, CS, business, physics,
  and any university course. Trigger on: class notes, lecture notes, chapter notes, equation sheets, formula sheets,
  theorem references, algorithm references, assignment solutions (PA, homework, labs), test/midterm/final exam prep,
  course progress tracking, study notes, practice problems, chapter examples, worked examples, proofs, derivations,
  code walkthroughs, case studies, quiz prep, diagrams, or uploading images of notes, textbook pages, lecture slides,
  or handwritten work. Also trigger when updating or viewing previously created notes, fixing bugs in existing notes,
  or changing themes/styles. Always use this skill for academic note-taking even if the user doesn't name a specific
  subject — if they mention a course, class, or studying, this skill applies.
---

# Course Notes System

A structured note-taking system that creates interactive, color-coded HTML note pages for university courses. Every solution, concept, and reference item is explained from scratch for someone learning the material for the first time.

## Architecture Overview

- **Modular file system** — each chapter, problem set, and shared section lives in its own HTML fragment file in a GitHub repo. A `build.py` script assembles them into one viewable HTML page. Only edit the specific fragments needed for each task.
- **`progress.md`** — the session bridge. Contains the fetch guide (which files to load per task type), concepts index (what every chapter covers), and session log. Lives in the GitHub repo. Only fetched when the task requires cross-chapter context.
- **`project-rules.md`** at the repo root provides project rules and directives.
- **GitHub API push** — changed files are pushed via `scripts/push_to_github.py`. No manual downloads or terminal commands.
- **NotebookLM** (optional supplement) — if connected, useful for querying source material (textbook PDFs, slides). Not required for any core workflow. See "NotebookLM Integration" section below.
- **Uploaded files** — read from disk page-by-page for detailed content extraction and image embedding.

## Reference Files

This skill uses reference files to keep context lean. Load them only when the task requires it:

| File | When to read |
|---|---|
| `references/themes.md` | Picking or applying a theme, changing fonts, course setup Question 4 |
| `references/component-styles.md` | Generating or editing HTML output (cards, sidebar, pills, chapter titles) |
| `references/formula-sheet-spec.md` | Building or updating the formula/reference sheet |
| `references/diagram-rules.md` | Generating SVG diagrams for problems or concepts |
| `references/solution-pipeline.md` | Solving any problems, building assessment prep, updating progress tracker |
| `references/summary-spec.md` | Building or updating the summary page |
| `references/theme.md` | Component templates (structural, works with any theme's colors) |

---

## Step 0 — Classify the Task

Before fetching anything, determine what the user is asking for. Not every interaction needs the full workflow or `progress.md`. Match the task to a tier and fetch only what's needed:

### Tier 1 — Targeted Fix (fetch only the named file)

The user identifies a specific file or describes a specific bug. No cross-chapter context needed.

Examples: "fix the sidebar toggle," "the formula popup is clipping," "change the font in shell-head," "the active menu color is wrong"

**Workflow:** Fetch the named file(s) from the repo → fix the issue → rebuild with `build.py` → push changed files. No `progress.md` needed. No session log update needed for cosmetic fixes.

### Tier 2 — Scoped Addition (fetch relevant fragments directly)

Adding content that doesn't need cross-chapter referencing. The user provides the material or context.

Examples: "solve these 5 problems for Chapter 3," "add Test 2 prep — it covers Ch 4-6," "here's a practice exam, solve it," "update the progress tracker"

**Workflow:** Fetch the specific fragment files needed (e.g. `ch3-prob.html`, `t2prep.html`) → build the content → rebuild → push. Fetch `progress.md` only if you need to look up which chapters a test covers and the user hasn't told you. Update session log if substantial content was added.

### Tier 3 — New Chapter (fetch progress.md first)

Writing a new chapter that requires cross-referencing with previous chapters to avoid re-explaining concepts.

Examples: "here's Chapter 6, write the notes," "add lecture 12 notes from these slides"

**Workflow:** Fetch `progress.md` → read the concepts index to know what's already defined → fetch the chapter's fragment files per the fetch guide → read uploaded source material → write the chapter → update formulas, summary, progress → update `progress.md` (concepts index + session log) → rebuild → push everything.

### Tier 4 — New Course Setup (nothing to fetch)

The user is starting a brand new course.

**Workflow:** Run the setup questions → create the repo structure → push initial files. See "Course Setup" below.

---

## How Cross-Session Memory Works

AI assistants have no memory between conversations. `progress.md` in the GitHub repo bridges that gap — but only when needed (Tier 3 tasks).

**`progress.md` contains:**
1. **Course config** — name, subject, theme, assessments, content organization
2. **Fetch guide** — which files to load for each task type
3. **Concepts index** — what every chapter covers: concepts defined, formulas introduced, key examples, cross-references
4. **Session log** — what was done in previous sessions

**`progress.md` is compact by design** — a full semester fits in a few hundred lines. It's a map of what lives where, not the full notes.

**Cross-referencing rules:**
- If a concept was defined in a previous chapter, DON'T re-explain it — write "see Section X.Y" or "recall from Ch2 that F=ma"
- If a formula from a previous chapter is USED but not the focus, show it briefly with a back-reference
- If a concept is being EXTENDED, give a one-line reminder and then extend
- NEVER load previous chapter fragment files — use the concepts index

---

## The No-Regression Rule

This is the single most important structural guarantee. It appears once here and applies everywhere:

**When adding new content, ALL existing content in OTHER fragment files must remain EXACTLY as it was.** Never open, read, or modify fragment files that aren't being actively worked on. The modular file system enforces this structurally — each chapter lives in its own file, and `build.py` just concatenates. A student who studied from Ch1 notes will find them unchanged after Ch5 is added because `ch1-notes.html` was never touched.

**Prohibited patterns:**
- ❌ "Let me fetch all the chapter files to understand the structure" → Read `progress.md` concepts index instead
- ❌ "Let me read ch1-notes.html to see how Ch1 was formatted" → Use the skill's component templates
- ❌ "I'll regenerate the full HTML from the fragments" → Run `build.py`
- ❌ "The build script isn't available, so I'll assemble manually" → Fetch `build.py` from the repo

---

## Subject Detection and Adaptation

When the user names a course, detect the subject category and adapt the note structure. The sidebar, theme, image pipeline, and solution detail level are the same across ALL subjects. What changes is vocabulary and specialized content blocks.

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

## Course Setup — RUN ONCE PER NEW COURSE (Tier 4)

The very first time the user creates notes for a new course, prompt them for their course structure BEFORE doing anything else.

Ask the user (use the `ask_user_input` tool where possible, free text for specifics):

**Question 1: "What's the course name and code?"**
Free text — e.g., "MECH 2005 — Dynamics"

**Question 2: "What's your course structure?"**
Free text — prompt with examples:
- "How many tests/midterms? Is the final cumulative?"
- "How many assignments or PAs? Any labs or projects?"
- "Any quizzes? Weekly, bi-weekly?"
- "Do you know the grade weights?"

Parse whatever they give you. Extract: assessment type, count, and any notes.

**Question 3: "How is the course content organized?"**
Single-select: By chapters / By lectures / By modules / Mix

**Question 4: "Pick a theme for your notes (default: Deep Space)."**
Read `references/themes.md` for the full 30-theme list. Check `progress.md` for a `_USER_THEME_DEFAULT` entry (or NotebookLM if connected). After picking, ask: "Happy with the font, or want to swap it?"

**Store the configuration** in `progress.md` header:
```
Course: MECH 2005 — Dynamics
Subject: Engineering
Content org: Chapters
Theme: Deep Space
  Background: #0B0E14
  Accents: #AD8CFF, #56D6C1, #FFD866
  Font: Space Grotesk
Assessments:
  - Assignments: 8 (PA1–PA8)
  - Tests: 3 (Test 1, Test 2, Test 3)
  - Final: yes (cumulative)
Chapters: [populated as content is added]
```

This configuration drives the sidebar (no "Midterm prep" if the course has tests), the progress tracker, and assessment prep sections.

**If the user dives straight in** ("here are my Chapter 1 notes") without doing setup, infer what you can from context and ask remaining questions in a lightweight way — don't block them.

---

## Incremental Chapter Addition — Tier 3 Workflow

**Step 0 — Fetch `progress.md`.**
```bash
curl -sL "$RAW_BASE_URL/progress.md" -o ./progress.md
```
Read it. Do NOT fetch any other files until you've read the fetch guide.

**Step 1 — Fetch ONLY the files listed in the fetch guide.**
For Chapter N, typically: `chapters/chN-notes.html`, `chapters/formulas.html`, `chapters/summary.html`, `chapters/progress.html`, `shell-head.html`.

**Step 2 — Read the new chapter's source material.**
Textbook pages (scoped by TOC if available), lecture notes, uploaded slides, problem sets, user-provided content.

**Step 3 — Edit the fragment files.**

| File | Edit type | What to do |
|------|-----------|------------|
| `chN-notes.html` | Replace/rewrite | Replace placeholder with full chapter content |
| `chN-prob.html` | Replace/rewrite | Replace placeholder with solved recommended problems |
| `formulas.html` | Append | Add new chapter's formula cards at the end |
| `summary.html` | Append | Replace "Pending" placeholder with chapter's clusters |
| `progress.html` | Append | Add new chapter's progress items |
| `shell-head.html` | Small edit | Remove `pending` class from sidebar links |

For small fragment files (< 5KB), `create_file` (overwrite) is fine. For large files or append operations, use `str_replace`.

When generating HTML, read `references/component-styles.md` for card, sidebar, and pill CSS. When building formula sheet content, read `references/formula-sheet-spec.md`. When building summary content, read `references/summary-spec.md`.

**Step 4 — Rebuild and preview.**
```bash
curl -sL "$RAW_BASE_URL/build.py" -o ./build.py
python3 build.py
```
Present the built HTML for review.

**Step 5 — Push changed files.**
```bash
python3 scripts/push_to_github.py <filepath> <repo> <repo_path> "$TOKEN" "Add Chapter N notes"
```
Only push files that changed — typically 5-7, never all files.

**Step 6 — Update `progress.md`.**
Add the new chapter to the concepts index and append to the session log. Push `progress.md`.

---

## Handling Uploaded Files

The user will upload lecture slides, textbook pages, handwritten notes, assignment sheets, and exams.

### Textbook Scoped Reading

When the user uploads the course textbook PDF and asks to write a chapter:
1. Check `progress.md` for textbook page ranges (or NotebookLM `_TEXTBOOK_TOC` if available)
2. Cross-reference the chapter with the TOC to get the exact page range
3. Read ONLY those pages using pdf-reading tools — not the entire textbook
4. This does NOT apply to lecture notes, exams, assignments — those are typically short enough to read fully

### Image Extraction Pipeline

**Step 1: Scan the entire upload.** Read/view every page (or scoped chapter pages for textbooks). Build an inventory of diagrams, figures, examples, derivation steps, tables, code samples.

**Step 2: Extract important images selectively.** For PDFs: `pdftoppm -f {page} -l {page} -png input.pdf output`. Only extract pages with visual content — not every page.

**Step 3: Decide what to embed.**

| Content type | Embed? |
|---|---|
| Problem statement / exam question | YES always |
| Diagram, FBD, flowchart, sketch | YES always |
| Textbook figure, graph, plot | YES always |
| Code output / terminal screenshot | YES always |
| Slide with only bullet text | NO — transcribe |
| Professor handwriting | YES + typed clean version alongside |

**Step 4: Convert and embed.** Base64-encode each image, embed as `<img src="data:image/png;base64,...">` inside a `.figure-box` container with caption.

**Step 5: Generate diagrams when none exist.** Read `references/diagram-rules.md` for SVG generation specs.

---

## Skeleton-First Build Order (New Course)

When generating a course notes file system for the first time:

1. **Create the full skeleton FIRST** — `shell-head.html` with CSS and sidebar, `shell-foot.html` with JS, placeholder fragments for every chapter/section
2. **Populate the sidebar immediately** with all menu items from the config — pending items styled with lighter color but still clickable
3. **Create `build.py`** that assembles all fragments
4. **Create `progress.md`** with fetch guide, empty concepts index, initial session log
5. **Create `project-rules.md`** with project rules
6. **Formula sheet, Summary, and Progress are live from the start** — they begin with whatever content exists and grow incrementally. NEVER "generated after all chapters"
7. **When a new chapter is added**, also update: `formulas.html`, `summary.html`, `progress.html`
8. **Push all files to GitHub** via the push script

### Repo Structure

```
{repo}/
├── project-rules.md       ← project rules and directives
├── progress.md            ← session state, fetch guide, concepts index
├── build.py               ← assembles fragments into one HTML
├── shell-head.html        ← CSS, sidebar, opening tags
├── shell-foot.html        ← JS, closing tags
├── {COURSE}-notes.html    ← built output (view this, don't edit directly)
└── chapters/
    ├── ch{N}-notes.html   ← chapter notes (one per chapter)
    ├── ch{N}-prob.html    ← recommended problems (one per chapter)
    ├── formulas.html      ← formula/theorem sheet (appended each chapter)
    ├── summary.html       ← course summary (appended each chapter)
    ├── progress.html      ← progress tracker (appended each chapter)
    ├── t{N}prep.html      ← test prep pages
    └── final.html         ← final exam prep
```

Fragment files ARE the source of truth. The built `{COURSE}-notes.html` is a derived artifact.

---

## Note Page Structure

The sidebar is DYNAMIC — built from the course configuration. Only sections relevant to the course are shown.

| Menu item | Shown when |
|---|---|
| Chapters / Lectures / Modules | Always |
| └ Recommended Problems (sub-link per chapter) | Always — nested under each chapter |
| Assignments (PA / HW / Labs) | Course has assignments |
| Reference sheet | Always |
| Test 1 prep, Test 2 prep, etc. | Course has multiple tests |
| Midterm prep | Course has a single midterm |
| Final prep | Course has a final |
| Quiz prep | Course has quizzes |
| Summary | Always |
| Progress | Always |

For detailed specs on each section, read the relevant reference file:
- Solutions/problems → `references/solution-pipeline.md`
- Formula sheet → `references/formula-sheet-spec.md`
- Summary → `references/summary-spec.md`
- Assessment prep → `references/solution-pipeline.md`
- Progress tracker → `references/solution-pipeline.md`
- Diagrams → `references/diagram-rules.md`
- Cards/sidebar/pills → `references/component-styles.md`

---

## NotebookLM Integration (Optional)

NotebookLM is a useful supplement but the entire workflow functions without it. If the user has NotebookLM MCP tools connected, use them as a bonus layer. If not, skip gracefully.

**With NotebookLM available:**
- `notebook_query` — ask questions about uploaded source material (textbook PDFs, slides)
- `source_get_content` — pull raw text from sources for detailed extraction
- `source_add` — user can upload course materials for querying
- `note` (create/update) — mirror `_COURSE_CONFIG` and `_TEXTBOOK_TOC` as notes for supplemental access
- `studio_create` — generate study artifacts (flashcards, quizzes, audio overviews)

**Without NotebookLM:**
- Cross-referencing uses `progress.md` concepts index (always the primary source)
- Source material comes from uploaded files read from disk
- Config lives in `progress.md` header (always the authoritative source)
- Theme defaults stored in `progress.md` global section
- Flashcards/quizzes can be generated directly as HTML

**Available NotebookLM MCP tools (when connected):**
`notebook_create`, `notebook_get`, `notebook_query`, `notebook_describe`, `note` (create/list/update/delete), `source_add` (url/text/drive/file), `source_get_content`, `source_describe`, `label`, `studio_create`

---

## Content Quality Standard

**Target reader: a student encountering this material for the first time.** Never assume prior knowledge beyond earlier chapters.

**Completeness is non-negotiable.** Every concept, formula, theorem, definition, proof sketch, and example from the source material must appear. No steps skipped in derivations or solutions.

### Pre-Output Checklist

Before presenting HTML output, verify:
- [ ] Every solution follows the full pipeline (read `references/solution-pipeline.md`)
- [ ] Every reference item has: explanation, when to use, when NOT to use, examples
- [ ] No steps skipped in any solution or proof
- [ ] Chapter notes: every variable has a neutral pill below the formula
- [ ] Formula sheet: every variable is color-coded with working popup (read `references/formula-sheet-spec.md`)
- [ ] Uploaded images embedded and captioned
- [ ] Visual-setup problems have diagrams (read `references/diagram-rules.md`)
- [ ] Card borders use `border-left` on the card (not `::before` pseudo-elements)
- [ ] Sidebar colors match theme (read `references/component-styles.md`)
- [ ] Chosen theme palette and font applied consistently (read `references/themes.md`)
- [ ] No concept re-explained if already defined in a previous chapter
- [ ] **NO REGRESSION**: only the specific fragment files being edited were modified
- [ ] **FRAGMENTS ONLY**: edits were made to fragment files, never to the built output
- [ ] **BUILD SCRIPT USED**: `build.py` was run, not manual concatenation
- [ ] **GITHUB PUSHED**: changed files were pushed via push script (if token available)
- [ ] Formula sheet has all 3 toggle views working
- [ ] Tip labels have ★ prefix
