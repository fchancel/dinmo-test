import logging
from fastapi import FastAPI
import uvicorn
from api.events import create_start_app_handler

from api.routes import router
from config import Settings, get_settings


log = logging.getLogger("uvicorn")


def create_application(settings: Settings) -> FastAPI:
    # FastAPI application
    log.info("Creating application ...")

    api = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        docs_url=settings.documentation_url,
    )

    # Routes
    log.info("  ... add routes ...")
    api.include_router(router, prefix="/api")

    # Event handlers registration
    log.info("  ... add events handlers ...")
    api.add_event_handler("startup", create_start_app_handler())
    return api


api = create_application(get_settings())

if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000)
