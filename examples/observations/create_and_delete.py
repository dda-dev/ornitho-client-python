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

new_observation = ornitho.Observation.create(
    observer=observer,
    species=species,
    timing=datetime.now(),
    coord_lat=51.99666467623097,
    coord_lon=7.6341611553058595,
    precision=ornitho.Precision.PRECISE,
    estimation_code=ornitho.EstimationCode.MINIMUM,
    count=2,
    comment="TEST",
    hidden_comment="HIDDEN TEST",
    hidden=True,
    atlas_code=atlas_code,
    details=details,
    resting_habitat=resting_habitat,
    observation_detail=observation_detail,
)

print(
    f"{new_observation.count} {new_observation.species.name}; Place: {new_observation.place.name}; "
    f"Time: {new_observation.timing}; Observer: {new_observation.observer.name}; Altitude: {new_observation.altitude}"
)
new_observation.delete()
