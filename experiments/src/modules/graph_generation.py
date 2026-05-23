"""Module 4: Graph-Enhanced Generation.

Builds a prompt that combines graph structure information with filtered
retrieval documents, then calls the LLM to produce an answer.
"""
from src.llm_client import chat


def generate_answer(
    question: str,
    filtered_docs: list[tuple[str, float, dict]],
    subgraph_text: str,
) -> str:
    """Generate an answer using graph-enhanced context.

    Args:
        question: The user question.
        filtered_docs: List of (doc_text, retrieval_score, trust_details)
            tuples that passed the trust filter.
        subgraph_text: Human-readable subgraph relation strings.

    Returns:
        The generated answer string.
    """
    # --- build context sections ---
    doc_section = ""
    for i, (doc_text, _, trust) in enumerate(filtered_docs):
        trust_score = trust.get("overall", 0.0)
        doc_section += f"\n[Document {i+1}] (trust={trust_score:.2f}):\n{doc_text[:800]}\n"

    graph_section = ""
    if subgraph_text:
        graph_section = (
            "\n--- Knowledge Graph Context ---\n"
            "The following relationships from the knowledge graph may provide "
            "additional structural context:\n\n"
            f"{subgraph_text}\n"
        )

    # --- construct prompt ---
    system_prompt = (
        "You are a helpful and accurate question-answering assistant. "
        "Answer the user's question based ONLY on the provided documents and "
        "knowledge graph context. "
        "If the provided context is insufficient to answer the question, "
        "state that clearly rather than guessing.\n\n"
        "Guidelines:\n"
        "- Cite the document number when using specific information.\n"
        "- Use the knowledge graph relationships to enrich your reasoning.\n"
        "- Be concise but thorough."
    )

    user_prompt = (
        f"Question: {question}\n\n"
        f"--- Retrieved Documents ---{doc_section}\n"
        f"{graph_section}\n"
        "Please provide a well-reasoned answer."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    answer = chat(messages, temperature=0.0, max_tokens=1024)
    return answer
