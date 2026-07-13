#!/usr/bin/env bash
# รัน SDD Studio (local เท่านั้น)
set -e
cd "$(dirname "$0")"
PORT="${PORT:-8787}"
echo "▶ SDD Studio → http://localhost:$PORT   (engine เริ่มต้น: template/offline)"
exec python3 -m uvicorn app.server:app --reload --port "$PORT"
