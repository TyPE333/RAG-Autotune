import sqlite3
import json
from typing import Dict, List, Tuple
from scripts.utils.config import CONFIG


class FeedbackLogger:
    """
    A logger that stores feedback in a local SQLite database.
    """

    def __init__(self, db_path: str = CONFIG.get("data_paths.feedback_store")):
        self.conn = sqlite3.connect(db_path)
        self._ensure_table()

    def _ensure_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                retrieved_doc_ids TEXT,
                label TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(question, retrieved_doc_ids)
            )
        """)
        self.conn.commit()

    def insert(self, feedback: Dict):
        try:
            self.conn.execute(
                "INSERT INTO feedback (question, retrieved_doc_ids, label) VALUES (?, ?, ?)",
                (
                    feedback["question"],
                    json.dumps(feedback["retrieved_doc_ids"]),
                    feedback["label"]
                )
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Duplicate feedback skipped.")
    
    def sample_positive_pairs(self, n: int = 5) -> List[Tuple[str, str]]:
        cursor = self.conn.execute(
            "SELECT question, retrieved_doc_ids FROM feedback WHERE label = 'thumbs_up' ORDER BY RANDOM() LIMIT ?",
            (n,)
        )
        rows = cursor.fetchall()
        result = []
        for q, doc_ids_json in rows:
            try:
                doc_ids = json.loads(doc_ids_json)
                if doc_ids:
                    result.append((q, doc_ids[0]))
            except json.JSONDecodeError:
                continue  # Skip malformed entries
        return result

    
    def sample_negative_feedback(self, n: int = 5) -> List[Tuple[str, str]]:
        cursor = self.conn.execute(
            "SELECT question, retrieved_doc_ids FROM feedback WHERE label = 'thumbs_down' ORDER BY RANDOM() LIMIT ?",
            (n,)
        )
        rows = cursor.fetchall()
        return [
            (q, json.loads(doc_ids)[0])  # top-1 doc only
            for q, doc_ids in rows if json.loads(doc_ids)
        ]
