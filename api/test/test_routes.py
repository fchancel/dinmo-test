from unittest.mock import patch
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from fastapi.testclient import TestClient
from unittest import mock

from ..schemas import AveragePerCountrySchema, PeopleSchema, PeopleListSchema, NbPeoplePerCountrySchema, GenderRepartitionInCountrySchema
from ..routes import create_people
from ..models import People
from main import api
import pytest


client = TestClient(api)


# -------------------------------------------------#
#             Post - create_people                 #
# -------------------------------------------------#


def test_create_people_without_data(db: Session):
    response = client.post("/api/v1/people")
    assert response.status_code == 422



def test_create_people_wrong_format(db: Session):
    datas = {
        "people": [
            {
                "name": "LeBron James",
                "age": 38,
                "gender": "male"
            },
            {
                "name": "Kobe Bryant",
                "age": 41,
                "country": "USA",
                "gender": "male"
            }
        ]
    }

    response = client.post("/api/v1/people", json=datas)
    assert response.status_code == 422


def test_create_people(db: Session):
    datas = PeopleListSchema(people=[
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male")
            ])
    response = client.post("/api/v1/people", json=datas.dict())
    assert response.status_code == 201
    assert response.json() == "Data created"

    result = db.query(People).all()
    assert len(result) == 2 


# -------------------------------------------------#
#             Get - get_average_age                #
# -------------------------------------------------#

def test_get_average_age_no_data(db: Session):
    response = client.get("/api/v1/people/average_age")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_average_age_one_country(db: Session):
    datas = PeopleListSchema(people=[
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male")
            ])
    create_people(datas, db)
    response = client.get("/api/v1/people/average_age")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [AveragePerCountrySchema(country='USA', average=39)]


def test_get_average_age_two_country(db: Session):
    datas = PeopleListSchema(people=[
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male"),
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male")

            ])
    create_people(datas, db)
    response = client.get("/api/v1/people/average_age")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==  [
                AveragePerCountrySchema(country='France', average=40),
                AveragePerCountrySchema(country='USA', average=39)
                ]

# -------------------------------------------------#
#             Get - get_nb_people                  #
# -------------------------------------------------#

def test_get_nb_people_no_data(db: Session):
    response = client.get("/api/v1/people/nb")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_nb_people_one_country(db: Session):
    datas = PeopleListSchema(people=[
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male")
            ])
    create_people(datas, db)
    response = client.get("/api/v1/people/nb")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [NbPeoplePerCountrySchema(country='USA', total=2)]


def test_get_nb_people_two_country(db: Session):
    datas = PeopleListSchema(people=[
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male"),
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male")
            ])

    create_people(datas, db)
    response = client.get("/api/v1/people/nb")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        NbPeoplePerCountrySchema(country='France', total=1),
        NbPeoplePerCountrySchema(country='USA', total=2)
        ]


# -------------------------------------------------#
#             Get - get_gender_repartition         #
# -------------------------------------------------#
def test_get_gender_no_data(db: Session):
    response = client.get("/api/v1/people/gender/no-data")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_gender_repartition_one_gender(db: Session):
    datas = PeopleListSchema(people=[
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male")
            ])
    create_people(datas, db)
    response = client.get("/api/v1/people/gender/USA")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [GenderRepartitionInCountrySchema(gender='male', total=2)]


def test_get_gender_repartition_two_gender(db: Session):
    datas = PeopleListSchema(people=[
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male"),
                PeopleSchema(name="Parker Candace", age=36, country="USA", gender="female")
            ])

    create_people(datas, db)
    response = client.get("/api/v1/people/gender/USA")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        GenderRepartitionInCountrySchema(gender='female', total=1),
        GenderRepartitionInCountrySchema(gender='male', total=2)
    ]
