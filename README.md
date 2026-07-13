# sdlc — AI-SDLC & Spec-Driven Development Study

ศึกษา Spec-Driven Development (SDD) — paradigm ที่ใช้ specification เป็นจุดเริ่มต้นขับ AI coding agent ผ่าน flow `specify → plan → tasks → implement`

โปรเจกต์ประกอบด้วย 3 ส่วนหลัก:

| ส่วน | คำอธิบาย |
|---|---|
| `spec-kit-demo/` | ตัวอย่าง To-do Task API ที่สร้างจาก SDD flow — มี spec, plan, contracts, source code, tests ครบ |
| `sdd-studio/` | Local web app ที่จำลอง SDD flow ทั้ง 7 สเตจผ่าน UI — กดทีละสเตจ เห็น input/output แต่ละขั้น |
| `ai-sdlc-framework-convergence.md` | รายงานวิจัยเปรียบเทียบ AI-SDLC frameworks (Spec Kit, AWS AI-DLC, Microsoft pipeline ฯลฯ) |

---

## Quick Start — SDD Studio

```bash
cd sdd-studio
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./run.sh                      # → http://localhost:8787
```

เปิดเบราว์เซอร์ไปที่ `http://localhost:8787` แล้วกดเดิน flow ทีละสเตจ

### Engine 2 โหมด

| โหมด | วิธีใช้ | ต้องการ network |
|---|---|---|
| **Template** (ค่าเริ่มต้น) | ใช้ได้ทันที — แสดงตัวอย่าง To-do Task API ที่เตรียมไว้ | ไม่ (offline) |
| **Claude** (AI จริง) | ตั้ง API key แล้วสลับ engine บน UI | ใช่ |

สำหรับโหมด Claude:

```bash
export ANTHROPIC_API_KEY=sk-...
export SDD_MODEL=claude-sonnet-5   # optional — เลือกรุ่นได้
./run.sh
```

---

## 7 สเตจของ SDD Flow

```
 1. /constitution   → ตั้งกติกาทีม (เช่น test-first, coding style)
 2. /specify        → บอก "อะไร/ทำไม" ด้วยภาษาคน → ได้ spec
 3. /clarify        → ตอบคำถามที่ AI ถามกลับ → อุดช่องว่างใน spec
 4. /plan           → เลือกเทคโนโลยี → ได้ plan, data model, API contract
 5. /tasks          → แตกงานเรียงตาม dependency (test ก่อน code)
 6. /implement      → AI เขียนโค้ด + tests → กด Run tests รัน pytest จริง
 7. /analyze        → ตรวจความสอดคล้อง spec ↔ plan ↔ code (optional)
```

Artifact ทุกสเตจถูกเขียนลง `sdd-studio/workspace/` ในโครงสร้างเดียวกับ `spec-kit-demo/`

---

## โครงสร้างโปรเจกต์

```
sdlc/
├── spec-kit-demo/              # ตัวอย่างผลลัพธ์ SDD ที่ทำเสร็จแล้ว
│   ├── specs/001-todo-task-api/ #   spec, plan, data-model, contracts, tasks
│   ├── src/                     #   source code (FastAPI + SQLite)
│   └── tests/                   #   pytest test suite
├── sdd-studio/                 # Local web app ขับ SDD flow
│   ├── app/                     #   FastAPI server + generators
│   ├── web/                     #   Frontend (HTML/CSS/JS)
│   ├── templates/               #   Template สำหรับโหมด offline
│   ├── workspace/               #   Artifact ที่ generate ระหว่างใช้งาน
│   └── run.sh                   #   Script สำหรับรัน
├── ai-sdlc-framework-convergence.md   # รายงานวิจัย AI-SDLC
├── ai-sdlc-report.html                # รายงานวิจัย (HTML)
└── spec-kit-flow.html                 # Diagram ของ SDD flow
```

---

## ดูตัวอย่าง spec-kit-demo โดยตรง

ถ้าต้องการดูตัวอย่างผลลัพธ์ SDD โดยไม่รัน Studio — เปิดดูไฟล์ใน `spec-kit-demo/` ได้เลย:

```bash
# อ่าน spec
cat spec-kit-demo/specs/001-todo-task-api/spec.md

# รัน To-do API ที่ generate มา
cd spec-kit-demo
pip install fastapi "uvicorn[standard]" pydantic
uvicorn src.main:app --reload          # → http://localhost:8000

# รันเทสต์
pip install pytest httpx
pytest -q
```

ลองใช้ API:

```bash
# สร้าง task
curl -X POST localhost:8000/tasks -H 'Content-Type: application/json' \
     -d '{"title":"ซื้อของ"}'

# ดูทั้งหมด
curl localhost:8000/tasks

# กรองเฉพาะที่เสร็จ
curl 'localhost:8000/tasks?status=done'

# ทำเครื่องหมายเสร็จ
curl -X POST localhost:8000/tasks/1/complete

# ลบ
curl -X DELETE localhost:8000/tasks/1
```

---

## Requirements

- Python 3.12+
- Dependencies: `fastapi`, `uvicorn`, `pydantic`, `pytest`, `httpx`
- (Optional) `anthropic` — เฉพาะโหมด Claude

---

## Privacy

โปรเจกต์นี้ทำงาน local เท่านั้น — ไม่มีการ publish หรือส่งข้อมูลออกนอกเครื่อง ยกเว้นโหมด Claude ที่ผู้ใช้เปิดเองและใช้ API key ของตัวเอง
