---
name: academic-paper-workflow
description: >
  End-to-end academic paper writing workflow from literature collection to publication-ready PDF.
  Covers 10 steps: (1) Literature search & download from arxiv, (2) PDF-to-Markdown conversion,
  (3) Structured information extraction, (4) Multi-angle method fusion & new method proposal,
  (5) LaTeX paper writing with proper citations, (6) Citation verification from external sources only,
  (7) LaTeX compilation to PDF, (8) Experiment implementation & execution,
  (9) Result visualization with matplotlib, (10) Paper polishing with latex-paper-en skill.
  Use when the user wants to write a research paper, thesis, or technical report from scratch.
  Triggers: "write a paper", "论文", "start paper project", "literature review",
  "帮我写论文", "论文工作流", "academic writing workflow".
---

# Academic Paper Workflow

Guide the user through the full paper writing pipeline. Record progress in the project's CLAUDE.md after each step.

## Project Directory Convention

```
<project-root>/
├── CLAUDE.md                # Progress tracking
├── .env                     # API keys
├── arxiv-papers/            # Step 1: Downloaded PDFs
├── arxiv-papers-md/         # Step 2: PDF → Markdown
├── arxiv-papers-extracted/  # Step 3: Structured extraction
├── arxiv-papers-fusion/     # Step 4: Method fusion
├── paper/                   # Step 5-7: LaTeX source
│   ├── main.tex
│   ├── references.bib
│   └── figures/
└── experiments/             # Step 8-9: Experiments
    ├── pyproject.toml
    └── results/
```

## Pipeline Steps

### Step 0: Determine Input Source

Route based on what the user provides:

| Input | Entry point |
|---|---|
| Paper titles / arxiv URLs | Step 1 (download) |
| Research keywords | Step 1 (search → filter → user confirms → download) |
| Local PDF files | Step 2 directly |
| Reference list | Step 1 (parse → search → download) |

### Step 1: Literature Collection

Download papers to `arxiv-papers/`. Name as `序号_简短标题.pdf`. Use parallel subagents for multiple papers.

### Step 2: PDF to Markdown

**Tool:** pymupdf4llm (`pip install pymupdf4llm`)

```python
import pymupdf4llm
md_text = pymupdf4llm.to_markdown("C:/path/to/file.pdf")  # Use OS-native paths
```

Assign one subagent per paper (parallel). Each subagent:
1. Converts PDF → MD with pymupdf4llm
2. Adds YAML front matter (title, authors, date, arxiv_id)
3. Cleans artifacts (broken tables, garbled math)
4. Saves to `arxiv-papers-md/`

Subagent prompt template: See [references/pdf2md-agent.md](references/pdf2md-agent.md)

### Step 3: Structured Extraction

One subagent per paper. Extract to `arxiv-papers-extracted/` with sections: Abstract, Methodology, Contribution, Limitation, Evaluation, Key Insights. See [references/extraction-template.md](references/extraction-template.md).

### Step 4: Method Fusion

Assign 3-5 fusion angles as parallel subagents. Each reads all extracted papers, produces comparison table + gap analysis + fusion proposals. User selects best proposal → becomes paper's core method.

### Step 5: LaTeX Paper Writing

Write to `paper/main.tex`. Standard structure:
1. Abstract (problem → approach → results → significance)
2. Introduction (challenges → gap → approach → contributions)
3. Related Work (organized by theme, not chronologically)
4. Methodology (with math, TikZ diagrams)
5. Experiments (setup → results → ablation → analysis)
6. Conclusion (contributions + limitations + future work)

Experiment data can be placeholders initially; mark for later replacement.

### Step 5.5: Citation Verification

**CRITICAL: Never fabricate citations. Every reference must trace to an external source.**

3-layer verification:
1. **Citation pool**: Scan all collected papers' References → build JSON pool
2. **Own papers' metadata**: Check if citation is one of our collected papers
3. **External verification**: WebSearch for remaining (ACL Anthology, Semantic Scholar)

Generate `references.bib` with `note = {Verified: source}` for each entry.

### Step 5.6: LaTeX Compilation

**Tool:** Tectonic (lightweight, auto-downloads packages)

```bash
# Download from https://github.com/tectonic-typesetting/tectonic/releases
paper/tectonic_bin/tectonic.exe paper/main.tex
```

### Step 6: Experiment Implementation

Set up `experiments/` with `uv`. Standard structure: `src/` for code, `data/` for datasets, `results/` for output, `run_experiment.py` as entry point. See [references/experiment-templates.md](references/experiment-templates.md) for setup guide.

**Rules:**
- Small-scale test first (10-20 samples) to validate pipeline
- Never auto-run large benchmarks — confirm with user
- Report cost estimate before large API usage
- Define module interfaces before implementation to avoid integration bugs

### Step 6.5: Result Visualization

matplotlib bar charts, radar charts, heatmaps. Save to `experiments/results/figures/` → copy to `paper/figures/`. Insert in .tex with `\includegraphics`.

### Step 7: Paper Polishing

**Tool:** `latex-paper-en` skill. Run analysis modules:

```bash
cd <project-with-uv-env>
uv run python -B ~/.agents/skills/latex-paper-en/scripts/analyze_grammar.py main.tex
uv run python -B ~/.agents/skills/latex-paper-en/scripts/analyze_experiment.py main.tex
uv run python -B ~/.agents/skills/latex-paper-en/scripts/analyze_logic.py main.tex
uv run python -B ~/.agents/skills/latex-paper-en/scripts/deai_check.py main.tex --analyze
uv run python -B ~/.agents/skills/latex-paper-en/scripts/analyze_abstract.py main.tex
```

Common fixes: add concrete numbers to abstract, add transition before contributions, justify tool choices, add findings summary to conclusion.

### Step 7.5: Self-Consistency Check (before submission)

Apply [references/paper-quality-checklist.md](references/paper-quality-checklist.md) to verify:
1. Contribution-verification mapping (Introduction → Method → Ablation → Conclusion)
2. Numerical consistency (Abstract vs Table vs text)
3. Terminology consistency
4. Citation consistency
5. Run data verification script if available

## Environment

- **Python:** uv (`uv run python script.py`, `uv pip install package`)
- **GPU:** Not required; use LLM APIs (DeepSeek, OpenAI, etc.)
- **LaTeX:** Tectonic preferred over MiKTeX (fewer install issues)
- **PDF→MD:** pymupdf4llm (`to_markdown()`, not `to_markstream()`)
- **Parallel tasks:** Agent tool with `run_in_background=true`
- **Polishing:** latex-paper-en skill (`npx skills add bahayonghang/academic-writing-skills@latex-paper-en -g -y`)
