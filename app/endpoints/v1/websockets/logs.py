import asyncio
from pathlib import Path

from fastapi import APIRouter, WebSocket
from fastapi.templating import Jinja2Templates

from app.utils.logging import logger

router = APIRouter()

base_dir = Path(__file__).resolve().parent
LOG_FILE_PATH = "app/utils/app.log"

templates = Jinja2Templates(directory="app/templates")


async def log_reader():
    """_summary_

    Returns:
        _type_: _description_
    """

    log_lines = []
    with open(f"{LOG_FILE_PATH}", "r", encoding="utf-8") as file:
        for line in file.readlines():
            if "ERROR" in line:
                log_lines.append(f'<span class="text-red-400"></span>{line}<br/>')
            if "WARNING" in line:
                log_lines.append(f'<span class="text-orange-300"></span>{line}<br/>')
            else:
                log_lines.append(f"{line}<br/>")
        return log_lines


@router.websocket("/")
async def ws_logs_endpoint(websocket: WebSocket):
    """_summary_

    Args:
        websocket (WebSocket): _description_
    """

    await websocket.accept()

    try:
        while True:
            await asyncio.sleep(1)
            logs = await log_reader()
            await websocket.send_text(logs)
    except Exception as e:
        logger.debug(e)
    finally:
        await websocket.close()
