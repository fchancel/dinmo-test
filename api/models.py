from sqlalchemy import Column, String, Integer
from config import get_settings
if get_settings().test:
    from .test.conftest import Base
else:
    from .database import Base


class People(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    age = Column(Integer)
    gender = Column(String(255), index=True)
    country = Column(String(60), index=True)
