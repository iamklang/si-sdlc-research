# Feature Specification: To-do Task API

Feature Branch: 001-todo-task-api
Status: Draft
Input: "REST API จัดการ to-do task — สร้าง/อ่าน/แก้/ลบ task, ทำเครื่องหมายเสร็จ, กรองตามสถานะ"

## User Scenarios & Testing (mandatory)

### Primary User Story
ในฐานะผู้ใช้ ฉันต้องการจดงานที่ต้องทำเป็นรายการ task เพื่อไม่ให้ลืม —
เพิ่มงานใหม่ ดูรายการทั้งหมด ทำเครื่องหมายว่าเสร็จแล้ว แก้ไขรายละเอียด และลบงานที่ไม่ต้องการ

### Acceptance Scenarios
1. Given ยังไม่มี task, When สร้าง task ด้วยชื่อ "ซื้อของ", Then คืน task ที่มี id, ชื่อ, สถานะ = ยังไม่เสร็จ
2. Given มี task อยู่ 3 รายการ, When ขอรายการทั้งหมด, Then คืนครบ 3 รายการ
3. Given มี task ที่ยังไม่เสร็จ, When ทำเครื่องหมายว่าเสร็จ, Then สถานะเปลี่ยนเป็นเสร็จ + บันทึกเวลาที่เสร็จ
4. Given มี task ทั้งเสร็จและไม่เสร็จ, When กรองด้วยสถานะ "เสร็จ", Then คืนเฉพาะ task ที่เสร็จ
5. Given มี task หนึ่งรายการ, When ลบ task นั้น, Then task หายจากรายการและเรียกซ้ำได้ 404

### Edge Cases
- สร้าง task โดยไม่ใส่ชื่อ → ปฏิเสธพร้อม error ที่บอกสาเหตุ
- แก้/ลบ task ด้วย id ที่ไม่มีอยู่ → คืน 404

## Requirements (mandatory)

### Functional Requirements
- FR-001: ระบบต้องให้สร้าง task ใหม่โดยระบุ "ชื่อ" (บังคับ) และ "รายละเอียด" (ไม่บังคับ)
- FR-002: ระบบต้องกำหนดสถานะเริ่มต้นของ task ใหม่เป็น "ยังไม่เสร็จ" (pending)
- FR-003: ระบบต้องคืนรายการ task ทั้งหมด และรองรับการกรองตามสถานะ (pending/done)
- FR-004: ระบบต้องให้ดู task รายตัวด้วย id
- FR-005: ระบบต้องให้แก้ไขชื่อและรายละเอียดของ task ที่มีอยู่
- FR-006: ระบบต้องให้เปลี่ยนสถานะ task เป็น "เสร็จ" และบันทึกเวลาที่เสร็จ
- FR-007: ระบบต้องให้ลบ task
- FR-008: ระบบต้องปฏิเสธ input ที่ไม่ถูกต้อง (ชื่อว่าง/ยาวเกิน) พร้อมข้อความอธิบาย
- FR-009: ชื่อ task ต้องยาวไม่เกิน [NEEDS CLARIFICATION: จำกัดความยาวกี่ตัวอักษร?]
- FR-010: การเรียง task ในรายการ [NEEDS CLARIFICATION: เรียงตามอะไร ใหม่/เก่าก่อน?]

### Key Entities
- Task: หน่วยงานที่ต้องทำหนึ่งชิ้น
  - id, title (บังคับ), description (ไม่บังคับ), status (pending|done), created_at, completed_at

## ⚠️ ค้าง 2 จุด ([NEEDS CLARIFICATION]) → ต้องผ่าน /clarify ก่อนไป /plan
