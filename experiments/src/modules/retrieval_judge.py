"""Module 1: Adaptive Retrieval Judge.

Uses LLM to assess self-confidence on a question, deciding whether
external retrieval is needed.
"""
from src.llm_client import chat_json


def judge_retrieval(question: str, threshold: float = 0.7) -> tuple[bool, float]:
    """Decide if retrieval is needed for the given question.

    Args:
        question: The user question to evaluate.
        threshold: Confidence threshold below which retrieval is triggered.

    Returns:
        (need_retrieve, confidence) where need_retrieve is True when
        confidence < threshold.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a knowledge assessment assistant. "
                "Given a question, estimate how confident you are that you can "
                "answer it correctly using only your parametric knowledge, "
                "without any external retrieval.\n\n"
                "Return a JSON object with two fields:\n"
                '- "confidence": a float between 0 and 1\n'
                '- "reasoning": a brief explanation of your confidence level'
            ),
        },
        {
            "role": "user",
            "content": f"Question: {question}",
        },
    ]

    result = chat_json(messages)
    confidence = float(result.get("confidence", 0.5))
    confidence = max(0.0, min(1.0, confidence))
    need_retrieve = confidence < threshold

    return need_retrieve, confidence
