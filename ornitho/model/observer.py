from datetime import datetime
from typing import List, Optional

from ornitho.model.abstract import ListableModel
from ornitho.model.abstract.base_model import check_refresh
from ornitho.model.right import Right


class Observer(ListableModel):
    ENDPOINT: str = "observers"

    def __init__(self, id_) -> None:
        """Observer constructor
        :param id_: ID, which is used to get the observer from Biolovison – None if a new observation will be created
        :type id_: int
        """
        super().__init__(id_)
        self._rights: List[Right] = []

    @classmethod
    def current(cls) -> "Observer":
        url = f"{cls.ENDPOINT}/current"
        response = cls.request(method="GET", url=url)
        return cls.create_from_ornitho_json(response[0])

    @property  # type: ignore
    @check_refresh
    def external_id(self) -> int:
        return int(self._raw_data["external_id"])

    @property  # type: ignore
    @check_refresh
    def name(self) -> str:
        return self._raw_data["name"]

    @property  # type: ignore
    @check_refresh
    def surname(self) -> str:
        return self._raw_data["surname"]

    @property  # type: ignore
    @check_refresh
    def street(self) -> str:
        return self._raw_data["street"]

    @property  # type: ignore
    @check_refresh
    def number(self) -> str:
        return self._raw_data["number"]

    @property  # type: ignore
    @check_refresh
    def postcode(self) -> str:
        return self._raw_data["postcode"]

    @property  # type: ignore
    @check_refresh
    def municipality(self) -> str:
        return self._raw_data["municipality"]

    @property  # type: ignore
    @check_refresh
    def lat(self) -> float:
        return float(self._raw_data["lat"])

    @property  # type: ignore
    @check_refresh
    def lon(self) -> float:
        return float(self._raw_data["lon"])

    @property  # type: ignore
    @check_refresh
    def email(self) -> str:
        return self._raw_data["email"]

    @property  # type: ignore
    @check_refresh
    def private_phone(self) -> str:
        return self._raw_data["private_phone"]

    @property  # type: ignore
    @check_refresh
    def work_phone(self) -> str:
        return self._raw_data["work_phone"]

    @property  # type: ignore
    @check_refresh
    def mobile_phone(self) -> str:
        return self._raw_data["mobile_phone"]

    @property  # type: ignore
    @check_refresh
    def birth_year(self) -> int:
        return int(self._raw_data["birth_year"])

    @property  # type: ignore
    @check_refresh
    def atlas_list(self) -> int:
        return int(self._raw_data["atlas_list"])

    @property  # type: ignore
    @check_refresh
    def id_universal(self) -> int:
        return int(self._raw_data["id_universal"])

    @property  # type: ignore
    @check_refresh
    def display_order(self) -> str:
        return self._raw_data["display_order"]

    @property  # type: ignore
    @check_refresh
    def registration_date(self) -> datetime:
        registration_date = datetime.fromtimestamp(
            int(self._raw_data["registration_date"]["@timestamp"]),
        ).astimezone()
        return registration_date

    @property  # type: ignore
    @check_refresh
    def last_inserted_data(self) -> Optional[datetime]:
        last_inserted_data = (
            datetime.fromtimestamp(
                int(self._raw_data["last_inserted_data"]["@timestamp"]),
            ).astimezone()
            if "last_inserted_data" in self._raw_data
            else None
        )
        return last_inserted_data

    @property  # type: ignore
    @check_refresh
    def last_login(self) -> datetime:
        last_login = datetime.fromtimestamp(
            int(self._raw_data["last_login"]["@timestamp"]),
        ).astimezone()
        return last_login

    @property  # type: ignore
    @check_refresh
    def anonymous(self) -> bool:
        return False if self._raw_data.get("anonymous") == "0" else True

    @property  # type: ignore
    @check_refresh
    def hide_email(self) -> bool:
        return False if self._raw_data.get("hide_email") == "0" else True

    @property  # type: ignore
    @check_refresh
    def photo(self) -> str:
        return self._raw_data["photo"]

    @property  # type: ignore
    @check_refresh
    def species_order(self) -> str:
        return self._raw_data["species_order"]

    @property  # type: ignore
    @check_refresh
    def langu(self) -> str:
        return self._raw_data["langu"]

    @property  # type: ignore
    @check_refresh
    def item_per_page_obs(self) -> int:
        return int(self._raw_data["item_per_page_obs"])

    @property  # type: ignore
    @check_refresh
    def item_per_page_gallery(self) -> int:
        return int(self._raw_data["item_per_page_gallery"])

    @property  # type: ignore
    @check_refresh
    def archive_account(self) -> bool:
        return False if self._raw_data.get("archive_account") == "0" else True

    @property  # type: ignore
    @check_refresh
    def collectif(self) -> bool:
        return False if self._raw_data.get("collectif") == "0" else True

    @property  # type: ignore
    @check_refresh
    def use_latin_search(self) -> bool:
        return False if self._raw_data.get("use_latin_search") == "N" else True

    @property  # type: ignore
    @check_refresh
    def private_website(self) -> str:
        return self._raw_data["private_website"]

    @property  # type: ignore
    @check_refresh
    def presentation(self) -> str:
        return self._raw_data["presentation"]

    @property  # type: ignore
    @check_refresh
    def has_search_access(self) -> bool:
        return False if self._raw_data.get("has_search_access") == "0" else True

    @property  # type: ignore
    @check_refresh
    def default_hidden(self) -> bool:
        return False if self._raw_data.get("default_hidden") == "0" else True

    @property  # type: ignore
    @check_refresh
    def debug_file_upload(self) -> bool:
        return False if self._raw_data.get("debug_file_upload") == "0" else True

    @property  # type: ignore
    @check_refresh
    def mobile_use_form(self) -> bool:
        return False if self._raw_data.get("mobile_use_form") == "0" else True

    @property  # type: ignore
    @check_refresh
    def mobile_use_mortality(self) -> bool:
        return False if self._raw_data.get("mobile_use_mortality") == "0" else True

    @property  # type: ignore
    @check_refresh
    def show_precise(self) -> bool:
        return False if self._raw_data.get("show_precise") == "0" else True

    @property  # type: ignore
    @check_refresh
    def bypass_purchase(self) -> bool:
        return False if self._raw_data.get("bypass_purchase") == "0" else True

    @property  # type: ignore
    @check_refresh
    def mobile_use_protocol(self) -> bool:
        return False if self._raw_data.get("mobile_use_protocol") == "0" else True

    @property  # type: ignore
    @check_refresh
    def mobile_use_trace(self) -> bool:
        return False if self._raw_data.get("mobile_use_trace") == "0" else True

    @property  # type: ignore
    def rights(self) -> List[Right]:
        if self.id_:
            if not self._rights:
                self._rights = Right.retrieve_for_observer(self.id_)
        return self._rights
