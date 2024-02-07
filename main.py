"""_summary_
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.core.config import settings
from app.db.database import close_db, init_db
from app.endpoints.v1.api import api_router_v1
from app.endpoints.v1.ws import ws_router_v1
from app.endpoints.v2.api import api_router_v2
from app.utils.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """_summary_

    Args:
        app (FastAPI): _description_
    """
    logger.debug("*** Start Up ***")
    await init_db()
    yield
    await close_db()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """_summary_

    Args:
        request (Request): _description_
        call_next (_type_): _description_

    Returns:
        _type_: _description_
    """

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-time"] = str(process_time)

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[host.strip() for host in settings.API_ALLOW_ORIGINS.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# import routes
app.include_router(api_router_v1, prefix="/api/v1")
app.include_router(api_router_v2, prefix="/api/v2")
app.include_router(ws_router_v1, prefix="/ws/v1")


@app.get("/")
def main():
    """redirecting to swagger docs when root is reached

    Returns:
        _type_: _description_
    """
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        workers=settings.API_WORKERS,
        reload=False,
        log_config="./app/utils/logging.ini",
        log_level="info",
        use_colors=True,
        timeout_graceful_shutdown=5,
    )
