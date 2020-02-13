from datetime import datetime
from typing import Optional

import pytz

from ornitho.model.abstract import ListableModel


class Observer(ListableModel):
    ENDPOINT: str = "observers"

    @property
    def external_id(self) -> int:
        return int(self._raw_data["external_id"])

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def surname(self) -> str:
        return self._raw_data["surname"]

    @property
    def street(self) -> str:
        return self._raw_data["street"]

    @property
    def number(self) -> str:
        return self._raw_data["number"]

    @property
    def postcode(self) -> str:
        return self._raw_data["postcode"]

    @property
    def municipality(self) -> str:
        return self._raw_data["municipality"]

    @property
    def lat(self) -> float:
        return float(self._raw_data["lat"])

    @property
    def lon(self) -> float:
        return float(self._raw_data["lon"])

    @property
    def email(self) -> str:
        return self._raw_data["email"]

    @property
    def private_phone(self) -> str:
        return self._raw_data["private_phone"]

    @property
    def work_phone(self) -> str:
        return self._raw_data["work_phone"]

    @property
    def mobile_phone(self) -> str:
        return self._raw_data["mobile_phone"]

    @property
    def birth_year(self) -> int:
        return int(self._raw_data["birth_year"])

    @property
    def atlas_list(self) -> int:
        return int(self._raw_data["atlas_list"])

    @property
    def id_universal(self) -> int:
        return int(self._raw_data["id_universal"])

    @property
    def display_order(self) -> str:
        return self._raw_data["display_order"]

    @property
    def registration_date(self) -> datetime:
        registration_date = datetime.fromtimestamp(
            int(self._raw_data["registration_date"]["@timestamp"])
        )
        return pytz.utc.localize(registration_date)

    @property
    def last_inserted_data(self) -> Optional[datetime]:
        last_inserted_data = (
            pytz.utc.localize(
                datetime.fromtimestamp(
                    int(self._raw_data["last_inserted_data"]["@timestamp"])
                )
            )
            if "last_inserted_data" in self._raw_data
            else None
        )
        return last_inserted_data

    @property
    def last_login(self) -> datetime:
        last_login = datetime.fromtimestamp(
            int(self._raw_data["last_login"]["@timestamp"])
        )
        return pytz.utc.localize(last_login)

    @property
    def anonymous(self) -> bool:
        return False if self._raw_data.get("anonymous") == "0" else True

    @property
    def hide_email(self) -> bool:
        return False if self._raw_data.get("hide_email") == "0" else True

    @property
    def photo(self) -> str:
        return self._raw_data["photo"]

    @property
    def species_order(self) -> str:
        return self._raw_data["species_order"]

    @property
    def langu(self) -> str:
        return self._raw_data["langu"]

    @property
    def item_per_page_obs(self) -> int:
        return int(self._raw_data["item_per_page_obs"])

    @property
    def item_per_page_gallery(self) -> int:
        return int(self._raw_data["item_per_page_gallery"])

    @property
    def archive_account(self) -> bool:
        return False if self._raw_data.get("archive_account") == "0" else True

    @property
    def collectif(self) -> bool:
        return False if self._raw_data.get("collectif") == "0" else True

    @property
    def use_latin_search(self) -> bool:
        return False if self._raw_data.get("use_latin_search") == "N" else True

    @property
    def private_website(self) -> str:
        return self._raw_data["private_website"]

    @property
    def presentation(self) -> str:
        return self._raw_data["presentation"]

    @property
    def has_search_access(self) -> bool:
        return False if self._raw_data.get("has_search_access") == "0" else True

    @property
    def default_hidden(self) -> bool:
        return False if self._raw_data.get("default_hidden") == "0" else True

    @property
    def debug_file_upload(self) -> bool:
        return False if self._raw_data.get("debug_file_upload") == "0" else True

    @property
    def mobile_use_form(self) -> bool:
        return False if self._raw_data.get("mobile_use_form") == "0" else True

    @property
    def mobile_use_mortality(self) -> bool:
        return False if self._raw_data.get("mobile_use_mortality") == "0" else True

    @property
    def show_precise(self) -> bool:
        return False if self._raw_data.get("show_precise") == "0" else True

    @property
    def bypass_purchase(self) -> bool:
        return False if self._raw_data.get("bypass_purchase") == "0" else True

    @property
    def mobile_use_protocol(self) -> bool:
        return False if self._raw_data.get("mobile_use_protocol") == "0" else True

    @property
    def mobile_use_trace(self) -> bool:
        return False if self._raw_data.get("mobile_use_trace") == "0" else True
