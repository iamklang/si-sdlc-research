# T002 — SQLite connection + init schema (DDL มาจาก data-model.md)
import sqlite3
from pathlib import Path

DB_PATH = Path("tasks.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  title        TEXT    NOT NULL CHECK(length(title) BETWEEN 1 AND 200),
  description  TEXT,
  status       TEXT    NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','done')),
  created_at   TEXT    NOT NULL,
  completed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)
