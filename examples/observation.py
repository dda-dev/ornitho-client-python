import os
from datetime import datetime, timedelta

import pytz

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")


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
print(f"Found {len(resp)} observations between 31.10.2019 and 31.10.2019")

td = timedelta(hours=1)
resp = ornitho.Observation.diff(datetime.now() - td)
print(
    f"Found {len(resp[ornitho.ModificationType.ONLY_MODIFIED]) + len(resp[ornitho.ModificationType.ONLY_DELETED])} observation in the last hour!"
)

td = timedelta(days=1)
resp = ornitho.Observation.diff(
    datetime.now().astimezone(pytz.timezone("Asia/Tokyo")) - timedelta(hours=1) - td,
    modification_type=ornitho.ModificationType.ONLY_DELETED,
)
print(
    f"Found {len(resp[ornitho.ModificationType.ONLY_DELETED])} deleted observation in the last 24 hours!"
)
