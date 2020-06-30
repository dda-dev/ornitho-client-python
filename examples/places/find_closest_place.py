import os

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

lat = 51.99666467623097
lon = 7.6341611553058595

# Get closest place from coordinates
closest_place = ornitho.Place.find_closest_place(coord_lat=lat, coord_lon=lon)
print(
    f"Closest place for {lat}, {lon}: {closest_place.id_} – {closest_place.name} / {closest_place.municipality}"
)

# Get closest hidden place from coordinates
closest_hidden_place = ornitho.Place.find_closest_place(
    coord_lat=lat, coord_lon=lon, get_hidden=True
)
print(
    f"Closest hidden place for {lat}, {lon}: {closest_hidden_place.id_} – {closest_hidden_place.name} / {closest_hidden_place.municipality}"
)
