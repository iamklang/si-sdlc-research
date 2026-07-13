"""Interface กลางของ generator — TemplateGenerator กับ ClaudeGenerator ต้อง implement เหมือนกัน."""
from dataclasses import dataclass


@dataclass
class FileArtifact:
    path: str      # path สัมพัทธ์กับ workspace root
    content: str


class Generator:
    """generate(stage_id, context) -> (files, note)

    context = {
        "feature": str,          # ชื่อฟีเจอร์
        "user_input": dict,      # input จากฟอร์มของสเตจนั้น
        "prior": {path: content} # artifact ที่สเตจก่อน ๆ ผลิตไว้ (ไว้เป็น context)
    }
    """
    name = "base"

    def generate(self, stage_id: str, context: dict):
        raise NotImplementedError
