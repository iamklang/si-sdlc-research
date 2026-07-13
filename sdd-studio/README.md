# SDD Studio 🧬

เว็บ **local** ที่ขับ Spec-Driven Development flow (แบบ GitHub Spec Kit) ทีละสเตจ —
กดสั่งผ่าน UI แล้วเห็น **Input → Action (คน/AI) → Output** พร้อมเขียน artifact จริงลงดิสก์

## รัน
```bash
cd sdd-studio
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./run.sh                      # → http://localhost:8787
```

## โหมด (Hybrid engine)
- **Template (ค่าเริ่มต้น, ออฟไลน์)** — เดินตาม flow ด้วยตัวอย่าง To-do Task API ที่เตรียมไว้ · **ไม่มี network call ใด ๆ**
- **Claude (AI จริง)** — ตั้ง key ก่อนรัน แล้วสลับ engine บน UI:
  ```bash
  export ANTHROPIC_API_KEY=sk-...
  export SDD_MODEL=claude-sonnet-5   # optional
  ```

## 7 สเตจ
`/constitution → /specify → /clarify → /plan → /tasks → /implement → /analyze`
artifact ถูกเขียนลง `workspace/` (โครงเดียวกับ `../spec-kit-demo/`) — ที่สเตจ `/implement` กด **Run tests** เพื่อรัน pytest จริง

## 🔒 ความเป็นส่วนตัว
local/private เท่านั้น — ไม่มีการ publish ขึ้น claude web จุดเดียวที่ส่งข้อมูลออกนอกเครื่องคือโหมด Claude
ที่ผู้ใช้เปิดเอง (ใช้ key ของตัวเอง) ตามนโยบายใน `../CLAUDE.md`
