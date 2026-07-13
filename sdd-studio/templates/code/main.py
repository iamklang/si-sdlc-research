# T012–T013 — FastAPI app + middleware (Observable) + error handler กลาง
import time
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .db import init_db
from .routes import router

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("todo")

app = FastAPI(title="To-do Task API", version="1.0.0")

# สร้าง schema ตั้งแต่ตอน import — กันกรณี TestClient ไม่ trigger startup event
init_db()


@app.on_event("startup")
def _startup():
    init_db()


@app.middleware("http")                       # หลัก IV. Observable
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    ms = (time.perf_counter() - start) * 1000
    log.info(
        '{"method":"%s","path":"%s","status":%d,"ms":%.1f}',
        request.method, request.url.path, response.status_code, ms,
    )
    return response


def _error(status: int, code: str, message: str):    # error shape กลาง
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@app.exception_handler(StarletteHTTPException)
async def http_exc(request, exc):
    return _error(exc.status_code, "http_error", str(exc.detail))


@app.exception_handler(RequestValidationError)       # FR-008
async def validation_exc(request, exc):
    return _error(422, "validation_error", "invalid input")


app.include_router(router)

# รัน: uvicorn src.main:app --reload
