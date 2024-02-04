"""_summary_
"""

from fastapi import APIRouter

from app.endpoints.v1.apis import auth, hello, logs, notifications, tasks

api_router_v1 = APIRouter()

api_router_v1.include_router(
    hello.router, prefix="/hello-world", tags=["v1", "Hello World"]
)
api_router_v1.include_router(auth.router, prefix="/auth", tags=["v1", "Auth"])
api_router_v1.include_router(logs.router, prefix="/logs", tags=["v1", "Logs"])
api_router_v1.include_router(
    notifications.router, prefix="/notifications", tags=["v1", "Notifications"]
)
api_router_v1.include_router(tasks.router, prefix="/tasks", tags=["v1", "Tasks"])
