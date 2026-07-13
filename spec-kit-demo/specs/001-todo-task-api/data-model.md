<!-- STAGE 4 (Phase 1) — design artifact จาก /plan -->
# Data Model: To-do Task API

## Entity: Task
| Field | Type | Constraint | มาจาก |
|---|---|---|---|
| id | INTEGER | PK, autoincrement | — |
| title | TEXT | NOT NULL, len 1–200 | FR-001, FR-009 |
| description | TEXT | nullable | FR-001 |
| status | TEXT | `pending` \| `done`, default `pending` | FR-002 |
| created_at | TEXT | ISO-8601 UTC, NOT NULL | FR-010 |
| completed_at | TEXT | ISO-8601 UTC, nullable | FR-006 |

## State Transitions
```
[create] ──▶ pending ──[mark done]──▶ done
                 ▲                        │
                 └────(idempotent: done→done คงเดิม)
```
- `pending → done` : set `completed_at = now()`
- `done → done`    : no-op (FR ตาม edge case idempotent)

## Schema (SQLite DDL)
```sql
CREATE TABLE tasks (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  title        TEXT    NOT NULL CHECK(length(title) BETWEEN 1 AND 200),
  description  TEXT,
  status       TEXT    NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','done')),
  created_at   TEXT    NOT NULL,
  completed_at TEXT
);
CREATE INDEX idx_tasks_status ON tasks(status);
```
