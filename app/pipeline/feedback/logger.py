import sqlite3
import json
from typing import Dict
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
