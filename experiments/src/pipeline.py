"""TA-GraphRAG full pipeline orchestration."""
from src.retriever import BM25Retriever
from src.knowledge_graph import build_kg_from_hotpotqa
from src.modules.iterative_refine import iterative_refine
from src.config import TOP_K_RETRIEVAL


def build_context_documents(example: dict) -> list[str]:
    """Extract context documents from HotpotQA example."""
    docs = []
    for title, sentences in example.get("context", []):
        doc = f"{title}: " + " ".join(sentences)
        docs.append(doc)
    return docs


def run_ta_graphrag(question: str, retriever: BM25Retriever, example: dict, top_k: int = TOP_K_RETRIEVAL) -> dict:
    """Run the full TA-GraphRAG pipeline.

    Delegates to iterative_refine which internally orchestrates
    all 6 modules (retrieval judge → graph retrieval → trust filter →
    graph generation → hallucination detection → iterative refinement).
    """
    # Build knowledge graph from example
    kg = build_kg_from_hotpotqa(example)

    # Get document list for the iterative refine module
    documents = build_context_documents(example)

    # Run iterative refinement (contains all 6 modules internally)
    result = iterative_refine(
        question=question,
        documents=documents,
        kg=kg,
        retriever=retriever,
        top_k=top_k,
    )

    return {
        "answer": result["answer"],
        "retrieved_docs": result.get("retrieved_docs", []),
        "confidence": result["history"][0]["confidence"] if result.get("history") else 0.5,
        "trust_score": result["final_trust"],
        "hallucination_score": result["final_hallucination"],
        "iterations": result["iterations"],
        "method": "ta_graphrag",
    }
