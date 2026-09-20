import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.chunks = []

    def build(self, chunks):
        self.chunks = chunks

        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query, k=4):
        if self.index is None:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        k = min(k, len(self.chunks))
        scores, indices = self.index.search(query_embedding, k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            results.append({
                "chunk_id": int(index),
                "text": self.chunks[index],
                "score": float(score)
            })

        return results
