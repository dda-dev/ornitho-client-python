import os

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

# Get places by commune
places_by_commune = ornitho.Place.list_all(id_commune=12827)
print(
    f"Found {len(places_by_commune)} places for commune {places_by_commune[0].commune.name} found!"
)

# Get first 2 pages of all places
first_page, pagination_key = ornitho.Place.list()
second_page, pagination_key = ornitho.Place.list(pagination_key=pagination_key)
print(f"The first 2 pages contains {len(first_page + second_page)} places!")

# Get all places
all_places = ornitho.Place.list_all()
print(f"Found {len(all_places)} places!")

# Get hidden places, which names begins with "MhB-" and transects
transect_places = ornitho.Place.list_all(
    get_hidden=1, name="MhB-", place_type="transect"
)
print(f"Found {len(transect_places)} transect places!")
