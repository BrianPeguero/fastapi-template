"""Entry point of the application
"""


import time

import os

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from starlette.responses import RedirectResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.utils.logging import logger


os.system("color")


@asynccontextmanager
# pylint: disable-next=redefined-outer-name,unused-argument
async def lifespan(app: FastAPI):
    """The lifespan function defines code that needs to be executed before the
    application starts up and also code that should be executed after shutdown

    Args:
        app (FastAPI): The application
    """

    # code to execute before start up
    logger.debug("*** Start Up ***")
    yield
    # code to execute after the app shuts down
    logger.debug("*** Shutdown ***")


app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)


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
    response.headers["X-process-Time"] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.API_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def docs_redirect():
    """_summary_

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
        ssl_certfile=settings.SSL_CERTFILE,
        ssl_keyfile=settings.SSL_KEYFILE,
        log_level="info",
        log_config="./app/utils/logging.ini",
        use_colors=True,
        reload=False,
        timeout_graceful_shutdown=5,
    )
