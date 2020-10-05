import os

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

form = ornitho.Form.get(494624)

# Print all playback information
for key, value in form.playbacks.items():
    print(
        f"Playback for {ornitho.Species.get(key).english_name} {'' if value else 'not '}played!"
    )

# Check if playback was used for a specific species
print(f"Playback for species with id 338: {form.playblack_played(338)}")
print(
    f"Playback for species with id 339: {form.playblack_played(ornitho.Species.get(339))}"
)
print(f"Playback for species with id 1: {form.playblack_played(1)}")
