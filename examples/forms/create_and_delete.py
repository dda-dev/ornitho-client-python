import os
from datetime import datetime

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

observer = ornitho.Observer.current()
species = ornitho.Species.get(id_=386)  # Robin
atlas_code = ornitho.FieldOption.get(id_="3_2")  # A1
details = [
    ornitho.Detail(count=1, sex="M", age="U"),
    ornitho.Detail(count=1, sex="F", age="U"),
]
resting_habitat = ornitho.FieldOption.get(id_="1_5")  # Grassland
observation_detail = ornitho.FieldOption.get(id_="4_2")  # food seeking

first_observation = ornitho.Observation.create(
    observer=observer,
    species=species,
    timing=datetime.now(),
    notime=False,
    coord_lat=51.99666467623097,
    coord_lon=7.6341611553058595,
    precision=ornitho.Precision.TRANSECT_PRECISE,
    estimation_code=ornitho.EstimationCode.EXACT_VALUE,
    count=2,
    comment="TEST",
    hidden_comment="HIDDEN TEST",
    hidden=True,
    atlas_code=atlas_code,
    details=details,
    resting_habitat=resting_habitat,  # currently ignored by the API, when observation is send as part of a form
    observation_detail=observation_detail,  # currently ignored by the API, when observation is send as part of a form
    create_in_ornitho=False,
)
second_observation = ornitho.Observation.create(
    observer=observer,
    species=493,
    timing=datetime.now(),
    notime=False,
    coord_lat=51.99666467623097,
    coord_lon=7.6341611553058595,
    precision=ornitho.Precision.TRANSECT_PRECISE,
    estimation_code=ornitho.EstimationCode.EXACT_VALUE,
    count=4,
    comment="TEST",
    hidden_comment="HIDDEN TEST",
    hidden=True,
    create_in_ornitho=False,
    export_date=datetime.now(),
)

cbbm_place = ornitho.Place.list_all(
    get_hidden=1, name="DDA-Teststrecke", place_type="transect"
)[1]

form = ornitho.Form.create(
    time_start=datetime.now().time(),
    time_stop=datetime.now().time(),
    observations=[first_observation, second_observation],
    protocol="CBBM",
    place=cbbm_place.id_,
    visit_number=250,
)

print(f"New form id: {form.id_}")

form.delete()
