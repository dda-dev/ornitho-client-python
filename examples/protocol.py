import os

import ornitho
from ornitho import MapLayer

ornitho.consumer_key = os.environ.get("ORNITHO_CONSUMER_KEY")
ornitho.consumer_secret = os.environ.get("ORNITHO_CONSUMER_SECRET")
ornitho.user_email = os.environ.get("ORNITHO_USER_EMAIL")
ornitho.user_pw = os.environ.get("ORNITHO_USER_PW")
ornitho.api_base = os.environ.get("ORNITHO_API_BASE")

resp = ornitho.Protocol.list_all()
for protocol in resp:
    print(f"Protocol {protocol.name} has id {protocol.id_}")

resp = ornitho.Protocol.get(25)
print(
    f"Protocol {resp.name} has entity {resp.entity.full_name_german} and {len(resp.sites)} sites"
)

with open(f"./{resp.sites[2].custom_name}.pdf", "wb") as file:
    file.write(resp.sites[2].pdf(map_layer=MapLayer.OSMLIVE, boundary=True))
