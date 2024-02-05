from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.security.notifition import Notification
from app.schemas import notification_schema


async def get_all_notifications(db: AsyncSession) -> List[Notification]:
    """_summary_

    Args:
        db (AsyncSession): _description_

    Returns:
        List[Notification]: _description_
    """

    results = await db.execute(select(Notification))

    return results.scalar().all()


async def get_notification_by_id(notif_id: int, db: AsyncSession) -> List[Notification]:
    """_summary_

    Args:
        notif_id (int): _description_
        db (AsyncSession): _description_

    Returns:
        List[Notification]: _description_
    """

    results = await db.execute(select(Notification).where(Notification.id == notif_id))

    return results.scalar().first()


async def get_all_notifications_by_user_id(
    user_id: int, db: AsyncSession
) -> List[Notification]:
    """_summary_

    Args:
        user_id (int): _description_
        db (AsyncSession): _description_

    Returns:
        List[Notification]: _description_
    """

    results = await db.execute(
        select(Notification).where(Notification.user_id_to == user_id)
    )

    return results.scalar().all()


async def create_notification(
    notification: notification_schema.NotificationCreate, db: AsyncSession
):
    create_data = notification.dict()
    db_obj = Notification(**create_data)
    await db.add(db_obj)
    await db.commit()

    return db_obj
