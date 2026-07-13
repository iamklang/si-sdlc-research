"""TemplateGenerator — โหมดออฟไลน์ 100% (ไม่มี network call).

อ่านเนื้อหาจาก sdd-studio/templates/ (seed จาก spec-kit-demo ของ To-do Task API)
แล้วคืนเป็น artifact ตาม path ที่แต่ละสเตจกำหนดใน stages.OUTPUTS
"""
from pathlib import Path
from .base import Generator, FileArtifact
from ..stages import OUTPUTS

TEMPLATES = Path(__file__).resolve().parent.parent.parent / "templates"


def _read(rel: str) -> str:
    return (TEMPLATES / rel).read_text(encoding="utf-8")


class TemplateGenerator(Generator):
    name = "template"

    def generate(self, stage_id: str, context: dict):
        out_paths = OUTPUTS[stage_id]

        if stage_id == "constitution":
            # ถ้าคนแก้ principles ในฟอร์ม ใช้ตามนั้น ไม่งั้นใช้ template
            edited = (context.get("user_input") or {}).get("principles")
            content = edited if edited else _read("constitution.md")
            return [FileArtifact(out_paths[0], content)], "ตั้งกติกาเรียบร้อย"

        if stage_id == "specify":
            return [FileArtifact(out_paths[0], _read("spec.specify.md"))], \
                   "ร่าง spec แล้ว — มี [NEEDS CLARIFICATION] ค้าง 2 จุด"

        if stage_id == "clarify":
            # โหมด offline ใช้คำตอบ canned; spec.clarify.md คือเวอร์ชันที่เคลียร์แล้ว
            return [FileArtifact(out_paths[0], _read("spec.clarify.md"))], \
                   "เคลียร์ [NEEDS CLARIFICATION] ครบ → spec พร้อมไป /plan"

        if stage_id == "plan":
            files = [
                FileArtifact(out_paths[0], _read("plan.md")),
                FileArtifact(out_paths[1], _read("data-model.md")),
                FileArtifact(out_paths[2], _read("contracts/openapi.yaml")),
                FileArtifact(out_paths[3], _read("quickstart.md")),
            ]
            return files, "ผ่าน Constitution Check + สร้าง contract ก่อนโค้ด"

        if stage_id == "tasks":
            return [FileArtifact(out_paths[0], _read("tasks.md"))], \
                   "แตกงาน T001–T015 (TDD order)"

        if stage_id == "implement":
            mapping = {
                "src/__init__.py": "code/__init__.py",
                "src/db.py": "code/db.py",
                "src/models.py": "code/models.py",
                "src/routes.py": "code/routes.py",
                "src/main.py": "code/main.py",
                "tests/test_tasks.py": "tests/test_tasks.py",
            }
            files = [FileArtifact(p, _read(mapping[p])) for p in out_paths]
            return files, "เขียน src/ + tests/ แล้ว — กด Run tests ได้เลย"

        if stage_id == "analyze":
            report = (
                "# /analyze — Consistency Report\n\n"
                "| ตรวจ | ผล |\n|---|---|\n"
                "| spec ↔ plan | ✅ FR ทุกข้อมี design รองรับ |\n"
                "| plan ↔ tasks | ✅ ทุก endpoint มี task + test |\n"
                "| tasks ↔ code | ✅ T001–T015 มีไฟล์ครบ |\n"
                "| constitution | ✅ Test-First + API-First + Simplicity ผ่าน |\n\n"
                "สรุป: ไม่มี requirement ตกหล่น พร้อม merge\n"
            )
            return [FileArtifact(out_paths[0], report)], "ตรวจครบ — สอดคล้องกันทั้งหมด"

        raise ValueError(f"unknown stage: {stage_id}")
