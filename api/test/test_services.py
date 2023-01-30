
from ..schemas import GenderRepartitionInCountrySchema, NbPeoplePerCountrySchema, AveragePerCountrySchema
from ..services import make_nb_people_per_country_response, make_people_average_per_country_response, make_people_gender_repartition_in_country_response

def test_make_people_average_per_country_responsee():
    # Test with valid data
    data = [("France", 50.0), ("Colombia", 50.0)]
    expected_response = [AveragePerCountrySchema(country="France", average=50.0), AveragePerCountrySchema(country="Colombia", average=50.0)]
    assert make_people_average_per_country_response(data) == expected_response

    # Test with empty data
    assert make_people_average_per_country_response([]) == []

    # Test with None data
    assert make_people_average_per_country_response(None) == []

def test_make_nb_people_per_country_response():
    # Test with valid data
    data = [("France", 50), ("Colombia", 50)]
    expected_response = [NbPeoplePerCountrySchema(country="France", total=50), NbPeoplePerCountrySchema(country="Colombia", total=50)]
    assert make_nb_people_per_country_response(data) == expected_response

    # Test with empty data
    assert make_nb_people_per_country_response([]) == []

    # Test with None data
    assert make_nb_people_per_country_response(None) == []


def test_make_people_gender_repartition_in_country_response():
    # Test with valid data
    data = [("female", 50), ("male", 50)]
    expected_response = [GenderRepartitionInCountrySchema(gender="female", total=50), GenderRepartitionInCountrySchema(gender="male", total=50)]
    assert make_people_gender_repartition_in_country_response(data) == expected_response

    # Test with empty data
    assert make_people_gender_repartition_in_country_response([]) == []

    # Test with None data
    assert make_people_gender_repartition_in_country_response(None) == []
