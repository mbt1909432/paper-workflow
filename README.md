# Paper Workflow

End-to-end academic paper writing workflow — from literature collection to publication-ready PDF.

Built as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills) that guides an AI agent through the full research paper pipeline.

## Workflow Overview

| Step | Stage | Description |
|------|-------|-------------|
| 0 | Input | Route by input type (titles, keywords, PDFs, arxiv URLs) |
| 1 | Collect | Download papers from arxiv to `arxiv-papers/` |
| 2 | Convert | PDF → Markdown with pymupdf4llm to `arxiv-papers-md/` |
| 3 | Extract | Structured extraction to `arxiv-papers-extracted/` |
| 3.5 | **Gate** | Integrity check: all 6 sections present, no placeholders |
| 4 | Fuse | Multi-angle method fusion to `arxiv-papers-fusion/` |
| 4.5 | **Adversarial** | Devil's Advocate review: challenge assumptions before writing |
| 5 | Write | LaTeX paper with proper citations |
| 5.5 | Verify | Citation verification with evidence hierarchy (A-E levels) |
| 5.6 | Compile | Tectonic compilation to PDF |
| 6 | Experiment | Implement and run experiments with `uv` |
| 6.5 | Visualize | matplotlib charts → insert into paper |
| 6.7 | **Gate** | Experiment integrity: valid JSON, no impossible values |
| 7 | Polish | Two-stage review: full analysis + verification pass |
| 7.5 | Check | Self-consistency audit before submission |

## Project Structure

```
paper-workflow/
├── skill/                      # The reusable skill definition
│   ├── SKILL.md                # Main skill file (install this)
│   └── references/             # Reference documents
│       ├── pdf2md-agent.md     # Subagent prompt template for PDF conversion
│       ├── extraction-template.md
│       ├── experiment-templates.md
│       ├── result-narrative.md
│       ├── paper-quality-checklist.md
│       └── common-pitfalls.md
├── paper/                      # LaTeX source and compiled PDF
│   ├── ta_graphrag.tex
│   ├── ta_graphrag.pdf
│   ├── references.bib
│   └── figures/
├── experiments/                # Experiment code and results
├── arxiv-papers/               # Downloaded PDFs
├── arxiv-papers-md/            # PDF → Markdown
├── arxiv-papers-extracted/     # Structured extraction
├── arxiv-papers-fusion/        # Method fusion analysis
├── docs/                       # Project documentation
└── CLAUDE.md                   # Progress tracking
```

## Key Features

- **Integrity Gates** at critical transitions (extraction → fusion, experiment → polishing)
- **Devil's Advocate** adversarial review before paper writing
- **Evidence Hierarchy** for citation verification (peer-reviewed > preprint > blog > unverified)
- **Two-Stage Polishing** with verification pass to catch regressions
- **Self-Consistency Audit** covering contribution mapping, numerical consistency, and terminology

## Demo Paper: TA-GraphRAG

This project includes a complete demo paper: **TA-GraphRAG: Trust-Aware Adaptive Graph Retrieval-Augmented Generation**

- 10 reference papers collected and analyzed
- 5-angle method fusion → TA-GraphRAG framework proposed
- Pilot experiment on HotpotQA (10 questions)
- Full LaTeX with TikZ architecture diagram, result tables, and matplotlib figures

## Requirements

- **Python**: [uv](https://github.com/astral-sh/uv) package manager
- **LaTeX**: [Tectonic](https://github.com/tectonic-typesetting/tectonic) (auto-downloads packages)
- **PDF→MD**: `pymupdf4llm`
- **Polishing**: [latex-paper-en](https://skills.sh/) skill
- **LLM APIs**: DeepSeek / OpenAI (for experiments only)

## License

MIT
