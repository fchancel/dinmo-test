from pydantic import BaseModel
from typing import List


class PeopleSchema(BaseModel):
    name: str
    age: int
    gender: str
    country: str


class PeopleListSchema(BaseModel):
    people: List[PeopleSchema]


class AveragePerCountrySchema(BaseModel):
    country: str
    average: int


class NbPeoplePerCountrySchema(BaseModel):
    country: str
    total: int


class GenderRepartitionInCountrySchema(BaseModel):
    gender: str
    total: int
