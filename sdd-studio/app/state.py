"""State ของ 1 run — เก็บว่าสเตจไหนเสร็จ, input/output อะไร, บังคับลำดับ, persist เป็น JSON."""
import json
from datetime import datetime, timezone
from pathlib import Path
from .stages import STAGE_ORDER, prior_stage

WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"
STATE_FILE = WORKSPACE / ".sdd-state.json"

DEFAULT = {
    "feature": "To-do Task API",
    "engine": "template",
    "stages": {},   # id -> {status, input, files:[paths], note, ts}
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class State:
    def __init__(self):
        self.data = self.load()

    def load(self) -> dict:
        if STATE_FILE.exists():
            try:
                return json.loads(STATE_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return json.loads(json.dumps(DEFAULT))  # deep copy

    def save(self):
        WORKSPACE.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def is_done(self, stage_id: str) -> bool:
        return self.data["stages"].get(stage_id, {}).get("status") == "done"

    def can_run(self, stage_id: str) -> bool:
        p = prior_stage(stage_id)
        return p is None or self.is_done(p)

    def mark_done(self, stage_id: str, user_input: dict, files: list, note: str):
        self.data["stages"][stage_id] = {
            "status": "done",
            "input": user_input,
            "files": [f.path for f in files],
            "note": note,
            "ts": _now(),
        }
        self.save()

    def prior_artifacts(self, workspace_read) -> dict:
        """คืน {path: content} ของทุกไฟล์ที่สเตจก่อน ๆ ผลิตไว้ (ไว้ป้อนเป็น context ให้ Claude)."""
        out = {}
        for sid in STAGE_ORDER:
            st = self.data["stages"].get(sid)
            if st and st["status"] == "done":
                for p in st["files"]:
                    try:
                        out[p] = workspace_read(p)
                    except Exception:
                        pass
        return out

    def set_engine(self, engine: str):
        self.data["engine"] = engine
        self.save()

    def set_feature(self, feature: str):
        self.data["feature"] = feature
        self.save()

    def reset(self):
        self.data = json.loads(json.dumps(DEFAULT))
        self.save()
