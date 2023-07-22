from fastapi import APIRouter

from api.v1.endpoints import hello, user, auth


api_router = APIRouter()
api_router.include_router(hello.router, tags=["Hello World"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])