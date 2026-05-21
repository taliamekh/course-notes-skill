---
name: course-notes
description: >
  Interactive course notes with 30 selectable themes. Supports engineering, math, stats, CS, business, physics,
  and any university course. Trigger on: class notes, lecture notes, chapter notes, equation sheets, formula sheets,
  theorem references, algorithm references, assignment solutions (PA, homework, labs), test/midterm/final exam prep,
  course progress tracking, study notes, practice problems, chapter examples, worked examples, proofs, derivations,
  code walkthroughs, case studies, quiz prep, diagrams, or uploading images of notes, textbook pages, lecture slides,
  or handwritten work. Also trigger when updating or viewing previously created notes.
  Uses NotebookLM MCP for cross-chapter referencing, source querying, and running index storage.
  Always use this skill for academic note-taking even if the user doesn't name a specific subject —
  if they mention a course, class, or studying, this skill applies.
---

# Course Notes System

A structured note-taking system that creates interactive, color-coded HTML note pages for university courses. Every solution, concept, and reference item is explained from scratch for someone learning the material for the first time.

## Setup & Prerequisites

### Required: NotebookLM MCP Extension
This skill relies on the **NotebookLM MCP Server** extension for Claude Desktop. It must be installed before using this skill.

**How to install (one-time):**
1. Install the Python package: `pip install notebooklm-mcp-cli`
2. Authenticate: `nlm login` (opens browser, sign into Google)
3. Download the `.mcpb` extension file from https://github.com/jacob-bd/notebooklm-mcp-cli/releases
4. In Claude Desktop: **Settings → Extensions → Install Extension** → select the `.mcpb` file
5. Restart Claude Desktop

### How It Works
- **NotebookLM** holds all course source material (PDFs, slides, lecture notes) and acts as a persistent knowledge base across conversations
- **Uploaded files** (sent directly to Claude) are read from disk page-by-page for detailed content extraction and image embedding
- **NotebookLM queries** handle cross-chapter referencing ("was this concept already covered?") without needing all chapters in context
- **A running index** (stored as a note in NotebookLM) tracks every concept, formula, and definition by chapter so notes stay coherent and never redundantly re-explain material
- **HTML output** goes to `/mnt/user-data/outputs/` for the user to push to their website/repo

### Workflow Summary
1. User uploads course materials to a NotebookLM notebook (via notebooklm.google.com or `source_add`)
2. User sends chapter-by-chapter material to Claude (uploaded files or pasted text)
3. Claude reads uploaded files from disk for full detail, queries NotebookLM for cross-referencing
4. Claude generates styled HTML notes and updates the running index
5. User downloads HTML and pushes to their website repo

### How Claude Remembers Across Conversations
Claude has no memory between conversations. The `_CONCEPTS_INDEX` note in NotebookLM is what bridges that gap. Here is what happens every time:

**Start of every note-writing session (even in a new conversation):**
1. Claude retrieves the `_CONCEPTS_INDEX` note from NotebookLM via `note` (action: list) → read content
2. This tells Claude exactly what every previous chapter covered: concepts defined, formulas introduced, key examples, and which chapters reference each other
3. Claude uses this to decide what to skip, what to back-reference, and what's new

**End of every note-writing session:**
1. Claude updates `_CONCEPTS_INDEX` via `note` (action: update) with the new chapter's concepts, formulas, cross-references, and key examples
2. This ensures the NEXT conversation (even days later) picks up exactly where this one left off

**If the user asks Claude to write Chapter 5, Claude will:**
1. Pull `_CONCEPTS_INDEX` → see Ch1–Ch4 summaries
2. Pull `_COURSE_CONFIG` → know the course structure and assessments
3. Query NotebookLM with `notebook_query` if anything is unclear ("did Chapter 3 cover beam deflection or just shear/moment diagrams?")
4. Read the uploaded Chapter 5 material from disk page-by-page for full detail
5. Write Chapter 5 notes, referencing earlier chapters instead of re-explaining
6. Update `_CONCEPTS_INDEX` with Chapter 5's additions

**The index is compact by design** — a full semester fits in a few hundred lines, well within context limits. It's not the full notes, just a map of what lives where.

## Theme

The default theme is **Deep Space** — the original theme this skill was built with. Its full reference (color tokens, component templates, SVG palette) lives in `references/theme.md`. If the user picks a different theme in Question 4, substitute that theme's colors and font into the same component templates. If they skip Question 4 or say "default", use Deep Space.

**User default preference:** If a user says "make X my default theme", store it in NotebookLM as a note titled `_USER_THEME_DEFAULT` with the theme name, colors, and font. Future courses will use that theme unless overridden in Question 4. If no `_USER_THEME_DEFAULT` note exists, Deep Space is the default.

**Theme preview:** If the user asks to preview a theme before committing, generate a small static HTML file showing: background color, 4 accent color swatches with labels, a font sample (heading + body text), and a mock menu bar with 3-4 placeholder items. This is NOT interactive — just a visual preview saved to `/mnt/user-data/outputs/theme-preview.html`.

**Notebook-style themes (7, 8, 9):** These use CSS background patterns (repeating lines, grid dots, or cork texture) in addition to colors. The grid/lines are subtle and should not interfere with readability.

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

**Question 2: "What's your course structure? List all assessments — tests, midterms, finals, assignments, labs, quizzes, projects — and how many of each."**
Free text — prompt with examples so the user knows what to include:
- "How many tests/midterms? Is the final cumulative?"
- "How many assignments or PAs? Any labs or projects?"
- "Any quizzes? Weekly, bi-weekly?"
- "Do you know the grade weights?"

Example answers:
- "3 tests, 8 assignments, 1 final (cumulative), no labs"
- "1 midterm, 1 final, 6 PAs, 4 labs, weekly quizzes"
- "2 midterms (30% each), 1 final (40%), 5 homework sets"

Parse whatever they give you. Extract: assessment type, count, and any notes (cumulative, weighted, etc.). If something is ambiguous ("tests" vs "midterms"), don't ask — just use their terminology.

**Question 3: "How is the course content organized?"**
Single-select:
- By chapters (textbook-driven)
- By lectures (lecture-driven)
- By modules/units
- Mix of the above

**Question 4: "Pick a theme for your notes (default: Deep Space)."**
Check NotebookLM for a `_USER_THEME_DEFAULT` note first — if one exists, use that as the default instead of Deep Space and tell the user: "Your default theme is {X}. Want to keep it or pick a different one?"

If no user default exists, present the 30 themes below by name and one-line description. The user can:
- Pick a theme by name or number
- Say "default" or skip to use Deep Space
- Ask to preview any theme before committing (generates a non-interactive mini preview)
- Say "make this my default" to save their choice as the default for all future courses

After picking a theme, ask: **"Happy with the font, or want to swap it?"** and offer the font list below.

### 30 Available Themes

Each theme defines 6 color-coded roles used throughout the notes:
- **Equations** (primary) — equation cards, formula highlights
- **Definitions** (secondary) — definition blocks, concept explanations
- **Tips** (tertiary) — tip callouts, exam warnings, key insights
- **Derivations** — step-by-step derivation chains, proofs
- **Examples** — worked examples, PA solutions
- **Units** — unit analysis blocks, conditions

**Equation coloring rule:**
- In **chapter notes and solutions**: equations/formulas are displayed in the **equation accent color**. Variables are NOT individually color-coded — they use neutral variable pills (name + unit) below the formula.
- In the **formula/equation reference sheet only**: variables within formulas ARE color-coded with their own distinct palette. This palette is **theme-specific** — each theme can define as many variable colors as needed, as long as they stay visually on-theme and are consistent every time that theme is used.

**Theme independence — CRITICAL:**
Each theme defines its OWN complete color set. Do NOT fall back to Deep Space colors for any theme. Every theme specifies:
- Title/heading color (used for page titles, chapter headings)
- 6 content-type colors (equations, definitions, tips, derivations, examples, units)
- Menu text colors (active + inactive)
- Background, surface, border, text, muted text
- Equation name color (lighter shade of equation color)
- Variable pill colors for the equation/formula sheet (as many as needed, all on-theme)

When generating notes for a non-Deep Space theme, pull ALL colors from that theme's definition — never mix in Deep Space defaults. The `references/theme.md` file contains component TEMPLATES (equation cards, callouts, step blocks, etc.) that work with any theme by substituting the chosen theme's colors. The templates are structural, not color-specific.

**Showing previews:** When the user asks to see themes, copy `references/theme-previews.html` to `/mnt/user-data/outputs/` and present it. Do NOT regenerate the preview — it's a static reference file that ships with the skill. If the user asks to preview a SINGLE theme in detail, then generate a focused one-theme preview on the fly.

**Menu readability:** Every theme must define a `menuTxt` color (inactive sidebar items) and `menuActive` color (active item) that have sufficient contrast against the sidebar background. For dark themes, inactive text should be at least `#6A6A6A` brightness. For light themes, inactive text should be no lighter than `#7A7A7A`. Test this visually — if you can't read the menu, the color needs to be darker (light themes) or brighter (dark themes).

| # | Theme Name | Description | Background | Accents | Font |
|---|---|---|---|---|---|
| 1 | **Deep Space** | Dark purple cosmos with teal and gold pops | #0B0E14 | #AD8CFF, #56D6C1, #FFD866 | Space Grotesk | Title: #7B5EC7 (deep purple) |
| 2 | **Pastel Dream** | Soft muted pastels on a warm white base | #FFF8F0 | #C47090, #60A88A, #C4983E, #7088BE | DM Sans |
| 3 | **Pink Cloud** | Blush pink with warm rose, orchid, and coral | #FFF0F5 | #C45080, #8A70B0, #C48870, #A06098 | Nunito |
| 4 | **Hacker Terminal** | Green-on-black retro terminal aesthetic | #0A0A0A | #00FF41, #00CCDD, #FFFF00, #4488FF | Fira Code |
| 3 | **VS Code Dark** | Accurate Dark+ with official syntax colors | #1E1E1E | #569CD6, #4EC9B0, #DCDCAA, #CE9178, #6A9955, #C586C0 | JetBrains Mono | Sidebar: #252526, Title: #9CDCFE |
| 6 | **Earth & Stone** | Warm terracotta, moss green, and sandstone | #2C2416 | #C4835A, #8B9F6B, #D4B98C, #A67C52 | Bitter |
| 7 | **Notebook Classic** | Lined paper background with blue ink and red margin | #FDF6E3 | #2B5EA7, #D94040, #4A4A4A, #8B8B8B | Caveat |
| 8 | **Grid Paper** | Engineering grid paper with pencil-grey tones | #F5F5F0 | #4A90D9, #E85D5D, #5CAB7D, #888888 | Architects Daughter |
| 9 | **Botanical Garden** | Sage greens, soft pinks, and cream — illustrated botanical feel | #F8F5EE | #5B8C3E, #C46B8A, #D4960A, #4A7A9B | Cormorant Garamond |
| 10 | **Ocean Depths** | Deep sea blues with bioluminescent accents | #0A1628 | #00D4FF, #0088CC, #FF6B6B, #64FFDA | Inter |
| 11 | **Sunset Gradient** | Warm oranges and pinks fading into purple | #1A0A2E | #FF6B35, #FF9A8B, #C084FC, #FFD93D | Poppins |
| 12 | **Forest Canopy** | Deep woodland greens with autumn gold | #0D1F0D | #4CAF50, #8BC34A, #FFB74D, #A1887F | Merriweather |
| 13 | **Arctic Frost** | Ice whites and pale blues, crisp and clean | #F0F4F8 | #0277BD, #00838F, #1565C0, #3F51B5, #546E7A, #5E35B1 | Roboto |
| 14 | **Lavender Fields** | Soft purples and lilacs on a light mauve base | #F3E8FF | #7830C0, #6070C8, #B07040, #9850B8 | Fredoka |
| 15 | **Midnight Navy** | Classic navy with gold and cream accents | #0D1B2A | #FFD700, #E0E0CE, #1B4965, #5FA8D3 | Playfair Display |
| 16 | **Engineering Blueprint** | Blueprint blue-on-white with technical drafting feel | #F8FBFF | #1565C0, #0D47A1, #FF6F00, #E3F2FD | IBM Plex Mono |
| 17 | **Med School** | Clinical white with anatomy-illustration accents | #FAFAFA | #E53935, #1E88E5, #43A047, #F4511E | Source Sans 3 |
| 18 | **Business Formal** | Charcoal and navy with gold accents, boardroom ready | #1A1A2E | #E0C97F, #4A6FA5, #C8C8C8, #2D3A4A | Libre Franklin |
| 19 | **CS Terminal** | Dark IDE with syntax rainbow highlights | #282C34 | #61AFEF, #98C379, #E06C75, #D19A66 | Source Code Pro |
| 20 | **Law Review** | Cream parchment with burgundy and navy, classic serif | #FFFDF5 | #800020, #1B365D, #8B7355, #C8A96E | Crimson Text |
| 21 | **Chemistry Lab** | Periodic-table inspired with element-colored accents | #0F0F1A | #00BCD4, #FF9800, #8BC34A, #E91E63 | Rubik |
| 22 | **Architecture Studio** | Minimalist concrete with precise accent lines | #F5F5F5 | #333333, #FF4444, #0066CC, #E0E0E0 | Barlow |
| 23 | **Math Chalkboard** | Dark green chalkboard with chalk-white text | #2D4A3E | #FFFFFF, #FFE082, #EF9A9A, #A5D6A7 | Kalam |
| 24 | **Art Studio** | Creative splashes of color on a gallery-white canvas | #FFFFFF | #FF1744, #2979FF, #FFD600, #00E676 | Fredoka |
| 25 | **Neon Cyberpunk** | Electric neons on pitch black | #0A0A0A | #FF00FF, #00FFFF, #FF3366, #39FF14 | Orbitron |
| 26 | **Vintage Library** | Aged paper with warm leather-brown tones | #F5E6CA | #8B4513, #654321, #DAA520, #CD853F | Lora |
| 27 | **Mint Fresh** | Cool mint green with clean white and grey | #F0FFF4 | #38B2AC, #2D9CDB, #48BB78, #E2E8F0 | Outfit |
| 28 | **Cherry Blossom** | Japanese-inspired pink and white with soft grey | #FFF5F7 | #DB2777, #F472B6, #FDA4AF, #9CA3AF | Zen Maru Gothic |
| 29 | **Coffee Shop** | Warm espresso browns and creamy latte tones | #1C1410 | #C49A6C, #8B6B4A, #E8D5B7, #5C3D2E | Josefin Sans |
| 30 | **Northern Lights** | Aurora borealis — shimmering green, violet, and blue on arctic night sky with subtle glow effects | #070B18 | #00E676, #B388FF, #448AFF, #FF4081, #FFD54F, #18FFFF | Exo 2 |

### Font Swap Options
If the user doesn't like their theme's default font, offer these alternatives:
- **Sans-serif:** Inter, Outfit, DM Sans, Nunito, Poppins, Roboto, Barlow, Libre Franklin, Source Sans 3, Quicksand, Fredoka, Exo 2, Rubik, Sora
- **Serif:** Merriweather, Playfair Display, Lora, Crimson Text, Bitter
- **Monospace:** JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono, Space Mono
- **Handwritten:** Caveat, Patrick Hand, Kalam, Architects Daughter

The chosen theme and font are stored in `_COURSE_CONFIG` and applied to ALL HTML output for that course. Read `references/theme.md` for component templates — substitute the chosen theme's colors and font in place of the Deep Space defaults.

**Store this configuration.** Save it as a note in the NotebookLM notebook using the `note` tool (action: create) with title `_COURSE_CONFIG`:

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
  - Labs: 0
  - Quizzes: 0
Chapters: [populated as content is added]
```

Also create a `_CONCEPTS_INDEX` note (see Section 3 below) — this is the running index that tracks what each chapter covers to prevent redundant explanations across chapters.

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
If a problem has a visual setup but no image provided, generate an SVG using the chosen theme's palette. Also generate when: uploaded image is blurry, solution says "see diagram" with none provided, or CS/stats/business problems need flowcharts/trees/curves.

### 3. NotebookLM Integration — Cross-Referencing & Running Index

NotebookLM serves two purposes: (1) querying source material across chapters without loading everything into context, and (2) storing a running index that tracks what concepts have been covered and where.

**First time for a course:**
1. `notebook_create` with the course name as title
2. User uploads their course PDFs/slides to the notebook (via notebooklm.google.com or `source_add` with source_type: url/drive/file)
3. Create course config note: `note` (action: create, title: `_COURSE_CONFIG`, content: config from step 0)
4. Create concepts index note: `note` (action: create, title: `_CONCEPTS_INDEX`, content: empty template below)

**Running Concepts Index (`_CONCEPTS_INDEX`) — CRITICAL FOR COHERENCE**

This note is updated after EVERY chapter is written. It prevents redundant explanations and enables cross-referencing. Format:

```
CONCEPTS INDEX — MECH 2005 Dynamics
Last updated: Ch3

Ch1 — Kinematics of Particles:
  Defined: position, velocity, acceleration, rectilinear motion, projectile motion
  Formulas: v=ds/dt, a=dv/dt, s=s₀+v₀t+½at², projectile equations
  Key examples: 1.1 (rectilinear), 1.2 (projectile), 1.3 (curvilinear)

Ch2 — Force and Acceleration:
  Defined: Newton's laws, FBDs, normal/tangential components
  Formulas: F=ma, ΣF=ma component equations
  Refs Ch1: uses velocity/acceleration definitions from Ch1 (not re-explained)
  Key examples: 2.1 (incline), 2.2 (pulley system)

Ch3 — Work and Energy:
  Defined: work, kinetic energy, potential energy, conservation of energy
  Formulas: W=Fd·cosθ, KE=½mv², PE=mgh, work-energy theorem
  Refs Ch2: uses FBD approach from Ch2 for identifying forces (not re-explained)
  Key examples: 3.1 (spring system), 3.2 (roller coaster)
```

**Before writing a new chapter:**
1. Retrieve the `_CONCEPTS_INDEX` note: `note` (action: list) to find it, then read its content
2. Query NotebookLM if needed: `notebook_query` with questions like "What topics are covered in the Chapter 4 lecture slides?" or "Was thermal expansion already explained in earlier chapters?"
3. Use `source_get_content` to pull raw text from specific sources if you need full detail beyond what the uploaded files provide

**After writing a new chapter:**
1. Update `_CONCEPTS_INDEX` via `note` (action: update) with new chapter's concepts, formulas, cross-references
2. Optionally store the finished HTML summary as a text source via `source_add` (source_type: text) for future querying

**Cross-referencing rules:**
- If a concept was defined in a previous chapter, DON'T re-explain it — write "see Section X.Y" or "recall from Ch2 that F=ma"
- If a formula from a previous chapter is USED but not the focus, show it briefly with a back-reference
- If a concept is being EXTENDED (e.g., Ch1 defined velocity, Ch3 uses it in energy equations), give a one-line reminder and then extend

**Available NotebookLM MCP tools reference:**
- `notebook_create` — create a new notebook
- `notebook_get` — get notebook details and list of sources
- `notebook_query` — ask AI questions about sources in the notebook (for cross-referencing)
- `notebook_describe` — get AI summary of entire notebook
- `note` (action: create/list/update/delete) — manage notes (used for config + running index)
- `source_add` (source_type: url/text/drive/file) — add sources to notebook
- `source_get_content` — get raw text of a source (fast, no AI processing)
- `source_describe` — get AI summary of a single source
- `label` — organize sources into categories
- `studio_create` — generate study artifacts (flashcards, quizzes, audio overviews, etc.)

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

**Checkpoint styling (uses chosen theme):**
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

**Styling (uses chosen theme):**
- Checked: accent purple (#AD8CFF) checkbox fill
- Unchecked: surface (#141820) with border (#1E2433)
- Progress bar fill: gradient from purple to teal
- Section headers: text color with chevron toggle
- Percentage labels: muted (#6E7191)
- Checkpoint bars: distinct from regular sections — wider padding, gradient background, flag icon

---

## Diagram Generation

When no image provided, generate SVG using the chosen theme's palette:
- Outlines: primary and secondary accent colors
- Force arrows: color by type (use accent colors mapped to categories — e.g., gravity=warm accent, normal=cool accent, friction=gold/tertiary, applied=primary)
- Labels: light text color from theme, chosen font
- Dimensions: muted color, dashed
- Axes: blue accent or secondary
- Background: transparent

Subject types: Engineering → FBDs, mechanisms. Math → plots, constructions. Stats → curves, trees. CS → flowcharts, data structures. Business → supply/demand, process flows.

---

## HTML Generation Rules

1. Always load: KaTeX (cdnjs), chosen theme font (Google Fonts), Tabler Icons
2. For CS: also load Prism.js for syntax highlighting
3. Chosen theme palette exclusively (see `references/theme.md` for component templates, substitute chosen theme colors)
4. KaTeX: `\( inline \)` and `\[ display \]`
5. Interactive pills (click to expand), collapsible solutions/examples
6. Fixed menu bar (top), fixed sidebar (full-course view)
7. Embedded images in `.figure-box` containers with captions
8. SVG diagrams inline using theme colors
9. Sections as `<section id="{name}">` for anchor nav
10. Progress checkboxes persist via localStorage keyed by course name
11. Menu bar is DYNAMIC — only shows sections relevant to course config
12. For notebook-style themes (7, 8, 9): add CSS background patterns (lines, grid, cork texture)

## Image CSS

Use CSS variables derived from the chosen theme. Example for Deep Space (substitute with actual theme colors):

```css
.figure-box { background: var(--surface); border:1px solid var(--border); border-radius:10px; padding:12px; margin:16px 0; text-align:center; }
.figure-box img { max-width:100%; border-radius:6px; }
.figure-caption { font-size:12px; color: var(--muted); margin-top:8px; font-style:italic; }
```

Every theme should define these CSS variables at minimum: `--bg`, `--surface`, `--border`, `--text`, `--muted`, `--accent1`, `--accent2`, `--accent3`, `--accent4`.

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
- [ ] Chosen theme palette and font applied consistently (not hardcoded Deep Space unless that's the chosen theme)
- [ ] No concept is re-explained if it was already defined in a previous chapter (check _CONCEPTS_INDEX)
- [ ] Cross-references to earlier chapters use "see Section X.Y" or brief reminders, not full re-explanations
- [ ] _CONCEPTS_INDEX note updated in NotebookLM after chapter is complete
