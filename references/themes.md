# Theme Reference

Read this file when applying a theme during course setup (Question 4) or when changing a theme mid-course.

## 30 Available Themes

Each theme defines 6 color-coded roles used throughout the notes:
- **Equations** (primary) — equation cards, formula highlights
- **Definitions** (secondary) — definition blocks, concept explanations
- **Tips** (tertiary) — tip callouts, exam warnings, key insights
- **Derivations** — step-by-step derivation chains, proofs
- **Examples** — worked examples, PA solutions
- **Units** — unit analysis blocks, conditions

**Equation coloring rule:**
- In **chapter notes and solutions**: equations/formulas are displayed in the **equation accent color**. Variables are NOT individually color-coded — they use neutral variable pills (name + unit) below the formula.
- In the **formula/equation reference sheet only**: variables within formulas ARE individually color-coded with a clickable popup. See `references/formula-sheet-spec.md` for full specification.

**Theme independence — CRITICAL:**
Each theme defines its OWN complete color set. Do NOT fall back to Deep Space colors for any theme. When generating notes, pull ALL values from the Theme Menu & UI Specs table below — never mix in another theme's defaults. The `references/theme.md` file contains component TEMPLATES that work with any theme by substituting the chosen theme's colors. The templates are structural, not color-specific. Variable colors for the formula sheet (potentially 20+) are generated on-theme and separate from the 6 content-type colors.

| # | Theme Name | Description | Background | Font |
|---|---|---|---|---|
| 1 | **Deep Space** | Dark purple cosmos with teal and gold pops | #0B0E14 | Space Grotesk |
| 2 | **Pastel Dream** | Soft muted pastels on a warm white base | #FFF8F0 | DM Sans |
| 3 | **Pink Cloud** | Blush pink with warm rose, orchid, and coral | #FFF0F5 | Nunito |
| 4 | **Hacker Terminal** | Green-on-black retro terminal aesthetic | #0A0A0A | Fira Code |
| 5 | **VS Code Dark** | Accurate Dark+ with official syntax colors | #1E1E1E | JetBrains Mono |
| 6 | **Earth & Stone** | Warm terracotta, moss green, and sandstone | #2C2416 | Bitter |
| 7 | **Notebook Classic** | Lined paper with blue ink and red margin | #FDF6E3 | Caveat |
| 8 | **Grid Paper** | Engineering grid with pencil-grey tones | #F5F5F0 | Architects Daughter |
| 9 | **Botanical Garden** | Sage greens, soft pinks, and cream | #F8F5EE | Cormorant Garamond |
| 10 | **Ocean Depths** | Deep sea blues with bioluminescent accents | #0A1628 | Inter |
| 11 | **Sunset Gradient** | Warm oranges and pinks fading into purple | #1A0A2E | Poppins |
| 12 | **Forest Canopy** | Deep woodland greens with autumn gold | #0D1F0D | Merriweather |
| 13 | **Arctic Frost** | Ice whites and pale blues, crisp and clean | #F0F4F8 | Roboto |
| 14 | **Lavender Fields** | Soft purples and lilacs on a light mauve base | #F3E8FF | Fredoka |
| 15 | **Midnight Navy** | Classic navy with gold and cream accents | #0D1B2A | Playfair Display |
| 16 | **Engineering Blueprint** | Blueprint blue-on-white with drafting feel | #F8FBFF | IBM Plex Mono |
| 17 | **Med School** | Clinical white with anatomy accents | #FAFAFA | Source Sans 3 |
| 18 | **Business Formal** | Charcoal and navy with gold accents | #1A1A2E | Libre Franklin |
| 19 | **CS Terminal** | Dark IDE with syntax rainbow highlights | #282C34 | Source Code Pro |
| 20 | **Law Review** | Cream parchment with burgundy and navy | #FFFDF5 | Crimson Text |
| 21 | **Chemistry Lab** | Periodic-table with element colors | #0F0F1A | Rubik |
| 22 | **Architecture Studio** | Minimalist concrete with precise lines | #F5F5F5 | Barlow |
| 23 | **Math Chalkboard** | Dark green chalkboard with chalk text | #2D4A3E | Kalam |
| 24 | **Art Studio** | Bold splashes on gallery-white canvas | #FFFFFF | Fredoka |
| 25 | **Neon Cyberpunk** | Electric neons on pitch black | #0A0A0A | Orbitron |
| 26 | **Vintage Library** | Aged paper with warm leather-brown | #F5E6CA | Lora |
| 27 | **Mint Fresh** | Cool mint green with clean white | #F0FFF4 | Outfit |
| 28 | **Cherry Blossom** | Japanese-inspired pink and white | #FFF5F7 | Zen Maru Gothic |
| 29 | **Coffee Shop** | Warm espresso browns and creamy latte | #1C1410 | Josefin Sans |
| 30 | **Northern Lights** | Aurora borealis — green, violet, blue | #070B18 | Exo 2 |

## Font Swap Options

If the user doesn't like their theme's default font, offer these alternatives:
- **Sans-serif:** Inter, Outfit, DM Sans, Nunito, Poppins, Roboto, Barlow, Libre Franklin, Source Sans 3, Quicksand, Fredoka, Exo 2, Rubik, Sora
- **Serif:** Merriweather, Playfair Display, Lora, Crimson Text, Bitter
- **Monospace:** JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono, Space Mono
- **Handwritten:** Caveat, Patrick Hand, Kalam, Architects Daughter

## Theme Menu & UI Specs — APPLY AUTOMATICALLY

When a theme is selected, look up its sidebar/menu colors below and apply them directly. These values come from the theme preview source code and are the DEFINITIVE specs for each theme's UI. Do not guess or derive these — use the exact values.

**How to use:** When the user picks theme X, find it by name below. Set `--sidebar-bg` to `sb`, `--sidebar-text` to `mt`, `--menu-active` to `ma`, page title color to `tc`. Use `dk` to determine dark (1) or light (0) mode pill styling. For pending items, lighten `mt` by ~30% — never use opacity reduction.

**Content-type colors (`c`):** `eq` = equations, `def` = definitions, `tip` = tips, `der` = derivations, `ex` = examples, `unit` = units. Apply these to the 6 card bracket colors and accent variables.

| Theme | dk | sb | mt | ma | tc | eq | def | tip | der | ex | unit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Deep Space | 1 | #090C12 | #8A8DA8 | #AD8CFF | #7B5EC7 | #AD8CFF | #56D6C1 | #FFD866 | #5B9DFF | #7EE8B4 | #F0A0C0 |
| Hacker Terminal | 1 | #060606 | #00AA2A | #00FF41 | #00FF41 | #00FF41 | #00CCDD | #FFFF00 | #4488FF | #FF5555 | #FF8C00 |
| VS Code Dark | 1 | #252526 | #858585 | #569CD6 | #9CDCFE | #569CD6 | #4EC9B0 | #DCDCAA | #CE9178 | #6A9955 | #C586C0 |
| Syntax Dark | 1 | #21252B | #636D83 | #61AFEF | #ABB2BF | #61AFEF | #98C379 | #D19A66 | #E06C75 | #56B6C2 | #C678DD |
| Neon Cyberpunk | 1 | #050505 | #6A6A6A | #FF00FF | #FF00FF | #FF00FF | #00FFFF | #39FF14 | #FF3366 | #FFFF00 | #FF8C00 |
| Ocean Depths | 1 | #08111F | #5A7A9A | #00D4FF | #C0E8FF | #00D4FF | #64FFDA | #FF6B6B | #4488DD | #48D1CC | #FFB74D |
| Northern Lights | 1 | #050910 | #5A6A8A | #00E676 | #D0E8F0 | #00E676 | #B388FF | #FFD54F | #448AFF | #FF4081 | #18FFFF |
| Midnight Navy | 1 | #0A1520 | #6A7A8A | #78B8FF | #4A8AC8 | #78B8FF | #5FA8D3 | #E0D8C0 | #3A7AAA | #48D1CC | #E0A0B8 |
| Sunset Gradient | 1 | #140824 | #8A6A8A | #FF6B35 | #F0D0C8 | #FF6B35 | #C084FC | #FFD93D | #FF9A8B | #64FFDA | #E88BC0 |
| Forest Canopy | 1 | #0A180A | #5A7A5A | #4CAF50 | #D0C8A0 | #4CAF50 | #8BC34A | #FFB74D | #64B5F6 | #A1887F | #D4A0B8 |
| Earth & Stone | 1 | #231D12 | #8A7A60 | #C4835A | #E8D0B8 | #C4835A | #8B9F6B | #D4B98C | #7A9EBF | #A0785A | #C0A060 |
| Coffee Shop | 1 | #16100C | #7A6A5A | #C49A6C | #E8D8C0 | #C49A6C | #8BAA7A | #E8D5B7 | #9A7A5A | #A68B6B | #D4A070 |
| Business Formal | 1 | #141424 | #7A7A8A | #E0C97F | #E8E0D0 | #E0C97F | #5FA8D3 | #C8C8C8 | #4A6FA5 | #7EBF8E | #D4A0B0 |
| Chemistry Lab | 1 | #0B0B14 | #6A6A8A | #00BCD4 | #E0E0F0 | #00BCD4 | #8BC34A | #FF9800 | #E91E63 | #7C4DFF | #FFEB3B |
| Math Chalkboard | 1 | #254035 | #8AAA98 | #FFE082 | #F0F0E8 | #FFE082 | #A5D6A7 | #FFFFFF | #EF9A9A | #90CAF9 | #CE93D8 |
| Pastel Dream | 0 | #FFF3E8 | #9A8A7A | #E8A0B8 | #D88AA0 | #D88AA0 | #80C0A0 | #D0B060 | #90A8D0 | #90C088 | #B898D0 |
| Pink Cloud | 0 | #FFE8EF | #907078 | #C45080 | #C45080 | #C45080 | #8A70B0 | #C48870 | #A06098 | #7090B0 | #B07088 |
| Lavender Fields | 0 | #EBE0F8 | #6A5A7A | #7830C0 | #7830C0 | #7830C0 | #6070C8 | #B07040 | #9850B8 | #5888A8 | #A060A0 |
| Cherry Blossom | 0 | #FFECF0 | #7A5A68 | #B8186A | #B8186A | #B8186A | #0A7A6E | #A86008 | #D05A90 | #2A6A8A | #7A607A |
| Mint Fresh | 0 | #E6F8EC | #4A6A5A | #2A8A86 | #2A8A86 | #2A8A86 | #1A7AB0 | #C86A18 | #2A8A50 | #4A5AC0 | #B02A6A |
| Arctic Frost | 0 | #E4EAF0 | #5A6878 | #0277BD | #0D47A1 | #0277BD | #00838F | #1565C0 | #3F51B5 | #546E7A | #5E35B1 |
| Art Studio | 0 | #FFF8E8 | #6A5A4A | #D50000 | #B04A00 | #D50000 | #1A5AC0 | #C49000 | #00885A | #7A00B0 | #E06000 |
| Botanical Garden | 0 | #F0EDDF | #6A6450 | #5B8C3E | #3A5A2A | #5B8C3E | #B06080 | #C49030 | #4A7A9B | #7B6B4A | #8A5DA0 |
| Notebook Classic | 0 | #F7F0DA | #5A5040 | #2B5EA7 | #2B5EA7 | #2B5EA7 | #2E8B57 | #D94040 | #6A5ACD | #5A5A5A | #B8860B |
| Grid Paper | 0 | #EEEEEA | #5A5A50 | #4A90D9 | #3A3A3A | #4A90D9 | #5CAB7D | #D85050 | #8B72BE | #6A6A6A | #C48A30 |
| Vintage Library | 0 | #ECD8B8 | #6A5A40 | #7A3A10 | #3A2010 | #7A3A10 | #1E4A3A | #B8860B | #4A3018 | #5A2A5A | #A06A30 |
| Law Review | 0 | #F8F5EC | #5A5040 | #6A0018 | #3A0010 | #6A0018 | #142A4A | #A08040 | #6A5040 | #1E4A3A | #5A2A5A |
| Med School | 0 | #F2F2F2 | #5A5A5A | #C62828 | #2A2A2A | #C62828 | #1565C0 | #D84315 | #2E7D32 | #6A1B9A | #00695C |
| Engineering Blueprint | 0 | #EDF2F8 | #4A5A70 | #1256A8 | #0A2A5A | #1256A8 | #2A6B2A | #D45A00 | #0A3A8A | #5A5AB0 | #B02020 |
| Architecture Studio | 0 | #EBEBEB | #555555 | #222222 | #1A1A1A | #222222 | #0055AA | #CC3333 | #666666 | #1A6B1A | #8A4010 |

**If the table is ever outdated**, fetch the theme preview source at `https://taliamekh.github.io/course-notes-skill/references/theme-previews.html` and extract the values from the JavaScript `G` array. Each theme object has: `bg`, `sb`, `dk`, `f`, `mt`, `ma`, `tc`, and `c:{eq,def,tip,der,ex,unit}`.

## Notebook-Style Themes (7, 8, 9)

These use CSS background patterns (repeating lines, grid dots, or cork texture) in addition to colors. The grid/lines are subtle and should not interfere with readability. Use `background-attachment: local` so the pattern scrolls with content. Set body `line-height` equal to the grid spacing (e.g. 24px) and ensure headings, paragraphs, and card padding use multiples of the grid size so text aligns to the grid lines.

## Theme Storage

The chosen theme and font are stored in `progress.md` (header section) and in `shell-head.html` (CSS variables), and applied to ALL HTML output for that course. Read `references/theme.md` for component templates — substitute the chosen theme's colors and font in place of the Deep Space defaults.

**Theme table vs config precedence:** The colors listed in the theme table above are defaults. When a user has customized their palette (stored in `progress.md` config), the config is the source of truth and overrides table values.

**User default preference:** If a user says "make X my default theme", store it in `progress.md` global section (or in NotebookLM as `_USER_THEME_DEFAULT` if available). Future courses will use that theme unless overridden during setup.

**Theme preview:** Full 30-theme preview hosted at: `https://taliamekh.github.io/course-notes-skill/references/theme-previews.html` — share this link directly. For a single theme preview, generate a focused HTML file saved to `/mnt/user-data/outputs/theme-preview.html`.
