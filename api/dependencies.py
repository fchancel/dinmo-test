from sqlalchemy.orm import Session

from config import get_settings
if get_settings().test:
    from .test.conftest import engine
else:
    from api.database import engine


def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
