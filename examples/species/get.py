import os

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

species = ornitho.Species.get(id_=366)
ornitho.Species.get(id_=366)
ornitho.Species.get(id_=366)
ornitho.Species.get(id_=366)
print(f"Species with ID {species.id_}: {species.german_name} / {species.latin_name}")
