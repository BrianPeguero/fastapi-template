from fastapi import APIRouter

from app.utils.celery import create_task

router = APIRouter()


@router.post("", status_code=201)
def make_task(time: int):
    """_summary_

    Args:
        time (int): _description_

    Returns:
        _type_: _description_
    """

    task = create_task.delay(time)

    return {"task_id": task.id}
