from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()

base_dir = Path(__file__).resolve().parent
LOG_FILE_PATH = "app/utils/app.log"

templates = Jinja2Templates(directory="app/templates")

@router.get("")
def get_logs(request: Request):
    context = {
        "title": "FastAPI Streaming Log Viewer Over Webockets",
        "log_file": LOG_FILE_PATH
    }

    return templates.TemplateResponse("index.html", {"request": request, "context": context})