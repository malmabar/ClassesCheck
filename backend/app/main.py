from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(api_router)

UI_DIR = Path(__file__).resolve().parent / "ui"
UI_FILE = UI_DIR / "index.html"
app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")


def _status_to_error_code(status_code: int) -> str:
    if status_code == 400:
        return "BAD_REQUEST"
    if status_code == 401:
        return "UNAUTHORIZED"
    if status_code == 403:
        return "FORBIDDEN"
    if status_code == 404:
        return "NOT_FOUND"
    if status_code == 409:
        return "CONFLICT"
    if status_code == 422:
        return "VALIDATION_ERROR"
    if status_code >= 500:
        return "INTERNAL_SERVER_ERROR"
    return f"HTTP_{status_code}"


def _build_error_payload(
    request: Request,
    *,
    status_code: int,
    message: str,
    details,
) -> dict:
    trace_id = getattr(request.state, "trace_id", None) or request.headers.get("X-Trace-Id") or str(uuid4())
    return {
        "code": _status_to_error_code(status_code),
        "message": message,
        "details": details,
        "trace_id": trace_id,
        # Backward compatibility for clients/tests expecting `detail`.
        "detail": details,
    }


@app.middleware("http")
async def attach_trace_id(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id") or str(uuid4())
    request.state.trace_id = trace_id
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail if exc.detail is not None else "Request failed."
    message = detail if isinstance(detail, str) else "Request failed."
    payload = _build_error_payload(
        request,
        status_code=exc.status_code,
        message=message,
        details=detail,
    )
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    payload = _build_error_payload(
        request,
        status_code=422,
        message="Request validation failed.",
        details=details,
    )
    return JSONResponse(status_code=422, content=payload)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    details = {"error_type": exc.__class__.__name__}
    if settings.app_env.lower() == "development":
        details["error"] = str(exc)
    payload = _build_error_payload(
        request,
        status_code=500,
        message="Internal Server Error",
        details=details,
    )
    return JSONResponse(status_code=500, content=payload)


@app.get("/", include_in_schema=False)
def ui_index() -> HTMLResponse:
    if not UI_FILE.exists():
        return HTMLResponse(
            "<h1>UI file not found</h1>",
            status_code=500,
        )
    return HTMLResponse(UI_FILE.read_text(encoding="utf-8"))
