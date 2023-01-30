from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Tuple, Optional

from api.models import People
from api.schemas import PeopleSchema


def bulk_insert_people(db: Session, datas: List[PeopleSchema]):
    db.bulk_insert_mappings(People, datas)
    db.commit()


def get_average_age_per_country(db: Session) -> Optional[List[Tuple[str, float]]]:
    return db.query(People.country, func.avg(People.age)).group_by(People.country).all()


def get_nb_people_per_country(db: Session) -> Optional[List[Tuple[str, int]]]:
    return db.query(People.country, func.count(People.id)).group_by(People.country).all()


def get_gender_repartion_in_country(db: Session, country: str) -> Optional[List[Tuple[str, int]]]:
    return db.query(People.gender, func.count(People.id)).filter(People.country == country).group_by(People.gender).all()
