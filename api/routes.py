from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from api.schemas import AveragePerCountrySchema, PeopleListSchema, GenderRepartitionInCountrySchema, NbPeoplePerCountrySchema

from .dependencies import get_session
from api import services
from .openapi_response import error_server_open_api, no_content_open_api
from .cruds import bulk_insert_people, get_average_age_per_country, get_gender_repartion_in_country, get_nb_people_per_country

router = APIRouter(tags={"People"}, prefix='/v1')

# -------------------------------------------------#
#            Post. Create people in DB             #
# -------------------------------------------------#


@ router.post('/people/',
              summary="Create people in DB",
              status_code=status.HTTP_201_CREATED,
              responses={**error_server_open_api})
def create_people(data: PeopleListSchema,
                  db: Session = Depends(get_session)):
    bulk_insert_people(db, data.people)
    return "Data created"


# -------------------------------------------------#
#            Get. get average age of all the       #
#            people grouped by country.            #
# -------------------------------------------------#


@ router.get('/people/average_age/',
             summary="Get average age of all the people grouped by country",
             response_description="List of country with average age",
             response_model=List[AveragePerCountrySchema],
             status_code=status.HTTP_200_OK,
             responses={**error_server_open_api,
                        **no_content_open_api})
def get_average_age(db: Session = Depends(get_session)):
    datas = get_average_age_per_country(db)
    if not datas:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return services.make_people_average_per_country_response(datas)


# -------------------------------------------------#
#            Get. get number of people from        #
#            each country.                         #
# -------------------------------------------------#


@ router.get('/people/nb/',
             summary="Get the number of people from each country.",
             response_description="List of country with the number of people",
             response_model=List[NbPeoplePerCountrySchema],
             status_code=status.HTTP_200_OK,
             responses={**error_server_open_api,
                        **no_content_open_api})
def get_nb_people(db: Session = Depends(get_session)):
    datas = get_nb_people_per_country(db)
    if not datas:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return services.make_nb_people_per_country_response(datas)


# -------------------------------------------------#
#            Get. get  gender repartition for      #
#            a given country.                      #
# -------------------------------------------------#


@ router.get('/people/gender/{country}',
             summary="Get the gender repartition for a given country",
             response_description="Total gender in a country",
             response_model=List[GenderRepartitionInCountrySchema],
             status_code=status.HTTP_200_OK,
             responses={**error_server_open_api,
                        **no_content_open_api})
def get_gender_repartition(country: str,
                           db: Session = Depends(get_session)):
    datas = get_gender_repartion_in_country(db, country)
    if not datas:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return services.make_people_gender_repartition_in_country_response(datas)
