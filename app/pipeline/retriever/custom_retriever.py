from typing import List
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from app.pipeline.retriever.base_retriever import BaseRetriever
from scripts.utils.config import CONFIG

class Retriever(BaseRetriever):
    
    def __init__(self, model_name=CONFIG.get("retriever_settings.embedding_model")):
        self.model = SentenceTransformer(model_name)
        self.client = QdrantClient(url=CONFIG.get("Qdrant.url"))
        self.collection = CONFIG.get("Qdrant.collection_name")
        self.top_k = CONFIG.get("retriever_settings.top_k", 3)

    def encode(self, query: str) -> List[float]:
        """
        Generate normalized embedding for a given query.
        """
        return self.model.encode(query, normalize_embeddings=True).tolist()

    def retrieve(self, query: str) -> List[dict]:
        """
        Perform ANN search over Qdrant and return top-k document payloads.
        """
        query_vector = self.encode(query)

        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=self.top_k
        )

        return [
            {
                "text": hit.payload.get("text", ""),
                "score": hit.score
            }
            for hit in results
        ]
