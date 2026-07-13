"""SDD Studio — FastAPI local server.

เสิร์ฟหน้าเว็บ + API ขับ Spec-Driven Development flow ทีละสเตจ
เขียน artifact จริงลง workspace/ และรัน pytest ได้ (local เท่านั้น)
"""
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .stages import STAGES, STAGE_BY_ID, OUTPUTS
from .state import State, WORKSPACE
from .generators.template import TemplateGenerator
from .runner import run_pytest

BASE = Path(__file__).resolve().parent.parent
WEB = BASE / "web"

app = FastAPI(title="SDD Studio")


# ---------- workspace helpers (กัน path traversal) ----------
def _abs(rel: str) -> Path:
    p = (WORKSPACE / rel).resolve()
    if not str(p).startswith(str(WORKSPACE.resolve())):
        raise HTTPException(400, "invalid path")
    return p


def ws_write(rel: str, content: str):
    p = _abs(rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def ws_read(rel: str) -> str:
    return _abs(rel).read_text(encoding="utf-8")


# ---------- engine selection ----------
def has_claude_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def get_generator(engine: str):
    if engine == "claude":
        if not has_claude_key():
            raise HTTPException(400, "ยังไม่มี ANTHROPIC_API_KEY — ใช้ engine=template หรือ export key ก่อน")
        from .generators.claude import ClaudeGenerator
        return ClaudeGenerator()
    return TemplateGenerator()


# ---------- request models ----------
class RunBody(BaseModel):
    input: dict = {}
    engine: str = "template"


class ConfigBody(BaseModel):
    feature: str | None = None
    engine: str | None = None


# ---------- routes: meta ----------
@app.get("/api/engine")
def engine_info():
    return {"templateAvailable": True, "claudeAvailable": has_claude_key()}


@app.get("/api/stages")
def stages_meta():
    return {"stages": STAGES}


@app.get("/api/state")
def get_state():
    st = State()
    return {"state": st.data, "claudeAvailable": has_claude_key()}


@app.post("/api/config")
def set_config(body: ConfigBody):
    st = State()
    if body.feature is not None:
        st.set_feature(body.feature)
    if body.engine is not None:
        st.set_engine(body.engine)
    return {"state": st.data}


# ---------- routes: run a stage ----------
@app.post("/api/run/{stage}")
def run_stage(stage: str, body: RunBody):
    if stage not in STAGE_BY_ID:
        raise HTTPException(404, f"unknown stage: {stage}")
    st = State()
    if not st.can_run(stage):
        raise HTTPException(409, "ต้องทำสเตจก่อนหน้าให้เสร็จก่อน")

    st.set_engine(body.engine)
    gen = get_generator(body.engine)
    context = {
        "feature": st.data.get("feature", ""),
        "user_input": body.input,
        "prior": st.prior_artifacts(ws_read),
    }
    try:
        files, note = gen.generate(stage, context)
    except Exception as e:  # noqa: BLE001 — คืน error ให้ UI แสดง
        raise HTTPException(502, f"generate ล้มเหลว: {e}")

    for f in files:
        ws_write(f.path, f.content)
    st.mark_done(stage, body.input, files, note)

    i = [s["id"] for s in STAGES].index(stage)
    next_id = STAGES[i + 1]["id"] if i + 1 < len(STAGES) else None
    return {
        "stage": stage,
        "actors": STAGE_BY_ID[stage]["actors"],
        "note": note,
        "files": [{"path": f.path, "content": f.content} for f in files],
        "nextStage": next_id,
        "engine": body.engine,
    }


@app.get("/api/artifact")
def get_artifact(path: str):
    try:
        return {"path": path, "content": ws_read(path)}
    except FileNotFoundError:
        raise HTTPException(404, "ไม่พบไฟล์")


@app.post("/api/implement/test")
def implement_test():
    return run_pytest()


@app.post("/api/reset")
def reset():
    st = State()
    st.reset()
    # ล้างไฟล์ artifact ใน workspace (คง .sdd-state.json ที่เพิ่ง reset)
    import shutil
    for child in WORKSPACE.iterdir():
        if child.name == ".sdd-state.json":
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    return {"state": st.data}


# ---------- static / index ----------
@app.get("/")
def index():
    return FileResponse(WEB / "index.html")


app.mount("/web", StaticFiles(directory=str(WEB)), name="web")
