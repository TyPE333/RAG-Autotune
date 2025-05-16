from app.pipeline.feedback.logger import FeedbackLogger
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointIdsList
from typing import List, Dict, Tuple


def sample_positive_pairs(n: int = 100) -> List[Tuple[str, str]]:
    """
    Sample positive feedback pairs from the feedback store.
    Returns: (query, doc_id) pairs
    """
    logger = FeedbackLogger()
    return logger.sample_positive_pairs(n)


def fetch_doc_texts(client: QdrantClient, doc_ids: List[str], collection_name: str) -> Dict[str, str]:
    """
    Fetch document texts from Qdrant using the document IDs.
    Returns: {doc_id: text}
    """
    response = client.retrieve(
        collection_name=collection_name,
        ids=PointIdsList(doc_ids),
        with_payload=True
    )
    return {
        str(doc.id): doc.payload["text"]
        for doc in response
        if "text" in doc.payload
    }


def get_query_text_pairs(n: int = 100, collection_name: str = "retriever_qa") -> List[Tuple[str, str]]:
    """
    Retrieves (query, doc_text) pairs for training.
    Raises ValueError if not enough usable feedback or texts.
    """
    pairs = sample_positive_pairs(n)
    if not pairs:
        raise ValueError("No positive feedback available.")

    doc_ids = [doc_id for _, doc_id in pairs]

    client = QdrantClient(path="qdrant_storage")  # or use `url="..."` if remote
    id_to_text = fetch_doc_texts(client, doc_ids, collection_name)

    query_text_pairs = [
        (query, id_to_text[doc_id])
        for query, doc_id in pairs
        if doc_id in id_to_text
    ]

    if not query_text_pairs:
        raise ValueError("No matching documents found in Qdrant for sampled doc_ids.")

    return query_text_pairs
