from typing import List
from config import CONFIG
from utils.read_json import json_generator
from utils.preprocessor import chunk_text, normalize_embeddings

from qdrant_client import QdrantClient, models as qm
from sentence_transformers import SentenceTransformer
from uuid import uuid4


def store_embeddings(
    ids: List[str],
    embeddings: List[List[float]],
    texts: List[str],
    payloads: List[dict],
    client: QdrantClient,
    collection_name: str,
):
    points = [
        qm.PointStruct(
            id=id_,
            vector=vec,
            payload=payload,
        )
        for id_, vec, payload in zip(ids, embeddings, payloads)
    ]
    client.upsert(collection_name=collection_name, points=points)


def main():
    collection_name = CONFIG.get("Qdrant.collection_name")

    # Initialize Qdrant client
    client = QdrantClient(url=CONFIG.get("Qdrant.url"))

    # Check and create collection if it doesn't exist
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qm.VectorParams(
                size=384, distance=qm.Distance.COSINE
            ),
            shard_number=2,
        )
        print(f"Created collection: {collection_name}")
    else:
        print(f"Collection already exists: {collection_name} — skipping creation")

    # Load embedding model
    model = SentenceTransformer(CONFIG.get("model_settings.embedding_model"))

    texts = []
    ids = []
    payloads = []

    for doc in json_generator(file_path=CONFIG.get("data_paths.raw_data")):
        chunks = chunk_text(doc["text"], chunk_size=256, overlap=64)

        for i, chunk in enumerate(chunks):
            uid = str(uuid4())
            ids.append(uid)
            texts.append(chunk)
            payloads.append({
                "text": chunk,
                "source_doc": doc.get("id", doc.get("title", "")),
                "chunk_index": i
            })

    print(f"Chunked {len(ids)} passages from {len(payloads)} total text units.")

    # Generate and normalize embeddings
    embeddings = model.encode(
        texts,
        batch_size=CONFIG.get("model_settings.batch_size"),
        normalize_embeddings=True,
    )
    embeddings = normalize_embeddings(embeddings)

    store_embeddings(ids, embeddings, texts, payloads, client, collection_name)

    print(f"Stored {len(ids)} embeddings to collection: {collection_name}")


if __name__ == "__main__":
    main()
