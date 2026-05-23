"""Module 5: Three-Stage Hallucination Detection.

Implements pre-generation, mid-generation, and post-generation verification
to produce a composite hallucination score.
"""
from src.llm_client import chat, chat_json


# ---------- Stage 1: Pre-generation (evidence sufficiency) ----------

def _check_evidence_sufficiency(question: str, docs: list[tuple[str, float, dict]]) -> dict:
    """Check whether the retrieved documents contain enough evidence."""
    doc_texts = "\n".join(
        f"[Doc {i+1}]: {text[:600]}" for i, (text, _, _) in enumerate(docs)
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are an evidence sufficiency checker. "
                "Given a question and a set of documents, assess whether the "
                "documents collectively contain sufficient evidence to answer "
                "the question.\n\n"
                'Return JSON: {"sufficient": true/false, "coverage_score": 0.0-1.0, '
                '"missing_aspects": ["..."]}'
            ),
        },
        {
            "role": "user",
            "content": f"Question: {question}\n\nDocuments:\n{doc_texts}",
        },
    ]

    result = chat_json(messages)
    result["coverage_score"] = max(0.0, min(1.0, float(result.get("coverage_score", 0.5))))
    return result


# ---------- Stage 2: Mid-generation (claim verification) ----------

def _verify_claims(question: str, answer: str, docs: list[tuple[str, float, dict]]) -> dict:
    """Verify that key claims in the answer are supported by documents."""
    doc_texts = "\n".join(
        f"[Doc {i+1}]: {text[:600]}" for i, (text, _, _) in enumerate(docs)
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a factual claim verifier. "
                "Given a question, an answer, and supporting documents, identify "
                "the key factual claims in the answer and check whether each claim "
                "is supported by the documents.\n\n"
                'Return JSON: {\n'
                '  "claims": [{"claim": "...", "supported": true/false, "evidence": "..."}],\n'
                '  "supported_ratio": 0.0-1.0,\n'
                '  "unsupported_claims": ["..."]\n'
                '}'
            ),
        },
        {
            "role": "user",
            "content": (
                f"Question: {question}\n\n"
                f"Answer: {answer}\n\n"
                f"Documents:\n{doc_texts}"
            ),
        },
    ]

    result = chat_json(messages)
    result["supported_ratio"] = max(0.0, min(1.0, float(result.get("supported_ratio", 0.5))))
    return result


# ---------- Stage 3: Post-generation (Chain-of-Verification) ----------

def _chain_of_verification(question: str, answer: str) -> dict:
    """Use CoVe: ask the LLM to generate verification questions and self-verify."""
    # Step 3a: generate verification questions
    vq_messages = [
        {
            "role": "system",
            "content": (
                "Given a question and an answer, generate 3-5 verification "
                "questions that could independently check the factual accuracy "
                "of the answer.\n\n"
                'Return JSON: {"verification_questions": ["q1", "q2", ...]}'
            ),
        },
        {
            "role": "user",
            "content": f"Question: {question}\nAnswer: {answer}",
        },
    ]

    vq_result = chat_json(vq_messages)
    verif_questions = vq_result.get("verification_questions", [])[:5]

    if not verif_questions:
        return {"consistency_score": 0.5, "details": "No verification questions generated"}

    # Step 3b: answer verification questions independently
    qa_pairs = []
    for vq in verif_questions:
        resp = chat(
            [
                {"role": "system", "content": "Answer the following question concisely and factually."},
                {"role": "user", "content": vq},
            ],
            temperature=0.0,
            max_tokens=256,
        )
        qa_pairs.append({"question": vq, "answer": resp})

    # Step 3c: check consistency between original answer and verification answers
    consistency_messages = [
        {
            "role": "system",
            "content": (
                "You are a consistency checker. Given an original answer to a "
                "question and a set of independently answered verification "
                "questions, assess whether the original answer is consistent "
                "with the verification answers.\n\n"
                'Return JSON: {"consistent": true/false, '
                '"consistency_score": 0.0-1.0, "inconsistencies": ["..."]}'
            ),
        },
        {
            "role": "user",
            "content": (
                f"Original question: {question}\n"
                f"Original answer: {answer}\n\n"
                "Verification Q&A:\n"
                + "\n".join(f"Q: {qa['question']}\nA: {qa['answer']}" for qa in qa_pairs)
            ),
        },
    ]

    consistency_result = chat_json(consistency_messages)
    consistency_result["consistency_score"] = max(
        0.0, min(1.0, float(consistency_result.get("consistency_score", 0.5)))
    )
    return consistency_result


# ---------- Public entry point ----------

def detect_hallucination(
    question: str,
    answer: str,
    docs: list[tuple[str, float, dict]],
) -> tuple[float, dict]:
    """Run three-stage hallucination detection.

    Args:
        question: The user question.
        answer: The generated answer to verify.
        docs: List of (doc_text, retrieval_score, trust_details) tuples.

    Returns:
        (hallucination_score, verification_details) where
        hallucination_score is in [0, 1] (0 = no hallucination, 1 = full).
    """
    stage1 = _check_evidence_sufficiency(question, docs)
    stage2 = _verify_claims(question, answer, docs)
    stage3 = _chain_of_verification(question, answer)

    # Composite score: lower coverage, lower supported_ratio, lower consistency
    # all contribute to a higher hallucination score.
    evidence_penalty = 1.0 - stage1.get("coverage_score", 0.5)
    claim_penalty = 1.0 - stage2.get("supported_ratio", 0.5)
    consistency_penalty = 1.0 - stage3.get("consistency_score", 0.5)

    hallucination_score = (
        0.2 * evidence_penalty + 0.4 * claim_penalty + 0.4 * consistency_penalty
    )

    verification_details = {
        "stage1_evidence": stage1,
        "stage2_claims": stage2,
        "stage3_consistency": stage3,
        "evidence_penalty": round(evidence_penalty, 4),
        "claim_penalty": round(claim_penalty, 4),
        "consistency_penalty": round(consistency_penalty, 4),
    }

    return round(hallucination_score, 4), verification_details
