"""Download and prepare datasets for TA-GraphRAG experiments."""
import json
import random
from pathlib import Path
from src.config import DATA_DIR, SAMPLE_SIZE, TEST_SIZE


def download_hotpotqa():
    """Download HotpotQA dev set and create samples."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    dev_url = "http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json"
    dev_path = DATA_DIR / "hotpot_dev_distractor_v1.json"

    if not dev_path.exists():
        print("Downloading HotpotQA dev set...")
        import requests
        resp = requests.get(dev_url, stream=True)
        resp.raise_for_status()
        with open(dev_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  Saved to {dev_path}")
    else:
        print(f"HotpotQA dev set already exists: {dev_path}")

    with open(dev_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"  Total dev examples: {len(data)}")

    # Sample for full experiment
    random.seed(42)
    sample = random.sample(data, min(SAMPLE_SIZE, len(data)))
    sample_path = DATA_DIR / "hotpotqa_dev_sample.json"
    with open(sample_path, "w", encoding="utf-8") as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)
    print(f"  Sample ({len(sample)} examples): {sample_path}")

    # Small test set
    test = random.sample(data, min(TEST_SIZE, len(data)))
    test_path = DATA_DIR / "hotpotqa_test.json"
    with open(test_path, "w", encoding="utf-8") as f:
        json.dump(test, f, ensure_ascii=False, indent=2)
    print(f"  Test ({len(test)} examples): {test_path}")

    return sample, test


def download_truthfulqa():
    """Download TruthfulQA dataset."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    url = "https://raw.githubusercontent.com/sylinrl/TruthfulQA/main/TruthfulQA.csv"
    csv_path = DATA_DIR / "truthfulqa.csv"

    if not csv_path.exists():
        print("Downloading TruthfulQA...")
        import requests
        resp = requests.get(url)
        resp.raise_for_status()
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"  Saved to {csv_path}")
    else:
        print(f"TruthfulQA already exists: {csv_path}")


if __name__ == "__main__":
    download_hotpotqa()
    print()
    download_truthfulqa()
    print("\nDone!")
