# Experiment Setup Guide

Universal guide for setting up and running experiments. Adapt to your specific research task.

---

## Environment Setup

### Initialize Project

```bash
cd <project-root>
mkdir -p experiments && cd experiments

# Create uv project
uv init
# Edit pyproject.toml to add dependencies
uv sync
```

### pyproject.toml Example

```toml
[project]
name = "experiments"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    # Add your dependencies here, e.g.:
    # "openai",
    # "numpy",
    # "python-dotenv",
]

[tool uv]
dev-dependencies = []
```

### Environment Variables

Create `.env` in `experiments/` for API keys:

```
DEEPSEEK_API_KEY=sk-xxx
# OPENAI_API_KEY=sk-xxx
```

Load in code with:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Directory Structure

```
experiments/
├── .env
├── pyproject.toml
├── data/                   # Datasets
├── src/                    # Source code
│   └── config.py           # Centralized config
├── run_experiment.py       # Main experiment runner
└── results/                # Output
    └── figures/
```

## Workflow Rules

1. **Always test small first** — run on 10-20 samples to validate the pipeline works
2. **Never auto-run full benchmarks** — confirm with user before large-scale runs
3. **Report cost estimate** — calculate API calls × price before running
4. **Save results as JSON** — easy to analyze and fill into paper tables later

## Module Interface Contract

Before implementing modules, define function signatures in a contract. This prevents the #1 bug: interface mismatch between modules.

```python
# Example: define all signatures BEFORE implementation
def preprocess(data_path: str) -> list[dict]: ...
def run_method(inputs: list[dict]) -> list[dict]: ...
def evaluate(predictions: list[dict], references: list[dict]) -> dict: ...
```

Each module's return type and structure should be documented so the caller knows what to expect.

## Running Experiments

```bash
# Small test (10 samples)
cd experiments && uv run python run_experiment.py --n 10

# Full run (user must confirm)
cd experiments && uv run python run_experiment.py --n 500
```

## Result Format

Save results as JSON for easy post-processing:

```json
{
  "dataset": "HotpotQA",
  "n_samples": 10,
  "methods": {
    "Method A": {"em": 20.0, "f1": 26.4},
    "Method B": {"em": 0.0, "f1": 15.6}
  },
  "per_question": [...]
}
```
