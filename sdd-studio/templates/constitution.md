<!--
STAGE 1 — สร้างจากคำสั่ง /constitution
INPUT : หลักการที่ทีมอยากยึด (คุณภาพ, การทดสอบ, style)
OUTPUT: ไฟล์นี้ — "รัฐธรรมนูญ" ที่ทุกสเตจถัดไปต้องเคารพ
-->
# To-do Task API — Constitution

## Core Principles

### I. API-First & Contract-Driven
ทุกฟีเจอร์ต้องนิยาม contract (OpenAPI) ก่อนเขียนโค้ด. Endpoint, request/response schema
และรหัสสถานะต้องถูกระบุใน `contracts/` ก่อน implementation เสมอ. การเปลี่ยน contract
ที่ breaking ต้องขึ้น version ใหม่.

### II. Test-First (NON-NEGOTIABLE)
เขียนเทสต์ก่อนโค้ดจริง (TDD). ลำดับบังคับ: เขียนเทสต์ → เทสต์แดง → เขียนโค้ด → เทสต์เขียว.
ทุก endpoint ต้องมี contract test และ integration test อย่างน้อยหนึ่งชุด. ห้าม merge
โค้ดที่ไม่มีเทสต์ครอบคลุม.

### III. Simplicity First
เริ่มจากทางที่ง่ายที่สุดที่ใช้ได้จริง. ห้ามเพิ่ม abstraction (repository, service layer,
message queue) จนกว่าจะมีเหตุผลที่พิสูจน์ได้. YAGNI เป็นค่าเริ่มต้น.

### IV. Observable & Predictable
ทุก request ต้อง log แบบ structured (method, path, status, latency).
Error response ต้องมีรูปแบบเดียวกันทั้งระบบ: `{ "error": { "code", "message" } }`.

### V. Stateless & Portable
บริการต้อง stateless — state อยู่ใน datastore เท่านั้น. ต้องรันได้ด้วยคำสั่งเดียว
โดยไม่พึ่ง service ภายนอกตอน dev (ใช้ SQLite/in-memory ได้).

## Quality Gates
- Lint + format ผ่านก่อน commit
- เทสต์ทั้งหมดเขียวก่อน merge
- ไม่มี `[NEEDS CLARIFICATION]` ค้างใน spec ก่อนขึ้น /plan

## Governance
Constitution นี้เหนือกว่าแนวปฏิบัติอื่น. การแก้ไขต้องบันทึกเหตุผลและ version.
ทุก PR/review ต้องยืนยันว่าไม่ขัดกับหลักการข้างต้น. ความซับซ้อนที่เพิ่มขึ้น
ต้องมีเหตุผลรองรับใน "Complexity Tracking" ของ plan.

**Version**: 1.0.0 | **Ratified**: 2026-07-12 | **Last Amended**: 2026-07-12
