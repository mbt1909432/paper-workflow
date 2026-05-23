"""Module 6: Iterative Refinement.

If the composite quality score (trust + hallucination) is below threshold,
re-trigger retrieval and generation for up to MAX_ITERATIONS rounds.
"""
from src.config import MAX_ITERATIONS, TRUST_THRESHOLD
from src.modules.retrieval_judge import judge_retrieval
from src.modules.graph_retrieval import retrieve_with_graph
from src.modules.trust_filter import filter_by_trust, compute_trust_score
from src.modules.graph_generation import generate_answer
from src.modules.hallucination_detect import detect_hallucination
from src.knowledge_graph import KnowledgeGraph
from src.retriever import BM25Retriever


def _composite_score(trust_score: float, hallucination_score: float) -> float:
    """Compute a composite quality score.

    trust_score is in [0, 1] (higher is better).
    hallucination_score is in [0, 1] (lower is better).
    Returns a value in [0, 1] where higher is better.
    """
    return 0.5 * trust_score + 0.5 * (1.0 - hallucination_score)


def iterative_refine(
    question: str,
    documents: list[str],
    kg: KnowledgeGraph,
    retriever: BM25Retriever | None = None,
    max_iterations: int = MAX_ITERATIONS,
    quality_threshold: float = 0.65,
    top_k: int = 5,
) -> dict:
    """Run the full TA-GraphRAG pipeline with iterative refinement.

    Args:
        question: The user question.
        documents: The full document corpus.
        kg: The knowledge graph.
        retriever: Optional pre-built BM25 retriever.
        max_iterations: Maximum number of retrieve-generate iterations.
        quality_threshold: Minimum composite score to accept an answer.
        top_k: Documents to retrieve per round.

    Returns:
        A dict with keys:
          - "answer": the final answer text
          - "final_composite": final composite quality score
          - "final_trust": final trust score
          - "final_hallucination": final hallucination score
          - "iterations": number of iterations executed
          - "history": list of per-round dicts with scores
    """
    history: list[dict] = []
    best_answer = ""
    best_composite = -1.0
    best_kept_docs: list[str] = []

    for iteration in range(1, max_iterations + 1):
        # --- Step 1: Retrieval Judge ---
        need_retrieve, confidence = judge_retrieval(question)
        print(f"  [Iter {iteration}] Retrieval judge: confidence={confidence:.2f}, need_retrieve={need_retrieve}")

        # --- Step 2: Retrieve ---
        # Always retrieve when a retriever is provided (RAG setting).
        # The judge's confidence still contributes to the composite score.
        if not need_retrieve and retriever is None:
            print(f"  [Iter {iteration}] High confidence, no retriever — generating directly.")
            answer = generate_answer(question, [], "")
            trust_score = confidence
            hallucination_score, verif = detect_hallucination(question, answer, [])
            kept_doc_texts = []
        else:
            retrieval_result = retrieve_with_graph(
                question, documents, kg, retriever=retriever, top_k=top_k,
            )
            docs = retrieval_result["docs"]
            subgraph_text = retrieval_result["subgraph_text"]

            # --- Step 3: Trust Filter ---
            kept, discarded = filter_by_trust(question, docs)
            trust_score = compute_trust_score(kept)
            print(f"  [Iter {iteration}] Trust filter: kept={len(kept)}, discarded={len(discarded)}, trust={trust_score:.2f}")

            # --- Step 4: Graph-Enhanced Generation ---
            answer = generate_answer(question, kept, subgraph_text)

            # --- Step 5: Hallucination Detection ---
            hallucination_score, verif = detect_hallucination(question, answer, kept)
            kept_doc_texts = [text for text, _, _ in kept]

        composite = _composite_score(trust_score, hallucination_score)
        print(f"  [Iter {iteration}] trust={trust_score:.2f}, hallucination={hallucination_score:.2f}, composite={composite:.2f}")

        round_info = {
            "iteration": iteration,
            "confidence": confidence,
            "trust_score": trust_score,
            "hallucination_score": hallucination_score,
            "composite_score": composite,
        }
        history.append(round_info)

        # Track best answer
        if composite > best_composite:
            best_composite = composite
            best_answer = answer
            best_kept_docs = kept_doc_texts

        # Accept if quality threshold is met
        if composite >= quality_threshold:
            print(f"  [Iter {iteration}] Quality threshold met ({composite:.2f} >= {quality_threshold}). Accepting.")
            break

        print(f"  [Iter {iteration}] Quality below threshold, will refine...")

    return {
        "answer": best_answer,
        "retrieved_docs": best_kept_docs,
        "final_composite": best_composite,
        "final_trust": history[-1]["trust_score"] if history else 0.0,
        "final_hallucination": history[-1]["hallucination_score"] if history else 1.0,
        "iterations": len(history),
        "history": history,
    }
