"""รัน pytest ใน workspace (สำหรับสเตจ /implement) แล้วคืนผล pass/fail."""
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"


def run_pytest() -> dict:
    if not (WORKSPACE / "tests").exists():
        return {"ok": False, "passed": 0, "failed": 0,
                "output": "ยังไม่มี tests/ — ต้องรัน /implement ก่อน"}
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "tests"],
            cwd=str(WORKSPACE),
            capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        return {"ok": False, "passed": 0, "failed": 0,
                "output": "ไม่พบ pytest — ติดตั้งด้วย: pip install pytest httpx fastapi"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "passed": 0, "failed": 0, "output": "pytest timeout (120s)"}

    out = (proc.stdout or "") + (proc.stderr or "")
    passed = failed = 0
    for line in out.splitlines():
        low = line.lower()
        if " passed" in low or " failed" in low or " error" in low:
            import re
            for n, kw in re.findall(r"(\d+)\s+(passed|failed|error)", low):
                if kw == "passed":
                    passed = int(n)
                else:
                    failed += int(n)
    return {"ok": proc.returncode == 0, "passed": passed, "failed": failed, "output": out.strip()}
