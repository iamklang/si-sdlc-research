<!--
STAGE 4 — สร้างจากคำสั่ง /plan "ใช้ Python + FastAPI + SQLite, pytest"
INPUT : spec.md (WHAT) + คำสั่งเลือกเทคโนโลยี
OUTPUT: ไฟล์นี้ (HOW) + data-model.md + contracts/ + quickstart.md
GATE  : ต้องผ่าน "Constitution Check" ก่อนไปต่อ
-->
# Implementation Plan: To-do Task API

**Branch**: `001-todo-task-api` | **Spec**: [spec.md](./spec.md)

## Technical Context
| ด้าน | เลือกใช้ |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI (async) |
| Storage | SQLite (ไฟล์เดียว, ไม่ต้องตั้ง server) |
| Validation | Pydantic v2 |
| Testing | pytest + httpx (TestClient) |
| Project Type | single (backend API) |

## Constitution Check *(gate)*
| หลักการ | ผ่าน? | หมายเหตุ |
|---|---|---|
| I. API-First | ✅ | จะสร้าง `contracts/openapi.yaml` ก่อน implement |
| II. Test-First | ✅ | tasks.md บังคับเขียน contract/integration test ก่อนโค้ด |
| III. Simplicity | ✅ | ไม่มี repository/service layer, เขียน SQL ตรง ๆ ผ่าน 1 module |
| IV. Observable | ✅ | middleware log method/path/status/latency + error shape กลาง |
| V. Stateless | ✅ | state อยู่ใน SQLite เท่านั้น, รันด้วย `uvicorn` คำสั่งเดียว |

→ **ผ่านทุกข้อ ไม่มี complexity ที่ต้อง justify** ไปต่อ Phase 1 ได้

## Project Structure
```
src/
├── main.py          # FastAPI app + middleware (logging, error handler)
├── models.py        # Pydantic schemas (TaskCreate, TaskUpdate, TaskOut)
├── db.py            # SQLite connection + init schema
└── routes.py        # endpoint handlers
tests/
├── contract/        # ตรวจว่า response ตรง OpenAPI
├── integration/     # ตรวจ user scenario ครบ 5 ข้อ
└── unit/            # validation ราย field
```

## Phase 0 — Research
- FastAPI async + SQLite: ใช้ `sqlite3` มาตรฐาน (พอสำหรับ single-user) → ไม่ต้อง ORM
- Timestamp: เก็บเป็น ISO-8601 UTC
- **Decision log**: ไม่ใช้ SQLAlchemy (ขัดหลัก Simplicity), ไม่ใช้ async DB driver (SQLite เร็วพอ)

## Phase 1 — Design Artifacts (สร้างโดย /plan)
- ✅ [`data-model.md`](./data-model.md) — ตาราง `tasks` + สถานะทรานสิชัน
- ✅ [`contracts/openapi.yaml`](./contracts/openapi.yaml) — 6 endpoints
- ✅ [`quickstart.md`](./quickstart.md) — วิธีรัน + curl ตัวอย่าง

## Complexity Tracking
*(ว่าง — ไม่มีการเบี่ยงจากหลักการ)*
