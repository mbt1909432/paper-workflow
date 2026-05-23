# Structured Extraction Template

Template for extracting key information from each paper's Markdown file.

---

## Output Format

Save each paper's extraction as `arxiv-papers-extracted/序号_简短标题_extracted.md`:

```markdown
---
title: "Paper Title"
authors: ["Author1", "Author2"]
date: YYYY-MM-DD
arxiv_id: "XXXX.XXXXX"
org: "Institution"
---

## Abstract
- Problem solved
- Core approach
- Key findings

## Methodology
- Framework / architecture used
- Key modules and pipeline
- Technical details worth noting

## Contribution
- Claimed innovations
- How it differs from prior work

## Limitation
- Admitted weaknesses
- Unsolved problems

## Evaluation
- Datasets used
- Evaluation metrics
- Key experimental results (with numbers)

## Key Insights
- Reusable methodological ideas
- Inspiration for our research
```

## Guidelines

- Focus on Abstract, Methodology, Conclusion sections — skip boilerplate
- Keep each section concise (3-5 bullet points)
- Preserve specific numbers from experiments (e.g., "EM: 62.4, F1: 75.8")
- The "Key Insights" section is the most important for Step 4 (method fusion)
