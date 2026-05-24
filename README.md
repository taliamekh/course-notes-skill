# Course Notes Skill

A skill that turns lecture material into interactive, color-coded HTML study notes for university courses. Built around a single-page web app with chapters, worked examples, assignment solutions, a reference sheet, per-assessment prep sections, and a checkpoint-based progress tracker that persists locally.

Works with any AI assistant that supports skills or custom instructions. Cross-conversation memory is handled through a **`progress.md` file in a GitHub repo** — so a new chat can pick up exactly where the last one left off without re-explaining anything. **NotebookLM** can optionally supplement this for source material querying.

## How it works

1. **One-time course setup.** First time a new course is mentioned, the skill asks four questions: course name + code, course structure (tests / midterm / final / assignments / labs / quizzes), how content is organized (chapters / lectures / modules), and theme choice. The answers are saved in `progress.md` inside the course's GitHub repo.

2. **Material is added chapter by chapter** — uploaded slides, textbook PDFs, handwritten notes, assignment sheets, past exams. The skill reads every page, inventories diagrams and figures, and decides what to embed vs. transcribe.

3. **Cross-chapter memory via `progress.md`.** Before writing a new chapter, the skill pulls a concepts index from `progress.md` that lists every concept and formula already covered. Anything previously defined gets a back-reference ("recall from Ch2 that F=ma"), not a re-explanation. After writing, the index is updated so the next chapter does the same. NotebookLM can optionally supplement this for querying source material, but isn't required.

4. **HTML output.** Notes are rendered as a styled single-page app with:
   - A **dynamic menu** that only shows sections relevant to the course (no "Midterm prep" if there's no midterm)
   - **Color-coded content blocks** for equations, definitions, tips, derivations, worked examples, and units
   - **Full solutions** with thought process → setup → step-by-step work → boxed answer → exam tips, built from scratch as a teaching artifact
   - A **reference sheet** where every equation/theorem/algorithm/framework is a mini-lesson (statement → plain-english meaning → origin → when to use → when NOT to use → examples)
   - **Per-assessment prep sections** generated from the course config (Test 1, Test 2, Midterm, Final, etc.) — each with scope banner, topic checklist, condensed review, must-know items, practice problems, and solved past exams
   - A **progress tracker** with hierarchical checkboxes and checkpoint dividers at each test/midterm/final, persisting via `localStorage`

5. **Subject-aware vocabulary.** The same structure adapts to engineering (FBDs, unit analysis), math (proofs, lemmas), stats (distributions, hypothesis tests), CS (pseudocode, Big-O, trace tables), or business (frameworks, case studies). Workflow and theme don't change — only the content blocks do.

## Smart task routing

Not every interaction needs the full workflow. The skill classifies tasks into tiers to avoid loading unnecessary context:

| Tier | When | What loads |
|---|---|---|
| **1 — Targeted fix** | "Fix the sidebar color," "the popup is broken" | Only the named file |
| **2 — Scoped addition** | "Solve these problems for Ch3," "add Test 2 prep" | Relevant fragment files |
| **3 — New chapter** | "Write Chapter 6 notes from these slides" | `progress.md` + chapter fragments |
| **4 — New course** | "I'm starting a new course" | Nothing — runs setup questions |

## Themes

30 themes are available, each with a complete color set (equations, definitions, tips, derivations, examples, units) and a paired Google Font. Users can pick by name or number, preview before committing, or save a default with "make this my default."

**Live preview:** [taliamekh.github.io/course-notes-skill/references/theme-previews.html](https://taliamekh.github.io/course-notes-skill/references/theme-previews.html)

<details>
<summary>Full theme list</summary>

| # | Theme | Vibe |
|---|---|---|
| 1 | Deep Space | Dark purple cosmos with teal and gold pops |
| 2 | Pastel Dream | Soft dreamy pastels on warm white |
| 3 | Pink Cloud | Blush pink with rose, orchid, coral |
| 4 | Hacker Terminal | Green-on-black retro terminal |
| 5 | VS Code Dark | Dark+ with official syntax colors |
| 6 | Earth & Stone | Warm terracotta, moss green, sandstone |
| 7 | Notebook Classic | Lined paper with blue ink and red margin |
| 8 | Grid Paper | Engineering grid with pencil-grey tones |
| 9 | Botanical Garden | Sage greens, soft pinks, cream |
| 10 | Ocean Depths | Deep sea blues with bioluminescent accents |
| 11 | Sunset Gradient | Warm oranges and pinks into purple |
| 12 | Forest Canopy | Deep woodland greens with autumn gold |
| 13 | Arctic Frost | Ice whites and pale blues, crisp and clean |
| 14 | Lavender Fields | Soft purples and lilacs on light mauve |
| 15 | Midnight Navy | Classic navy with blue and cream accents |
| 16 | Engineering Blueprint | Blueprint blue-on-white with drafting feel |
| 17 | Med School | Clinical white with anatomy accents |
| 18 | Business Formal | Charcoal and navy with gold accents |
| 19 | CS Terminal | Dark IDE with syntax rainbow highlights |
| 20 | Law Review | Cream parchment with burgundy and navy |
| 21 | Chemistry Lab | Periodic-table with element colors |
| 22 | Architecture Studio | Minimalist concrete with precise lines |
| 23 | Math Chalkboard | Dark green chalkboard with chalk text |
| 24 | Art Studio | Handpainted bold expressive on canvas |
| 25 | Neon Cyberpunk | Electric neons on pitch black |
| 26 | Vintage Library | Aged paper with warm leather-brown |
| 27 | Mint Fresh | Cool mint green with clean white |
| 28 | Cherry Blossom | Japanese-inspired pink and white |
| 29 | Coffee Shop | Warm espresso browns and creamy latte |
| 30 | Northern Lights | Aurora — green, violet, blue on arctic sky |

</details>

## Installation

This is an AI skill — it needs to live inside an AI product that supports custom instructions or skills.

### 1. Download the skill

**Option A — Clone with git:**

```bash
git clone https://github.com/taliamekh/course-notes-skill.git
```

**Option B — Download as ZIP:**

[Download main.zip](https://github.com/taliamekh/course-notes-skill/archive/refs/heads/main.zip), then extract it and rename the resulting folder from `course-notes-skill-main` to `course-notes`.

### 2. Install in your AI tool

Place the skill folder where your AI tool reads custom skills or instructions. This varies by platform:

| Platform | Typical location |
|---|---|
| Claude Code / Desktop | `~/.claude/skills/course-notes/` |
| Claude.ai (web) | Settings → Capabilities → Skills → upload |
| Other AI tools | Check your tool's custom instructions or skills documentation |

After install, open a new chat so the skill gets picked up.

### 3. NotebookLM (optional)

NotebookLM adds the ability to query source material (textbook PDFs, lecture slides) directly from within the workflow. The core skill works fully without it — `progress.md` handles all cross-session memory and cross-chapter referencing.

If you want the supplement:

```bash
pip install notebooklm-mcp-cli
nlm login
```

Then grab the `.mcpb` extension from [jacob-bd/notebooklm-mcp-cli/releases](https://github.com/jacob-bd/notebooklm-mcp-cli/releases) and install it in your AI tool's MCP/extension settings.

### 4. Use it

Just ask. The skill triggers whenever you mention course notes, lecture notes, an assignment, exam prep, or a specific class — e.g.:

- *"Write notes for Chapter 3 of my Dynamics class"*
- *"Help me prep for my MECH 2005 midterm"*
- *"Fix the sidebar toggle on my notes"*

## Repository contents

The skill uses a multi-file architecture to keep context lean. The main `SKILL.md` contains the core workflow (~380 lines), while detailed specs live in reference files that only load when the task requires them.

```
SKILL.md                              Core workflow, task routing, setup, structure
references/
  themes.md                           30-theme color table, font options, UI specs
  component-styles.md                 Card, sidebar, pill, and chapter title CSS
  formula-sheet-spec.md               KaTeX popups, 3-view toggle, variable coloring
  diagram-rules.md                    SVG generation, label collision math
  solution-pipeline.md                7-step solution format, assessment prep, progress tracker
  summary-spec.md                     Concept clusters, What/Why/How format, quick ref table
  theme.md                            Deep Space component templates (work with any theme)
  theme-previews.html                 Static preview of all 30 themes side-by-side
scripts/
  push_to_github.py                   GitHub Contents API push (base64 encode + PUT)
```

## License

MIT — use it, fork it, theme it.
