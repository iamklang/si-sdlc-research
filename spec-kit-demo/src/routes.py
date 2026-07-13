# T009–T011 — endpoint handlers (6 ตัวตาม openapi.yaml)
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from .db import get_conn
from .models import TaskCreate, TaskUpdate, TaskOut

router = APIRouter()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _row(r) -> TaskOut:
    return TaskOut(**dict(r))


@router.post("/tasks", status_code=201, response_model=TaskOut)   # FR-001, FR-002
def create_task(body: TaskCreate):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tasks(title, description, status, created_at) VALUES (?,?,'pending',?)",
            (body.title, body.description, _now()),
        )
        r = conn.execute("SELECT * FROM tasks WHERE id=?", (cur.lastrowid,)).fetchone()
    return _row(r)


@router.get("/tasks", response_model=list[TaskOut])               # FR-003, FR-010
def list_tasks(status: str | None = Query(default=None, pattern="^(pending|done)$")):
    q, args = "SELECT * FROM tasks", ()
    if status:
        q += " WHERE status=?"
        args = (status,)
    q += " ORDER BY created_at DESC, id DESC"                     # ใหม่สุดก่อน
    with get_conn() as conn:
        rows = conn.execute(q, args).fetchall()
    return [_row(r) for r in rows]


@router.get("/tasks/{task_id}", response_model=TaskOut)           # FR-004
def get_task(task_id: int):
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if r is None:
        raise HTTPException(404, "task not found")
    return _row(r)


@router.patch("/tasks/{task_id}", response_model=TaskOut)         # FR-005
def update_task(task_id: int, body: TaskUpdate):
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if r is None:
            raise HTTPException(404, "task not found")
        title = body.title if body.title is not None else r["title"]
        desc = body.description if body.description is not None else r["description"]
        conn.execute("UPDATE tasks SET title=?, description=? WHERE id=?", (title, desc, task_id))
        r = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    return _row(r)


@router.delete("/tasks/{task_id}", status_code=204)               # FR-007
def delete_task(task_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        if cur.rowcount == 0:
            raise HTTPException(404, "task not found")


@router.post("/tasks/{task_id}/complete", response_model=TaskOut)  # FR-006
def complete_task(task_id: int):
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if r is None:
            raise HTTPException(404, "task not found")
        if r["status"] != "done":                                 # idempotent (edge case)
            conn.execute(
                "UPDATE tasks SET status='done', completed_at=? WHERE id=?",
                (_now(), task_id),
            )
            r = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    return _row(r)
