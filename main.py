"""Entry point of the application
"""


from pathlib import Path
import os
import logging
import logging.config

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from app.api.v1.api import api_router
from app.core.config import settings


os.system("color")

logger = logging.getLogger()
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

LOG_FILE = "app/utils/app.log"
# logging.config.fileConfig(
#     "./app/utils/logging.ini",
#     defaults={"logfilename": LOG_FILE},
#     disable_existing_loggers=False,
# )


logger.setLevel(settings.API_DEBUG_LEVEL)


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.API_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        workers=settings.API_WORKERS,
        ssl_certfile=settings.SSL_CERTFILE,
        ssl_keyfile=settings.SSL_KEYFILE,
        log_level="info",
        log_config="./app/utils/logging.ini",
        use_colors=True,
    )
