<!--
STAGE 5 — สร้างจากคำสั่ง /tasks
INPUT : plan.md + data-model.md + contracts/ + constitution
OUTPUT: ไฟล์นี้ — งานย่อยเรียงตาม dependency, [P] = ทำขนานกันได้
กติกา : เรียงแบบ TDD (เขียนเทสต์ก่อนโค้ด ตามหลัก II)
-->
# Tasks: To-do Task API

**Legend**: `[P]` = ทำขนานกันได้ (คนละไฟล์ ไม่พึ่งกัน) · เรียงตามลำดับที่ต้องทำ

## Phase A — Setup
- [ ] **T001** สร้างโครงโปรเจกต์ `src/`, `tests/` + `pyproject.toml` (FastAPI, pydantic, pytest, httpx)
- [ ] **T002** `src/db.py` — เปิด SQLite + สร้างตารางจาก DDL ใน data-model.md

## Phase B — Tests First (ต้องแดงก่อน ⛔ ห้ามเขียนโค้ดจริงในเฟสนี้)
- [ ] **T003 [P]** contract test `POST /tasks` → ตรงกับ openapi (201 + schema Task)
- [ ] **T004 [P]** contract test `GET /tasks` + กรอง `?status=`
- [ ] **T005 [P]** contract test `POST /tasks/{id}/complete` (idempotent)
- [ ] **T006 [P]** integration test scenario #1–#5 จาก spec.md
- [ ] **T007 [P]** unit test validation: title ว่าง / ยาว > 200 → 422 (FR-008/009)

## Phase C — Core Implementation (ทำให้เทสต์ Phase B เขียว)
- [ ] **T008** `src/models.py` — Pydantic `TaskCreate`, `TaskUpdate`, `TaskOut`
- [ ] **T009** `src/routes.py` — `POST /tasks`, `GET /tasks` (+filter, เรียงใหม่สุดก่อน)
- [ ] **T010** `src/routes.py` — `GET/PATCH/DELETE /tasks/{id}` (404 เมื่อไม่พบ)
- [ ] **T011** `src/routes.py` — `POST /tasks/{id}/complete` (set completed_at, idempotent)

## Phase D — Integration
- [ ] **T012** `src/main.py` — middleware log (method/path/status/latency) ตามหลัก IV
- [ ] **T013** error handler กลาง → รูปแบบ `{ "error": { code, message } }`

## Phase E — Polish
- [ ] **T014 [P]** `quickstart.md` — วิธีรัน + curl ตัวอย่าง
- [ ] **T015 [P]** lint/format + ยืนยันเทสต์เขียวทั้งหมด (quality gate)

## Dependency Notes
```
T001 → T002 → (T003..T007 ขนานกัน) → (T008..T011) → T012/T013 → T014/T015
        setup      TEST-FIRST 🔴         CORE 🟢        integrate      polish
```
- Phase C เริ่มได้ก็ต่อเมื่อ Phase B แดงครบ (บังคับโดย constitution II)
- งานที่ [P] อยู่คนละไฟล์ → agent/คน แยกทำพร้อมกันได้

## ▶️ STAGE 6 — /implement
agent จะไล่ทำ T001→T015 ตามลำดับ, รันเทสต์หลังแต่ละสเตจ, หยุดให้คน review เมื่อติด
→ ผลลัพธ์ = โค้ดจริงใน `src/` + เทสต์เขียว + PR

## ▶️ STAGE 7 — /analyze (optional)
ตรวจ cross-artifact: spec ↔ plan ↔ tasks ↔ code ตรงกันไหม, มี requirement ตกหล่นไหม,
ขัด constitution ข้อไหนไหม → รายงานช่องว่างก่อน merge
