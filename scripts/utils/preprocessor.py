from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sklearn.preprocessing import normalize
import numpy as np


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Splits the input text into overlapping chunks to preserve context boundaries.

    Args:
        text (str): Raw input text.
        chunk_size (int): Max characters per chunk.
        overlap (int): Number of characters to overlap between chunks.

    Returns:
        List[str]: List of chunked strings.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty or whitespace.")

    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", " ", ""],  # Optional: aggressive fallbacks
        )
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        raise RuntimeError(f"Error splitting text: {e}")


def normalize_embeddings(embeddings: np.ndarray) -> List[List[float]]:
    """
    L2-normalizes a 2D embedding array (rows = vectors).

    Args:
        embeddings (np.ndarray): Unnormalized embeddings of shape (n_samples, dim)

    Returns:
        List[List[float]]: Normalized vectors as Python lists
    """
    if not isinstance(embeddings, np.ndarray):
        embeddings = np.array(embeddings)

    normed = normalize(embeddings, axis=1)
    return normed.tolist()
