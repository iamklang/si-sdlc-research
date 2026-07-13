"""นิยาม 7 สเตจของ Spec-Driven Development flow (mirror จาก spec-kit-flow.html).

แต่ละสเตจบอก: คำสั่ง, ผู้ทำ (actor: human/ai), รูปแบบ input ที่ UI ต้อง render,
และไฟล์ output ที่จะถูกเขียนลง workspace.
"""

SLUG = "001-todo-task-api"

# ไฟล์ output ต่อสเตจ (path สัมพัทธ์กับ workspace root — mirror spec-kit-demo)
OUTPUTS = {
    "constitution": [".specify/memory/constitution.md"],
    "specify":      [f"specs/{SLUG}/spec.md"],
    "clarify":      [f"specs/{SLUG}/spec.md"],
    "plan":         [
        f"specs/{SLUG}/plan.md",
        f"specs/{SLUG}/data-model.md",
        f"specs/{SLUG}/contracts/openapi.yaml",
        f"specs/{SLUG}/quickstart.md",
    ],
    "tasks":        [f"specs/{SLUG}/tasks.md"],
    "implement":    [
        "src/__init__.py", "src/db.py", "src/models.py",
        "src/routes.py", "src/main.py", "tests/test_tasks.py",
    ],
    "analyze":      [f"specs/{SLUG}/analysis.md"],
}

STAGES = [
    {
        "id": "constitution", "num": 1, "cmd": "/constitution",
        "title": "ตั้งกติกาที่บังคับทุกสเตจ", "actors": ["human"],
        "input": {"type": "principles", "label": "หลักการของทีม (แก้ไขได้ก่อนสั่ง)"},
        "flag": {"kind": "amber", "label": "rulebook",
                 "text": 'หลัก "Test-First" ที่ตั้งตรงนี้ จะไปบังคับลำดับงานใน /tasks'},
    },
    {
        "id": "specify", "num": 2, "cmd": "/specify",
        "title": 'บอก "อะไร/ทำไม" — ห้ามพูดถึงเทคโนโลยี', "actors": ["ai"],
        "input": {"type": "idea", "label": "อธิบายฟีเจอร์ที่อยากได้ (ภาษาคน)",
                  "placeholder": "REST API จัดการ to-do task — สร้าง/อ่าน/แก้/ลบ, ทำเครื่องหมายเสร็จ, กรองตามสถานะ"},
        "flag": {"kind": "amber", "label": "what · not how",
                 "text": "ได้ spec ที่มี FR-xxx + user story และ [NEEDS CLARIFICATION] ค้างไว้"},
    },
    {
        "id": "clarify", "num": 3, "cmd": "/clarify",
        "title": "อุดช่องว่างก่อนลงมือ (human gate)", "actors": ["human"],
        "input": {"type": "questions", "label": "ตอบคำถามที่ AI ถามกลับ",
                  "questions": [
                      {"id": "q1", "q": "ชื่อ task จำกัดความยาวกี่ตัวอักษร?", "default": "200"},
                      {"id": "q2", "q": "รายการ task เรียงตามอะไร?", "default": "เวลาสร้าง ใหม่สุดก่อน"},
                      {"id": "q3", "q": "ต้องมี auth / หลายผู้ใช้ไหม?", "default": "ยังไม่ต้อง (single-user)"},
                  ]},
        "flag": {"kind": "amber", "label": "human decides",
                 "text": "คำตอบจะถูกเขียนกลับเป็น FR-009/FR-010 + Out of Scope"},
    },
    {
        "id": "plan", "num": 4, "cmd": "/plan",
        "title": 'เลือก "ยังไง" (HOW) + ผ่าน gate', "actors": ["ai", "human"],
        "input": {"type": "tech", "label": "เลือกเทคโนโลยี",
                  "fields": [
                      {"id": "language", "label": "Language", "default": "Python 3.12"},
                      {"id": "framework", "label": "Framework", "default": "FastAPI"},
                      {"id": "storage", "label": "Storage", "default": "SQLite (stdlib)"},
                  ]},
        "flag": {"kind": "amber", "label": "constitution check",
                 "text": "ต้องเช็กว่าแผนไม่ขัดกติกา + สร้าง API contract ก่อนเขียนโค้ด"},
    },
    {
        "id": "tasks", "num": 5, "cmd": "/tasks",
        "title": "แตกงานเรียงตาม dependency", "actors": ["ai"],
        "input": {"type": "auto", "label": "อ่าน plan + contracts อัตโนมัติ"},
        "flag": {"kind": "amber", "label": "tdd order",
                 "text": "เทสต์ (Phase B) มาก่อนโค้ดจริง (Phase C) เสมอ · [P] = ขนานได้"},
    },
    {
        "id": "implement", "num": 6, "cmd": "/implement",
        "title": "AI เขียนโค้ด → คน review", "actors": ["ai", "human"],
        "input": {"type": "auto", "label": "อ่าน tasks.md อัตโนมัติ"},
        "flag": {"kind": "green", "label": "runnable",
                 "text": "เขียน src/ + tests/ จริง แล้วกด Run tests เพื่อรัน pytest"},
    },
    {
        "id": "analyze", "num": 7, "cmd": "/analyze",
        "title": "ตรวจความสอดคล้อง (optional)", "actors": ["ai", "human"],
        "input": {"type": "auto", "label": "ตรวจ spec ↔ plan ↔ tasks ↔ code"},
        "flag": None,
    },
]

STAGE_ORDER = [s["id"] for s in STAGES]
STAGE_BY_ID = {s["id"]: s for s in STAGES}


def prior_stage(stage_id: str):
    i = STAGE_ORDER.index(stage_id)
    return STAGE_ORDER[i - 1] if i > 0 else None
