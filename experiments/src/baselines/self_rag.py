"""Self-RAG baseline: adaptive retrieval with self-reflection."""
from src.llm_client import chat, chat_json
from src.retriever import BM25Retriever


def judge_need_retrieval(question: str) -> bool:
    """Ask LLM if retrieval is needed."""
    messages = [
        {"role": "user", "content": f"""Given this question, do you need to search for external information to answer it accurately?
Answer JSON: {{"need_retrieval": true/false, "confidence": 0.0-1.0}}

Question: {question}"""},
    ]
    try:
        result = chat_json(messages)
        return result.get("need_retrieval", True)
    except Exception:
        return True


def self_rag(question: str, retriever: BM25Retriever, top_k: int = 5) -> dict:
    """Run Self-RAG baseline."""
    # Step 1: Judge if retrieval needed
    need_retrieval = judge_need_retrieval(question)

    if need_retrieval:
        docs_with_scores = retriever.retrieve(question, top_k=top_k)
        context = "\n\n".join([doc for doc, _ in docs_with_scores])
    else:
        docs_with_scores = []
        context = "No external context needed."

    # Step 2: Generate
    messages = [
        {"role": "user", "content": f"""Answer the question. {"Use the context below if helpful." if context else ""}

Context: {context}
Question: {question}
Answer:"""},
    ]
    answer = chat(messages)

    # Step 3: Self-critique
    critique = chat([
        {"role": "user", "content": f"""Is this answer accurate and well-supported? Rate 1-5.
Question: {question}
Answer: {answer}
Context: {context}
JSON: {{"rating": 1-5, "issues": "description"}}"""},
    ])

    return {
        "answer": answer,
        "retrieved_docs": [doc for doc, _ in docs_with_scores],
        "need_retrieval": need_retrieval,
        "critique": critique,
        "method": "self_rag",
    }
