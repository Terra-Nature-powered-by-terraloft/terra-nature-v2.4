"""
Kappa Database Utilities
SQLite connection pooling and schema initialization
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
import threading

from ..config import config
from .logging import logger

class DatabaseManager:
    """Manage SQLite connections and schema"""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._initialized = False
        self.initialize()

    def initialize(self):
        """Initialize database schema"""
        if self._initialized:
            return

        logger.info("database_initialize", db_path=str(self.db_path))

        with self.connection() as conn:
            # Load and execute schema
            schema_path = Path(__file__).parent.parent / "data" / "schema.sql"
            if schema_path.exists():
                with open(schema_path, "r") as f:
                    schema_sql = f.read()
                    conn.executescript(schema_sql)
                    conn.commit()
                logger.info("database_schema_initialized", db_path=str(self.db_path))
            else:
                logger.warning("schema_file_not_found", path=str(schema_path))

        self._initialized = True

    @contextmanager
    def connection(self):
        """Get database connection (thread-safe)"""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self.db_path))
            self._local.conn.row_factory = sqlite3.Row
        try:
            yield self._local.conn
        except Exception as e:
            logger.error("database_error", error=str(e))
            self._local.conn.rollback()
            raise

    def execute(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute query and return results"""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Execute query and return first result"""
        results = self.execute(query, params)
        return results[0] if results else None

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert data and return last row id"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(data.values()))
            conn.commit()
            return cursor.lastrowid

    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """Update data and return affected rows"""
        set_clause = ", ".join([f"{k}=?" for k in data.keys()])
        where_clause = " AND ".join([f"{k}=?" for k in where.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        values = list(data.values()) + list(where.values())
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount

    def delete(self, table: str, where: Dict[str, Any]) -> int:
        """Delete data and return affected rows"""
        where_clause = " AND ".join([f"{k}=?" for k in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"

        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(where.values()))
            conn.commit()
            return cursor.rowcount

    def close(self):
        """Close database connection"""
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None
            logger.info("database_closed")

# Global database instance
db = DatabaseManager(config.kb_path)
