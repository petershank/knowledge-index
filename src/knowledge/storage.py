# src/knowledge/storage.py
import sqlite3
from pathlib import Path
from knowledge.models import Document

class KnowledgeDB:
    def __init__(self, db_path: str = "knowledge.db"):
        self.db_path = db_path
        self.init_db()

    def _get_connection(self):
        """Creates a connection to the SQLite database file."""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initializes the database schema if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Standard metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    path TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    modified_at TEXT NOT NULL
                )
            """)
            
            # 2. SQLite FTS5 Virtual Table for fast search
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
                    id UNINDEXED,
                    title,
                    content
                )
            """)
            conn.commit()

    def save_document(self, doc: Document):
        """Inserts or updates a Document in both metadata and search tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Convert python datetime to a standardized ISO string for SQLite
            modified_str = doc.modified_at.isoformat()
            
            # 1. Save to metadata table (INSERT OR REPLACE updates if ID exists)
            cursor.execute("""
                INSERT OR REPLACE INTO documents (id, path, source_type, modified_at)
                VALUES (?, ?, ?, ?)
            """, (doc.id, doc.path, doc.source_type, modified_str))
            
            # 2. Maintain FTS5 table
            # FTS5 tables don't support standard UNIQUE keys, so we manually 
            # delete any old entries for this ID before inserting the fresh text.
            cursor.execute("DELETE FROM documents_fts WHERE id = ?", (doc.id,))
            
            cursor.execute("""
                INSERT INTO documents_fts (id, title, content)
                VALUES (?, ?, ?)
            """, (doc.id, doc.title, doc.content))
            
            conn.commit()
