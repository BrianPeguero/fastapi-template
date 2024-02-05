"""_summary_

Returns:
    _type_: _description_
"""

from fastapi import APIRouter

from app.utils.logging import logger

router = APIRouter()


@router.get("", status_code=200)
def hello_world():
    """_summary_

    Returns:
        _type_: _description_
    """
    logger.debug("Hello from v1")

    return {"message": "Hellow from v1"}
