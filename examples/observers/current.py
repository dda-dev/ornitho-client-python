import os

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

current_observer = ornitho.Observer.current()

print(
    f"Logged in user: {current_observer.surname} {current_observer.name} – ID={current_observer.id_}, registered on {current_observer.registration_date}"
)

print("Rights:")
for right in current_observer.rights:
    print(right)
