from pathlib import Path
import os
import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from api.v1.api import api_router
from core.config import settings


os.system('color')

logger = logging.getLogger()
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

log_file = '/utils/app.log'
# logging.config.fileConfig('./app/utils/logging.ini', defaults={'logfilename': log_file}, disable_existing_loggers=False)

logger.setLevel(settings.API_DEBUG_LEVEL)



app = FastAPI(title="FastAPI Template")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.API_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


app.include_router(api_router, prefix="/api/v1")


@app.on_event(event_type='startup')
def startup():
    logger.debug("### Start up ###")

@app.on_event(event_type='shutdown')
def shutdown():
    logger.debug("### Shut down ###")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, 
                host=settings.API_HOST, 
                port=settings.API_PORT, 
                workers=settings.API_WORKERS, 
                ssl_certfile=settings.SSL_CERTFILE, 
                ssl_keyfile=settings.SSL_KEYFILE,
                log_level='info',
                log_config='./utils/logging.ini',
                use_colors=True
                )