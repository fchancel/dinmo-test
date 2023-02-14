import logging

from pydantic import BaseSettings
from functools import lru_cache
from os import environ
from sys import exit

log = logging.getLogger('uvicorn')


class Settings(BaseSettings):
    app_title: str = "EXAMPLE API"
    app_description: str = "A Crazy API"
    documentation_url: str = "/docs"
    test: bool = environ.get("TEST")
    db_url: str = "sqlite:///db/people.db"


@ lru_cache()
def get_settings() -> Settings:
    settings = None
    try:
        settings = Settings()
    except ValueError as err:
        log.critical(err)
        exit(1)
    return settings
