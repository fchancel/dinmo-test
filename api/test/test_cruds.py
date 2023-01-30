from sqlalchemy.orm import Session

from ..cruds import bulk_insert_people, get_average_age_per_country, get_nb_people_per_country, get_gender_repartion_in_country
from ..schemas import PeopleSchema
from ..models import People

# -------------------------------------------------#
#                   bulk_insert_people             #
# -------------------------------------------------#


def test_bulk_insert_people_empty_data(db: Session):
    # Test with empty data
    bulk_insert_people(db, [])
    result = db.query(People).all()
    assert len(result) == 0

def test_bulk_insert_people_valid_data(db: Session):
    # Test with valid data
    datas = [
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male")
            ]
    bulk_insert_people(db, datas)

    result = db.query(People).all()
    assert len(result) == 2
    assert result[0].name == 'LeBron James'
    assert result[1].name == 'Kobe Bryant'


def test_bulk_insert_people_same_name_data(db: Session):
    # Test with valid data and same name
    datas = [
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male")
            ]
    bulk_insert_people(db, datas)

    result = db.query(People).all()
    assert len(result) == 2
    assert result[0].name == 'LeBron James'
    assert result[1].name == 'LeBron James'


# -------------------------------------------------#
#             get_average_age_per_country          #
# -------------------------------------------------#


def test_get_average_age_per_country_empty_data(db: Session):
    # Test withempty data

    result = get_average_age_per_country(db)
    assert result == []

def test_get_average_age_per_country_one_country(db: Session):
    # Test with valid data and with one country
    datas = [
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male")
            ]
    bulk_insert_people(db, datas)

    result = get_average_age_per_country(db)
    assert len(result) == 1
    assert result == [('France', 40.0)]



def test_get_average_age_per_country_two_country(db: Session):
    # Test with valid data and with two country
    datas = [
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male"),
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male")
            ]
    bulk_insert_people(db, datas)

    result = get_average_age_per_country(db)
    assert len(result) == 2
    assert result == [('France', 40.0), ('USA', 39.5)]

# -------------------------------------------------#
#             get_nb_people_per_country            #
# -------------------------------------------------#

def test_get_nb_people_per_country_with_empty_data(db: Session):
    # Test with empty data

    result = get_nb_people_per_country(db)
    assert result == []



def test_get_nb_people_per_country_one_country(db: Session):
    # Test with valid data and one country
    datas = [
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male")
            ]
    bulk_insert_people(db, datas)

    result = get_nb_people_per_country(db)
    assert len(result) == 1
    assert result == [('France', 1)]


def test_get_nb_people_per_country_two_country(db: Session):
    # Test with valid data and two country
    datas = [
                PeopleSchema(name="Kobe Bryant", age=41, country="USA", gender="male"),
                PeopleSchema(name="LeBron James", age=38, country="USA", gender="male"),
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male")
            ]
    bulk_insert_people(db, datas)

    result = get_nb_people_per_country(db)
    assert len(result) == 2
    assert result == [('France', 1), ('USA', 2)]

# -------------------------------------------------#
#             get_gender_repartion_in_country      #
# -------------------------------------------------#

def test_get_gender_repartion_in_country_with_empty_data(db: Session):
    # Test with empty data

    result = get_gender_repartion_in_country(db, 'France')
    assert result == []


def test_get_gender_repartion_in_country_with_one_gender(db: Session):
    # Test with valid data and with one gender
    datas = [
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male"),
            ]
    bulk_insert_people(db, datas)

    result = get_gender_repartion_in_country(db, 'France')
    assert result == [('male', 1)]


def test_get_gender_repartion_in_country_with_two_gender(db: Session):
    # Test with valid data and with two gender
    datas = [
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male"),
                PeopleSchema(name="Astier Pauline", age=20, country="France", gender="female")
            ]
    bulk_insert_people(db, datas)

    result = get_gender_repartion_in_country(db, 'France')
    assert result == [('female', 1), ('male', 1)]


def test_get_gender_repartion_in_country_with_two_gender_and_several_people(db: Session):
    # Test with valid data and with two gender and several people
    datas = [
                PeopleSchema(name="Batum Nicolas", age=34, country="France", gender="male"),
                PeopleSchema(name="Poirier Vincent", age=29, country="France", gender="male"),
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male"),
                PeopleSchema(name="Astier Pauline", age=20, country="France", gender="female")
            ]
    bulk_insert_people(db, datas)

    result = get_gender_repartion_in_country(db, 'France')
    assert result == [('female', 1), ('male', 3)]


def test_get_gender_repartion_in_country_with_wrong_country(db: Session):
    # Test with wrong country name
    datas = [
                PeopleSchema(name="Batum Nicolas", age=34, country="France", gender="male"),
                PeopleSchema(name="Poirier Vincent", age=29, country="France", gender="male"),
                PeopleSchema(name="Parker Tony", age=40, country="France", gender="male"),
                PeopleSchema(name="Astier Pauline", age=20, country="France", gender="female")
            ]
    bulk_insert_people(db, datas)

    result = get_gender_repartion_in_country(db, 'USA')
    assert result == []