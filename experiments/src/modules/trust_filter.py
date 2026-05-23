"""Module 3: Trustworthiness-Aware Filtering.

Evaluates retrieved documents on factuality, relevance, and timeliness,
then filters out those below the trust threshold.
"""
from src.llm_client import chat_json
from src.config import TRUST_THRESHOLD


def _assess_single_doc(question: str, doc: str, doc_index: int) -> dict:
    """Ask the LLM to score one document on three trust dimensions."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a document trustworthiness assessor. "
                "Given a question and a retrieved document, evaluate the document "
                "on three dimensions, each as a float between 0 and 1:\n\n"
                '- "factuality": How factually accurate and well-supported the '
                "claims in the document appear to be.\n"
                '- "relevance": How relevant the document is to answering the question.\n'
                '- "timeliness": How up-to-date the information is (1.0 if the topic '
                "is not time-sensitive).\n\n"
                "Return a JSON object with keys: "
                "\"factuality\", \"relevance\", \"timeliness\", \"overall\", "
                "and \"reason\" (a brief explanation).\n"
                "The \"overall\" score should be a weighted average: "
                "0.4 * relevance + 0.4 * factuality + 0.2 * timeliness."
            ),
        },
        {
            "role": "user",
            "content": f"Question: {question}\n\nDocument {doc_index}:\n{doc[:1500]}",
        },
    ]

    result = chat_json(messages)

    # Clamp scores
    for key in ("factuality", "relevance", "timeliness", "overall"):
        if key in result:
            result[key] = max(0.0, min(1.0, float(result[key])))
        else:
            result[key] = 0.5

    return result


def filter_by_trust(
    question: str,
    docs: list[tuple[str, float]],
    threshold: float = TRUST_THRESHOLD,
) -> tuple[list[tuple[str, float, dict]], list[tuple[str, float, dict]]]:
    """Filter documents by trust score.

    Args:
        question: The user question.
        docs: List of (document_text, retrieval_score) tuples.
        threshold: Minimum overall trust score to keep a document.

    Returns:
        (kept, discarded) where each is a list of
        (document_text, retrieval_score, trust_details) tuples.
    """
    kept: list[tuple[str, float, dict]] = []
    discarded: list[tuple[str, float, dict]] = []

    for i, (doc_text, retrieval_score) in enumerate(docs):
        trust = _assess_single_doc(question, doc_text, i)
        entry = (doc_text, retrieval_score, trust)

        if trust["overall"] >= threshold:
            kept.append(entry)
        else:
            discarded.append(entry)

    # Safety: if nothing passes the filter, keep the top-1 document
    if not kept and docs:
        doc_text, retrieval_score = docs[0]
        trust = _assess_single_doc(question, doc_text, 0)
        kept.append((doc_text, retrieval_score, trust))

    return kept, discarded


def compute_trust_score(kept: list[tuple[str, float, dict]]) -> float:
    """Compute an aggregate trust score from the kept documents.

    Returns the mean overall trust score, or 0.0 if the list is empty.
    """
    if not kept:
        return 0.0
    return sum(t["overall"] for _, _, t in kept) / len(kept)
