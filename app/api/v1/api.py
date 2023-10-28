from fastapi import APIRouter

from app.api.v1.endpoints import hello, user, auth


api_router = APIRouter()
api_router.include_router(hello.router, tags=["Hello World", "v1"])
api_router.include_router(user.router, prefix="/user", tags=["User", "v1"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth", "v1"])
