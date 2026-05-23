# Common Pitfalls & Troubleshooting

Issues you're likely to encounter. Check here before debugging.

---

## LaTeX Compilation

### MiKTeX DLL Version Mismatch (Windows)

**Symptom:** `pdflatex` crashes with "internal error", DLL version not found.

**Fix:** Use Tectonic instead. Download from https://github.com/tectonic-typesetting/tectonic/releases (Windows MSVC build, ~20MB). No installation needed:

```bash
paper/tectonic_bin/tectonic.exe paper/main.tex
```

### Overfull Hbox Warnings

Common in papers with long URLs or formula-heavy text. Not critical for drafts. Fix by adding `\sloppy` or breaking long inline math.

### Non-ASCII in .bib

BibTeX `note` fields with Chinese/special characters may fail with default font encoding. Use English notes or switch to XeLaTeX + fontspec.

## Python Environment

### uv vs pip

Always use `uv run python script.py` and `uv pip install package`. Bare `python`/`pip` may point to a different installation.

### ModuleNotFoundError After Adding Dependencies

```bash
uv sync
```

### Running From Wrong Directory

Scripts expect to run from the directory containing `pyproject.toml`. Running from elsewhere causes `ModuleNotFoundError: No module named 'src'`.

## Module Integration

### Interface Mismatch

**Symptom:** `ImportError`, `TypeError`, or wrong results at module boundaries.

**Prevention:** Define all function signatures (contract) BEFORE implementing modules. See `experiment-templates.md`.

### Data Not Flowing Through Pipeline

**Symptom:** Downstream evaluation fails because a field is missing from pipeline output.

**Fix:** Check every `return` statement in your pipeline — make sure all fields the evaluator needs are actually passed through.

## Data & Files

### PDF→MD Conversion Quality

Double-column layouts and heavy LaTeX macros produce garbled output. Flag low-quality conversions and manually reconstruct critical sections.

### Subagent Leftover Files

After parallel processing, scan output directories for stray files (`.py` scripts, `_temp` files) and clean up.

## Windows-Specific

- Python file paths: use `C:/path/to/file` or raw strings `r"C:\path"`
- Claude Code bash: use Unix conventions (`/dev/null`, forward slashes, `mkdir -p`)
- Tectonic.exe: verify file size (~49MB). A few KB file is a corrupted download.
