import pandas as pd
import numpy as np
from typing import List
from uuid import uuid4

from qdrant_client import QdrantClient, models as qm
from sentence_transformers import SentenceTransformer

from scripts.utils.config import CONFIG

def store_embeddings(
    ids: List[str],
    embeddings: List[List[float]],
    payloads: List[dict],
    client: QdrantClient,
    collection_name: str,
):
    points = [
        qm.PointStruct(
            id=uid,
            vector=embedding,
            payload=payload
        )
        for uid, embedding, payload in zip(ids, embeddings, payloads)
    ]
    client.upsert(collection_name=collection_name, points=points)

def main(parquet_path: str, collection_name: str):
    # Init Qdrant
    client = QdrantClient(url=CONFIG.get("Qdrant.url"))

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qm.VectorParams(
                size=384,
                distance=qm.Distance.COSINE
            ),
            shard_number=2
        )
        print(f"Created collection: {collection_name}")
    else:
        print(f"Collection already exists: {collection_name} — skipping creation")

    # Load embedding model
    model = SentenceTransformer(CONFIG.get("retriever_settings.embedding_model"))

    # Load and clean the dataset
    df = pd.read_parquet(parquet_path)
    print(f"Loaded {len(df)} rows from {parquet_path}")

    # Required: columns like 'id' and 'text' (customize if different)
    ids = [str(uuid4()) for _ in range(len(df))]
    texts = df["documents"].tolist()
    doc_ids = df.get("id", range(len(df))).tolist()

    payloads = [
        {"text": str(text), "doc_id": str(doc_id)}
        for text, doc_id in zip(texts, doc_ids)
    ]

    embeddings = model.encode(
    texts,
    batch_size=CONFIG.get("retriever_settings.batch_size"),
    normalize_embeddings=True,
    )

    # Convert NumPy array to pure Python list of lists
    embeddings = [embedding.tolist() if isinstance(embedding, np.ndarray) else embedding for embedding in embeddings]

    store_embeddings(ids, embeddings, payloads, client, collection_name)

    print(f"Stored {len(ids)} embeddings to collection: {collection_name}")

if __name__ == "__main__":
    # Replace 'train.parquet' with 'validation.parquet' or 'test.parquet' as needed
    main(parquet_path="data/raw/train_data.parquet", collection_name="retriever_qa")
