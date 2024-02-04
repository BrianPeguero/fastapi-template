"""_summary_

Returns:
    _type_: _description_
"""

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import notification_crud
from app.db.database import get_session
from app.utils.logging import logger

router = APIRouter()


class NotificationConnetionManager:
    """_summary_"""

    def __init__(self):
        """_summary_"""

        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, user_id: int, db: AsyncSession):
        """_summary_

        Args:
            websocket (WebSocket): _description_
            user_id (int): _description_
            db (AsyncSession): _description_
        """

        await websocket.accept()
        self.active_connections.append(websocket)
        notifications = await get_notifications_ws(user_id=user_id, db=db)

        await websocket.send_json(jsonable_encoder(notifications))

    def disconnect(self, websocket: WebSocket):
        """_summary_

        Args:
            websocket (WebSocket): _description_
        """

        self.active_connections.remove(websocket)

    async def send_notification(
        self, websocket: WebSocket, user_id: int, db: AsyncSession
    ):
        """_summary_

        Args:
            websocket (WebSocket): _description_
            user_id (int): _description_
            db (AsyncSession): _description_
        """

        notifications = await get_notifications_ws(user_id=user_id, db=db)
        await websocket.send_json(jsonable_encoder(notifications))

    async def broadcast(self, user_id: int, db: AsyncSession):
        """_summary_

        Args:
            user_id (int): _description_
            db (AsyncSession): _description_
        """

        for connection in self.active_connections:
            conn = connection.__dict__
            path_params_user_id = int(conn["scope"]["path_params"]["user_id"])
            if path_params_user_id == user_id:
                notifications = await get_notifications_ws(user_id=user_id, db=db)

                await connection.send_json(jsonable_encoder(notifications))


manager = NotificationConnetionManager()


async def get_notifications_ws(user_id: int, db: AsyncSession):
    """_summary_

    Args:
        user_id (int): _description_
        db (AsyncSession): _description_

    Returns:
        _type_: _description_
    """

    return await notification_crud.get_all_notifications_by_user_id(
        user_id=user_id, db=db
    )


@router.websocket("/{uer_id}")
async def websocket_endpoint_notification(
    user_id: int, websocket: WebSocket, db: AsyncSession = Depends(get_session)
):
    """_summary_

    Args:
        user_id (int): _description_
        websocket (WebSocket): _description_
        db (AsyncSession, optional): _description_. Defaults to Depends(get_session).
    """

    await manager.connect(websocket, user_id=user_id, db=db)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
