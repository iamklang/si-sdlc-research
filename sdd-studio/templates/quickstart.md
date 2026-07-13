# Quickstart — To-do Task API (T014)

## รัน
```bash
pip install fastapi "uvicorn[standard]" pydantic
uvicorn src.main:app --reload
```

## เทสต์
```bash
pip install pytest httpx
pytest -q          # ต้องเขียวทั้งหมด (T015 quality gate)
```

## ลองใช้ (curl)
```bash
# สร้าง task
curl -X POST localhost:8000/tasks -H 'Content-Type: application/json' \
     -d '{"title":"ซื้อของ"}'

# ดูทั้งหมด (ใหม่สุดก่อน)
curl localhost:8000/tasks

# กรองเฉพาะที่เสร็จ
curl 'localhost:8000/tasks?status=done'

# ทำเครื่องหมายเสร็จ
curl -X POST localhost:8000/tasks/1/complete

# ลบ
curl -X DELETE localhost:8000/tasks/1
```
