import sqlite3
from app.pipeline.feedback.logger import FeedbackLogger
import json
from typing import Dict, List, Tuple

class InMemoryFeedbackLogger(FeedbackLogger):
    """
    A mock logger that stores feedback in memory for testing purposes.
    """

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        #create the schema
        self._ensure_table()

        # Insert mock data
        self.conn.execute(
            "INSERT INTO feedback (question, retrieved_doc_ids, label) VALUES (?, ?, ?)",
            ("When is Earth Day?", json.dumps(["doc1", "doc2"]), "thumbs_up")
        )
        self.conn.execute(
            "INSERT INTO feedback (question, retrieved_doc_ids, label) VALUES (?, ?, ?)",
            ("What is Diwali?", json.dumps(["doc3"]), "thumbs_down")
        )
        self.conn.commit()
    

def test_positive_pairs_returns_expected_format():

    logger = InMemoryFeedbackLogger()
    result = logger.sample_positive_pairs(5)

    query, doc_id = result[0]
    assert query == "When is Earth Day?"
    assert doc_id == "doc1"  # only the first ID from the list
        

def test_returns_empty_list_when_no_thumbs_up():
    logger = InMemoryFeedbackLogger()
    # Delete all thumbs_up entries
    logger.conn.execute("DELETE FROM feedback WHERE label = 'thumbs_up'")
    logger.conn.commit()

    result = logger.sample_positive_pairs(n=5)
    assert result == []


def test_skips_empty_retrieved_doc_ids():
    logger = InMemoryFeedbackLogger()
    logger.conn.execute(
        "INSERT INTO feedback (question, retrieved_doc_ids, label) VALUES (?, ?, ?)",
        ("Who is the president?", json.dumps([]), "thumbs_up")
    )
    logger.conn.commit()

    result = logger.sample_positive_pairs(n=5)
    # Still only 1 valid thumbs_up from setup
    assert len(result) == 1
    assert result[0][0] == "When is Earth Day?"


def test_handles_malformed_json():
    logger = InMemoryFeedbackLogger()
    logger.conn.execute(
        "INSERT INTO feedback (question, retrieved_doc_ids, label) VALUES (?, ?, ?)",
        ("Malformed?", "[this is not valid json]", "thumbs_up")
    )
    logger.conn.commit()

    # Should not crash
    result = logger.sample_positive_pairs(n=5)
    assert len(result) == 1  # Only the valid one from setup
