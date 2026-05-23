"""Evaluation metrics for TA-GraphRAG experiments."""
import re
import string
from collections import Counter


def normalize_answer(s: str) -> str:
    """Normalize answer for comparison (from SQuAD evaluation)."""
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)
    def white_space_fix(text):
        return " ".join(text.split())
    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return white_space_fix(remove_articles(remove_punc(lower(s))))


def exact_match(prediction: str, ground_truth: str) -> float:
    """Calculate exact match score."""
    return float(normalize_answer(prediction) == normalize_answer(ground_truth))


def f1_score(prediction: str, ground_truth: str) -> float:
    """Calculate token-level F1 score."""
    pred_tokens = normalize_answer(prediction).split()
    gt_tokens = normalize_answer(ground_truth).split()
    if not pred_tokens or not gt_tokens:
        return float(pred_tokens == gt_tokens)

    common = Counter(pred_tokens) & Counter(gt_tokens)
    num_common = sum(common.values())
    if num_common == 0:
        return 0.0

    precision = num_common / len(pred_tokens)
    recall = num_common / len(gt_tokens)
    return 2 * precision * recall / (precision + recall)


def evaluate_batch(predictions: list[str], ground_truths: list[str]) -> dict:
    """Evaluate a batch of predictions."""
    assert len(predictions) == len(ground_truths)
    em_scores = []
    f1_scores = []
    for pred, gt in zip(predictions, ground_truths):
        em_scores.append(exact_match(pred, gt))
        f1_scores.append(f1_score(pred, gt))
    return {
        "exact_match": sum(em_scores) / len(em_scores) * 100,
        "f1": sum(f1_scores) / len(f1_scores) * 100,
        "count": len(predictions),
    }


def faithfulness_score(answer: str, evidence: list[str]) -> float:
    """Simple heuristic faithfulness: fraction of answer tokens in evidence."""
    answer_tokens = set(normalize_answer(answer).split())
    if not answer_tokens:
        return 1.0
    evidence_text = " ".join(evidence).lower()
    covered = sum(1 for t in answer_tokens if t in evidence_text)
    return covered / len(answer_tokens)
