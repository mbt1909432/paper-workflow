"""Module 2: Multi-Granularity Graph Retrieval.

Retrieves relevant documents via BM25/ hybrid search and extracts
related subgraphs from the knowledge graph.
"""
from src.llm_client import chat_json
from src.knowledge_graph import KnowledgeGraph
from src.retriever import BM25Retriever


def retrieve_with_graph(
    question: str,
    documents: list[str],
    kg: KnowledgeGraph,
    retriever: BM25Retriever | None = None,
    top_k: int = 5,
    max_hops: int = 2,
) -> dict:
    """Retrieve documents and graph subgraph relevant to the question.

    Args:
        question: The user question.
        documents: The full document corpus.
        kg: The knowledge graph built from the corpus.
        retriever: Optional pre-built retriever. If None, a BM25Retriever
            is created from ``documents`` on the fly.
        top_k: Number of documents to retrieve.
        max_hops: Maximum hops for subgraph expansion.

    Returns:
        A dict with keys:
          - "docs": list of (document_text, score) tuples
          - "subgraph_relations": list of Relation objects
          - "subgraph_text": human-readable subgraph string
          - "key_entities": list of entity names extracted from the question
    """
    # --- document retrieval ---
    if retriever is None:
        retriever = BM25Retriever(documents)
    docs = retriever.retrieve(question, top_k=top_k)

    # --- extract key entities from the question via LLM ---
    entity_messages = [
        {
            "role": "system",
            "content": (
                "Extract the most important named entities from the question. "
                "Return a JSON object with a single key \"entities\" "
                "mapping to a list of entity strings. "
                "Return at most 5 entities."
            ),
        },
        {"role": "user", "content": f"Question: {question}"},
    ]

    try:
        entity_result = chat_json(entity_messages)
        key_entities = entity_result.get("entities", [])[:5]
    except Exception:
        # Fallback: use simple noun extraction
        words = question.replace("?", "").split()
        key_entities = [w for w in words if w[0].isupper()][:3]

    # --- subgraph retrieval ---
    # Seed with entities found in KG; fall back to document titles
    seed_entities = [e for e in key_entities if e in kg.entities]
    if not seed_entities:
        # Try matching entities from retrieved docs
        for doc_text, _ in docs:
            for entity_name in kg.entities:
                if entity_name.lower() in doc_text.lower():
                    seed_entities.append(entity_name)
                    if len(seed_entities) >= 5:
                        break
            if len(seed_entities) >= 5:
                break

    subgraph_relations = kg.get_subgraph(seed_entities, max_hops=max_hops) if seed_entities else []
    subgraph_text = kg.subgraph_to_text(subgraph_relations) if subgraph_relations else ""

    return {
        "docs": docs,
        "subgraph_relations": subgraph_relations,
        "subgraph_text": subgraph_text,
        "key_entities": key_entities,
    }
