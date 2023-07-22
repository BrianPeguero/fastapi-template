from fastapi import APIRouter
from typing import Any

import logging

logger = logging.getLogger()

router = APIRouter()


@router.get("/hello", status_code=200)
def hello() -> Any:
    logger.debug("hello from logger")
    return {"message": "Hello World"}