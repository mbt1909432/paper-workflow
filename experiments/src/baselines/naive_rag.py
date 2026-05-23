"""Naive RAG baseline: BM25 retrieval + direct generation."""
from src.llm_client import chat
from src.retriever import BM25Retriever


SYSTEM_PROMPT = """You are a helpful assistant. Answer the question based on the provided context.
If the context doesn't contain enough information, say "I cannot answer based on the given context."
Be concise and direct."""


def naive_rag(question: str, retriever: BM25Retriever, top_k: int = 5) -> dict:
    """Run Naive RAG baseline."""
    # Retrieve
    docs_with_scores = retriever.retrieve(question, top_k=top_k)
    context = "\n\n".join([doc for doc, _ in docs_with_scores])

    # Generate
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"},
    ]
    answer = chat(messages)

    return {
        "answer": answer,
        "retrieved_docs": [doc for doc, _ in docs_with_scores],
        "method": "naive_rag",
    }
