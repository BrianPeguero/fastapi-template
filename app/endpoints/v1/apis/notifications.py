from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import notification_crud, user_crud
from app.db.database import get_session
from app.endpoints.v1.websockets.notifications import manager
from app.schemas import notification_schemas

router = APIRouter()


@router.get("")
async def get_notification(db: AsyncSession = Depends(get_session)):
    """_summary_

    Args:
        db (AsyncSession, optional): _description_. Defaults to Depends(get_session).

    Returns:
        _type_: _description_
    """

    return await notification_crud.get_all_notifications(db=db)


@router.get("/id/{notif_id}")
async def get_notification_by_id(
    notif_id: int, db: AsyncSession = Depends(get_session)
):
    """_summary_

    Args:
        notif_id (int): _description_
        db (AsyncSession, optional): _description_. Defaults to Depends(get_session).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    notification = await notification_crud.get_notification_by_id(
        notif_id=notif_id, db=db
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Notification {notif_id}, not found",
        )

    return notification


@router.get("/user/{user_id}")
async def get_notification_by_user_id(
    user_id: int, db: AsyncSession = Depends(get_session)
):
    """_summary_

    Args:
        user_id (int): _description_
        db (AsyncSession, optional): _description_. Defaults to Depends(get_session).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    user = await user_crud.get_user_by_id(user_id=user_id, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User, {user_id} not found"
        )

    return await notification_crud.get_all_notifications_by_user_id(
        user_id=user_id, db=db
    )


@router.post("", response_model=notification_schemas.Notification)
async def create_notification(
    notif_in: notification_schema.NotificationCreate,
    db: AsyncSession = Depends(get_session),
):
    """_summary_

    Args:
        notif_in (notification_schema.NotificationCreate): _description_
        db (AsyncSession, optional): _description_. Defaults to Depends(get_session).

    Returns:
        _type_: _description_
    """

    notification = await notification_crud.create_notification(notif_in=notif_in, db=db)

    await manager.broadcast(notification.user_id_to, db)

    return notification


@router.delete("/id/{notif_id}")
async def delete_notification(notif_id: int, db: AsyncSession = Depends(get_session)):
    """_summary_

    Args:
        notif_id (int): _description_
        db (AsyncSession, optional): _description_. Defaults to Depends(get_session).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """

    notification = await notification_crud.get_notification_by_id(
        notif_id=notif_id, db=db
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification, {notif_id}, not found",
        )

    return {"message": f"Successfully deleted, {notif_id}"}
