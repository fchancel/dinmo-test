
import logging

from click import style
from sqlalchemy.orm import Session
from config import Settings
from api.database import create_database, engine

log = logging.getLogger('uvicorn')


def create_start_app_handler() -> None:
    async def create_db() -> None:
        log.info("Event handler: startup")
        log.info("Create database...")
        create_database()

    return create_db
