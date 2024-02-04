"""_summary_
"""

from fastapi import APIRouter

from app.endpoints.v1.websockets import logs, notifications

ws_router_v1 = APIRouter()

ws_router_v1.include_router(logs.router, prefix="/logs", tags=["v1", "Logs"])
ws_router_v1.include_router(
    notifications.router, prefix="/notifications", tags=["v1", "Notifications"]
)
