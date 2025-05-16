import pytest
from app.pipeline.retriever.custom_retriever import Retriever

@pytest.fixture
def retriever():
    return Retriever()

def test_encode_shape(retriever):
    vec = retriever.encode("What is the Eiffel Tower?")
    assert isinstance(vec, list)
    assert len(vec) in {384, 768}, "Unexpected embedding dimension"
    assert all(isinstance(v, float) for v in vec)

def test_retrieve_basic_query(retriever):
    results = retriever.retrieve("What is the Eiffel Tower?")
    assert isinstance(results, list)
    assert len(results) > 0, "No results returned from Qdrant"

def test_retrieve_result_format(retriever):
    results = retriever.retrieve("Capital of France")
    for r in results:
        assert "text" in r
        assert "score" in r
        assert isinstance(r["text"], str)
        assert isinstance(r["score"], float)
