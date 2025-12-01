import sqlite3
import os
from typing import List, Dict, Any, Optional
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'dealflow.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

class DBManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = self._get_conn()
        with open(SCHEMA_PATH, 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.close()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add_sponsor(self, company_name: str, website: str) -> int:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sponsors (company_name, website) VALUES (?, ?)",
            (company_name, website)
        )
        conn.commit()
        sponsor_id = cursor.lastrowid
        conn.close()
        return sponsor_id

    def get_sponsors_by_status(self, status: str) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sponsors WHERE status = ?", (status,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_all_sponsors(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sponsors")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update_sponsor_status(self, sponsor_id: int, status: str):
        conn = self._get_conn()
        conn.execute("UPDATE sponsors SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (status, sponsor_id))
        conn.commit()
        conn.close()

    def add_research_artifact(self, sponsor_id: int, content: str):
        conn = self._get_conn()
        conn.execute("INSERT INTO research_artifacts (sponsor_id, content) VALUES (?, ?)", (sponsor_id, content))
        conn.commit()
        conn.close()

    def log_event(self, sponsor_id: int, agent_name: str, action: str, details: str):
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO event_log (sponsor_id, agent_name, action, details) VALUES (?, ?, ?, ?)",
            (sponsor_id, agent_name, action, details)
        )
        conn.commit()
        conn.close()
    
    def get_event_log(self) -> List[Dict[str, Any]]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM event_log ORDER BY timestamp DESC LIMIT 50")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_research_artifact(self, sponsor_id: int) -> Optional[str]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM research_artifacts WHERE sponsor_id = ? ORDER BY created_at DESC LIMIT 1", (sponsor_id,))
        row = cursor.fetchone()
        conn.close()
        return row['content'] if row else None

if __name__ == "__main__":
    # Test
    db = DBManager()
    print("Database initialized.")
