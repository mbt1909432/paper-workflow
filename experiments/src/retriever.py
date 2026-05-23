"""BM25 + FAISS hybrid retriever."""
from rank_bm25 import BM25Okapi
import numpy as np
from typing import Optional


class BM25Retriever:
    """Simple BM25 retriever over documents."""

    def __init__(self, documents: list[str]):
        self.documents = documents
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        """Return top_k documents with scores."""
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(self.documents[i], float(scores[i])) for i in top_indices]


class VectorRetriever:
    """FAISS-based vector retriever using sentence-transformers."""

    def __init__(self, documents: list[str], model_name: str = "all-MiniLM-L6-v2"):
        self.documents = documents
        # Lazy import to avoid loading model until needed
        from sentence_transformers import SentenceTransformer
        import faiss

        self.model = SentenceTransformer(model_name)
        embeddings = self.model.encode(documents, show_progress_bar=False)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype(np.float32))

    def retrieve(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        """Return top_k documents with similarity scores."""
        import faiss

        query_vec = self.model.encode([query], show_progress_bar=False)
        faiss.normalize_L2(query_vec)
        scores, indices = self.index.search(query_vec.astype(np.float32), top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:
                results.append((self.documents[idx], float(score)))
        return results


class HybridRetriever:
    """Combine BM25 and vector retrieval with score fusion."""

    def __init__(self, documents: list[str], bm25_weight: float = 0.4, vector_weight: float = 0.6):
        self.bm25 = BM25Retriever(documents)
        self.vector = VectorRetriever(documents)
        self.bm25_weight = bm25_weight
        self.vector_weight = vector_weight

    def retrieve(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        """Fuse BM25 and vector results."""
        bm25_results = self.bm25.retrieve(query, top_k=top_k * 2)
        vector_results = self.vector.retrieve(query, top_k=top_k * 2)

        # Normalize scores
        doc_scores: dict[str, float] = {}
        for doc, score in bm25_results:
            doc_scores[doc] = doc_scores.get(doc, 0) + self.bm25_weight * score
        for doc, score in vector_results:
            doc_scores[doc] = doc_scores.get(doc, 0) + self.vector_weight * score

        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_docs[:top_k]
