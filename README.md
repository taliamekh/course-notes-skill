# Course Notes Skill

A Claude skill that turns lecture material into interactive, color-coded HTML study notes for university courses. Built around a single-page web app with chapters, worked examples, assignment solutions, a reference sheet, per-assessment prep sections, and a checkpoint-based progress tracker that persists locally.

Backed by **NotebookLM** for persistent course storage and cross-conversation memory — so a new chat can pick up exactly where the last one left off without re-explaining anything.

## How it works

1. **One-time course setup.** First time the user mentions a new course, the skill asks four questions: course name + code, course structure (tests / midterm / final / assignments / labs / quizzes), how content is organized (chapters / lectures / modules), and theme choice. The answers are saved as a `_COURSE_CONFIG` note inside a NotebookLM notebook for that course.

2. **The user adds material chapter by chapter** — uploaded slides, textbook PDFs, handwritten notes, assignment sheets, past exams. The skill reads every page, inventories diagrams and figures, and decides what to embed vs. transcribe.

3. **Cross-chapter memory via NotebookLM.** Before writing a new chapter, the skill pulls a `_CONCEPTS_INDEX` note that lists every concept and formula already covered. Anything previously defined gets a back-reference ("recall from Ch2 that F=ma"), not a re-explanation. After writing, the index is updated so the next chapter does the same.

4. **HTML output.** Notes are rendered as a styled single-page app with:
   - A **dynamic menu** that only shows sections relevant to the course (no "Midterm prep" if there's no midterm)
   - **Color-coded content blocks** for equations, definitions, tips, derivations, worked examples, and units
   - **Full solutions** with thought process → setup → step-by-step work → boxed answer → exam tips, never reformatted from source but built from scratch as a teaching artifact
   - A **reference sheet** where every equation/theorem/algorithm/framework is a mini-lesson (statement → plain-english meaning → origin → when to use → when NOT to use → examples)
   - **Per-assessment prep sections** generated from the course config (Test 1, Test 2, Midterm, Final, etc.) — each with scope banner, topic checklist, condensed review, must-know items, practice problems, and solved past exams
   - A **progress tracker** with hierarchical checkboxes and checkpoint dividers at each test/midterm/final, persisting via `localStorage`

5. **Subject-aware vocabulary.** The same structure adapts to engineering (FBDs, unit analysis), math (proofs, lemmas), stats (distributions, hypothesis tests), CS (pseudocode, Big-O, trace tables), or business (frameworks, case studies). Workflow and theme don't change — only the content blocks do.

## Themes

30 themes are available, each with a complete color set (equations, definitions, tips, derivations, examples, units) and a paired Google Font. Users can pick by name or number, preview before committing, or save a default with "make this my default."

**Live preview:** [taliamekh.github.io/course-notes-skill/references/theme-previews.html](https://taliamekh.github.io/course-notes-skill/references/theme-previews.html)
*(may take a minute to deploy after first enabling GitHub Pages)*

<details>
<summary>Full theme list</summary>

| # | Theme | Vibe |
|---|---|---|
| 1 | Deep Space | Dark purple cosmos with teal and gold pops |
| 2 | Hacker Terminal | Green-on-black retro terminal |
| 3 | VS Code Dark | Dark+ with official syntax colors |
| 4 | Syntax Dark | One Dark — warm syntax on cool grey |
| 5 | Neon Cyberpunk | Electric neons on pitch black |
| 6 | Ocean Depths | Deep sea blues with bioluminescent accents |
| 7 | Northern Lights | Aurora — green, violet, blue on arctic sky |
| 8 | Midnight Navy | Classic navy with blue and cream accents |
| 9 | Sunset Gradient | Warm oranges and pinks into purple |
| 10 | Forest Canopy | Deep woodland greens with autumn gold |
| 11 | Earth & Stone | Warm terracotta, moss green, sandstone |
| 12 | Coffee Shop | Warm espresso browns and creamy latte |
| 13 | Business Formal | Charcoal and navy with gold accents |
| 14 | Chemistry Lab | Periodic-table with element colors |
| 15 | Math Chalkboard | Dark green chalkboard with chalk text |
| 16 | Pastel Dream | Soft dreamy pastels on warm white |
| 17 | Pink Cloud | Blush pink with rose, orchid, coral |
| 18 | Lavender Fields | Soft purples and lilacs on light mauve |
| 19 | Cherry Blossom | Japanese-inspired pink and white |
| 20 | Mint Fresh | Cool mint green with clean white |
| 21 | Arctic Frost | Ice whites and pale blues, crisp and clean |
| 22 | Art Studio | Handpainted bold expressive on canvas |
| 23 | Botanical Garden | Sage greens, soft pinks, cream |
| 24 | Notebook Classic | Lined paper with blue ink and red margin |
| 25 | Grid Paper | Engineering grid with pencil-grey tones |
| 26 | Vintage Library | Aged paper with warm leather-brown |
| 27 | Law Review | Cream parchment with burgundy and navy |
| 28 | Med School | Clinical white with anatomy accents |
| 29 | Engineering Blueprint | Blueprint blue-on-white with drafting feel |
| 30 | Architecture Studio | Minimalist concrete with precise lines |

</details>

## Installation

This is a Claude skill, not a standalone tool. To use it:

1. **Install the NotebookLM MCP extension** (required for cross-conversation memory):
   ```
   pip install notebooklm-mcp-cli
   nlm login
   ```
   Then download the `.mcpb` extension from [jacob-bd/notebooklm-mcp-cli/releases](https://github.com/jacob-bd/notebooklm-mcp-cli/releases) and install it via **Claude Desktop → Settings → Extensions**.

2. **Add this skill** by copying `SKILL.md` and the `references/` folder into your Claude skills directory.

3. **Trigger it** by asking Claude to take or review course notes — e.g. *"Write notes for Chapter 3 of my Dynamics class"* or *"Review my notes for ECOR 1042"*.

## Repository contents

```
SKILL.md                        Skill definition: triggers, workflow, output rules
references/
  theme.md                      Deep Space reference (templates that apply to any theme)
  theme-previews.html           Static preview of all 30 themes side-by-side
```

## License

MIT — use it, fork it, theme it.
