from fastapi import APIRouter
from typing import Any

from app.utils.logging import logger


router = APIRouter()


@router.get("/hello", status_code=200)
def hello() -> Any:
    logger.debug("hello from logger")
    return {"message": "Hello World"}
