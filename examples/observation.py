import os
from datetime import datetime, timedelta

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = "https://www.ornitho.de/api/"

resp = ornitho.Observation.get(id_=43050307)
print(
    f"{resp.count} {resp.species.english_name_plur}; Place: {resp.place.name};"
    f"Time: {resp.timing}, Observer: {resp.observer.surname} {resp.observer.name}"
)

# Gateway Timeout
# resp = Observation.list_all()
# print("Success: %r" % len(resp))

resp = ornitho.Observation.by_observer_all(id_observer=35)
print(
    f"Found {len(resp)} observations from {resp[0].observer.surname} {resp[0].observer.name}"
)

resp = ornitho.Observation.search_all(
    period_choice="range", date_from="31.10.2019", date_to="31.10.2019"
)
print(f"Found {len(resp)} observation between 31.10.2019 and 31.10.2019")

td = timedelta(hours=1)
resp = ornitho.Observation.diff(datetime.now() - td)
print(f"Found {len(resp)} observation in the last hour!")

td = timedelta(days=1)
resp = ornitho.Observation.diff(
    datetime.now() - td, modification_type=ornitho.ModificationType.ONLY_DELETED
)
print(f"Found {len(resp)} deleted observation in the last 24 hours!")
