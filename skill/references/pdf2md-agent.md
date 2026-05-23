# PDF to Markdown Subagent Prompt Template

Use this prompt when dispatching a subagent to convert a single PDF to structured Markdown.

---

## Prompt

You are converting an academic PDF to structured Markdown. Follow these steps exactly:

### 1. Convert

```python
import pymupdf4llm
md_text = pymupdf4llm.to_markdown("C:/path/to/file.pdf")  # Use OS-native paths, not forward slashes on Windows
```

### 2. Add YAML Front Matter

Prepend metadata to the top of the file:

```markdown
---
title: "Paper Title"
authors: ["Author1", "Author2"]
date: YYYY-MM-DD
arxiv_id: "XXXX.XXXXX"
org: "Institution Name"
---
```

Extract metadata from the PDF content (first page usually has title, authors, dates).

### 3. Clean Up

- Remove duplicate headers caused by page breaks
- Fix broken table formatting (align columns)
- Remove page numbers, headers/footers
- Keep math formulas as-is (don't try to fix LaTeX)
- Remove figure captions that are just "Figure X:" without content

### 4. Save

Save to `arxiv-papers-md/序号_简短标题.md` using the same numbering as the source PDF.

### Important Rules

- Do NOT create temporary .py scripts in the output directory
- Do NOT create _temp or _backup files
- Use the Write tool directly to save the final .md file
- If conversion quality is poor (double-column layouts, heavy math), note it in the front matter with `quality: low`
