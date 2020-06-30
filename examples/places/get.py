import os

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

place = ornitho.Place.get(id_=17152)
print(f"Place with ID {place.id_}: {place.name} / {place.municipality}")
