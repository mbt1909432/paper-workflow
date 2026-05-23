"""CRAG baseline: Corrective Retrieval-Augmented Generation."""
from src.llm_client import chat, chat_json
from src.retriever import BM25Retriever


def evaluate_retrieval(question: str, docs: list[str]) -> dict:
    """Evaluate if retrieved documents are relevant."""
    context = "\n".join(f"[{i+1}] {doc[:200]}" for i, doc in enumerate(docs))
    messages = [
        {"role": "user", "content": f"""Evaluate if these documents are relevant to the question.
Return JSON: {{"relevant": true/false, "confidence": 0.0-1.0, "reason": "brief explanation"}}

Question: {question}
Documents:
{context}"""},
    ]
    try:
        return chat_json(messages)
    except Exception:
        return {"relevant": True, "confidence": 0.5, "reason": "parse error"}


def correct_and_regenerate(question: str, docs: list[str]) -> str:
    """Correct retrieval and regenerate answer."""
    context = "\n\n".join(docs)
    messages = [
        {"role": "user", "content": f"""Answer the question based on the context. If the context is insufficient, provide your best answer and note what's missing.

Context: {context}
Question: {question}
Answer:"""},
    ]
    return chat(messages)


def crag(question: str, retriever: BM25Retriever, top_k: int = 5) -> dict:
    """Run CRAG baseline."""
    # Step 1: Retrieve
    docs_with_scores = retriever.retrieve(question, top_k=top_k)
    docs = [doc for doc, _ in docs_with_scores]

    # Step 2: Evaluate retrieval quality
    eval_result = evaluate_retrieval(question, docs)

    # Step 3: If retrieval is poor, try to correct
    if not eval_result.get("relevant", True) or eval_result.get("confidence", 1.0) < 0.5:
        # Re-query with refined question
        refined = chat([
            {"role": "user", "content": f"Rewrite this question to be more specific for search:\n{question}\nRewritten:"},
        ])
        docs_with_scores_2 = retriever.retrieve(refined, top_k=top_k)
        docs = [doc for doc, _ in docs_with_scores_2]
        docs_with_scores = docs_with_scores_2

    # Step 4: Generate with correction awareness
    answer = correct_and_regenerate(question, docs)

    return {
        "answer": answer,
        "retrieved_docs": docs,
        "retrieval_eval": eval_result,
        "method": "crag",
    }
