from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

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


@app.get("/", include_in_schema=False)
def ui_index() -> HTMLResponse:
    if not UI_FILE.exists():
        return HTMLResponse(
            "<h1>UI file not found</h1>",
            status_code=500,
        )
    return HTMLResponse(UI_FILE.read_text(encoding="utf-8"))
