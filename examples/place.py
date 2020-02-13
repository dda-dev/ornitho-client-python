import os

import ornitho

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

resp = ornitho.Place.get(id_=767)
print("Success: %r" % resp.name)

resp, pagination_key = ornitho.Place.list(id_commune=8192, request_all=True)
print("Success: %r" % len(resp))

resp, pagination_key = ornitho.Place.list()
resp2, pagination_key = ornitho.Place.list(pagination_key=pagination_key)
print("Success: %r" % len(resp + resp2))

resp = ornitho.Place.list_all()
print("Success: %r" % len(resp))

resp = ornitho.Place.list_all(get_hidden=1, name="MhB-", place_type="transect")
print("Success: %r" % len(resp))
