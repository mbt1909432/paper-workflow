"""GraphRAG baseline: graph-based retrieval without trust modules."""
from src.llm_client import chat
from src.retriever import BM25Retriever
from src.knowledge_graph import KnowledgeGraph, build_kg_from_hotpotqa


def graph_rag(question: str, retriever: BM25Retriever, example: dict = None, top_k: int = 5) -> dict:
    """Run GraphRAG baseline (without trustworthiness modules)."""
    # Step 1: Retrieve documents
    docs_with_scores = retriever.retrieve(question, top_k=top_k)
    docs = [doc for doc, _ in docs_with_scores]

    # Step 2: Build/get knowledge graph
    if example:
        kg = build_kg_from_hotpotqa(example)
    else:
        from src.knowledge_graph import build_kg_from_documents
        kg = build_kg_from_documents(docs)

    # Step 3: Extract relevant subgraph
    # Use question keywords as seed entities
    question_words = set(question.lower().split())
    seed_entities = []
    for entity_name in kg.entities:
        if any(word in entity_name.lower() for word in question_words):
            seed_entities.append(entity_name)

    if seed_entities:
        subgraph = kg.get_subgraph(seed_entities, max_hops=2)
        graph_text = kg.subgraph_to_text(subgraph)
    else:
        graph_text = "No relevant subgraph found."

    # Step 4: Generate with graph context
    context = "\n\n".join(docs)
    messages = [
        {"role": "user", "content": f"""Answer the question using both the text context and knowledge graph information.

Text Context:
{context}

Knowledge Graph Relations:
{graph_text}

Question: {question}
Answer:"""},
    ]
    answer = chat(messages)

    return {
        "answer": answer,
        "retrieved_docs": docs,
        "graph_entities": len(kg.entities),
        "graph_relations": len(kg.relations),
        "subgraph_size": len(subgraph) if seed_entities else 0,
        "method": "graph_rag",
    }
