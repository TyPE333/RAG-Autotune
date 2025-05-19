from app.pipeline.feedback.logger import FeedbackLogger
from scripts.utils.config import CONFIG
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Tuple


def sample_positive_pairs(n: int = 100) -> List[Tuple[str, str]]:
    """
    Sample positive feedback pairs from the feedback store.
    Returns: (query, doc_id) pairs
    """
    logger = FeedbackLogger()
    return logger.sample_positive_pairs(n)

def fetch_doc_texts(client: QdrantClient, doc_ids: List[str], collection_name: str) -> Dict[str, str]:
    id_to_text = {}

    for doc_id in doc_ids:
        scroll_result, _ = client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="doc_id",
                        match=models.MatchValue(value=doc_id)
                    )
                ]
            ),
            limit=1,
            with_payload=True,
            with_vectors=False
        )

        if scroll_result:
            payload = scroll_result[0].payload
            if "text" in payload:
                id_to_text[doc_id] = payload["text"]

    return id_to_text


def get_query_text_pairs(n: int = 100, collection_name: str = "retriever_qa") -> List[Tuple[str, str]]:
    """
    Retrieves (query, doc_text) pairs for training.
    Raises ValueError if not enough usable feedback or texts.
    """
    pairs = sample_positive_pairs(n)
    if not pairs:
        raise ValueError("No positive feedback available.")

    doc_ids = [doc_id for _, doc_id in pairs]

    client = QdrantClient(url=CONFIG.get("Qdrant.url"))
    id_to_text = fetch_doc_texts(client, doc_ids, collection_name)

    query_text_pairs = [
        (query, id_to_text[doc_id])
        for query, doc_id in pairs
        if doc_id in id_to_text
    ]

    if not query_text_pairs:
        raise ValueError("No matching documents found in Qdrant for sampled doc_ids.")

    return query_text_pairs
