from typing import List, Tuple, Optional

from api.schemas import AveragePerCountrySchema, NbPeoplePerCountrySchema, GenderRepartitionInCountrySchema


def make_people_average_per_country_response(datas: Optional[List[Tuple[str, float]]]) -> List[Optional[AveragePerCountrySchema]]:
    if datas:
        return [AveragePerCountrySchema(country=data[0], average=data[1]) for data in datas]
    return []

def make_nb_people_per_country_response(datas: Optional[List[Tuple[str, float]]]) -> List[Optional[NbPeoplePerCountrySchema]]:
    if datas:
        return [NbPeoplePerCountrySchema(country=data[0], total=data[1]) for data in datas]
    return []

def make_people_gender_repartition_in_country_response(datas: Optional[List[Tuple[str, float]]]) -> List[Optional[GenderRepartitionInCountrySchema]]:
    if datas:
        return [GenderRepartitionInCountrySchema(gender=data[0], total=data[1]) for data in datas]
    return []