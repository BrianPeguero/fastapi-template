"""_summary_
"""

from fastapi import APIRouter

from app.endpoints.v2.apis import hello

api_router_v2 = APIRouter()

api_router_v2.include_router(
    hello.router, prefix="/hello-world", tags=["v2", "Hello World"]
)
