from typing import List, Optional

from ornitho.api_requester import APIRequester
from ornitho.model.abstract import BaseModel
from ornitho.model.observation import Observation


class Form(BaseModel):
    ENDPOINT: str = "observations/search"
    DEFAULT_HTTP_METHOD: str = "POST"

    def __init__(self, id_: int) -> None:
        """ Form constructor
        :param id_: ID, which is used to get the form from Biolovison
        :type id_: int
        """
        super(Form, self).__init__(id_)
        self._observations: Optional[List[BaseModel]] = None

    def instance_url(self) -> str:
        """ Returns url for this instance
        :return: Instance's url
        :rtype: str
        """
        return f"{self.ENDPOINT}"

    def refresh(self) -> "BaseModel":
        """ Refresh local model
        Call the api and refresh fields from response
        :return: Refreshed Object
        :rtype: BaseModel
        """
        with APIRequester() as requester:
            data, pagination_key = requester.request_raw(
                method="POST", url=self.instance_url(), body={"id_form": self.id_}
            )
            data = data["data"]["forms"][0]
            self._previous = self._raw_data
            self._raw_data = data
            self._observations = None
        return self

    @property
    def id_form_universal(self) -> str:
        return self._raw_data["id_form_universal"]

    @property
    def time_start(self) -> str:
        return self._raw_data["time_start"]

    @property
    def time_stop(self) -> str:
        return self._raw_data["time_stop"]

    @property
    def full_form(self) -> bool:
        return False if self._raw_data.get("full_form") == "0" else True

    @property
    def version(self) -> int:
        return int(self._raw_data["version"])

    @property
    def lat(self) -> float:
        return float(self._raw_data["lat"])

    @property
    def lon(self) -> float:
        return float(self._raw_data["lon"])

    @property
    def id_form_mobile(self) -> str:
        return self._raw_data["id_form_mobile"]

    @property
    def protocol_name(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["protocol_name"]
            if "protocol" in self._raw_data
            else None
        )

    @property
    def site_code(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["site_code"]
            if "protocol" in self._raw_data
            else None
        )

    @property
    def local_site_code(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["local_site_code"]
            if "protocol" in self._raw_data
            else None
        )

    @property
    def advanced(self) -> Optional[bool]:
        return (
            self._raw_data["protocol"]["advanced"] != "0"
            if "protocol" in self._raw_data
            else None
        )

    @property
    def visit_number(self) -> Optional[int]:
        return (
            int(self._raw_data["protocol"]["visit_number"])
            if "protocol" in self._raw_data
            else None
        )

    @property
    def sequence_number(self) -> Optional[int]:
        return (
            int(self._raw_data["protocol"]["sequence_number"])
            if "protocol" in self._raw_data
            else None
        )

    @property
    def list_type(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["list_type"]
            if "protocol" in self._raw_data
            else None
        )

    @property
    def waterbird_conditions(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["waterbird_conditions"]
            if "protocol" in self._raw_data
            and "waterbird_conditions" in self._raw_data["protocol"]
            else None
        )

    @property
    def observations(self) -> List[BaseModel]:
        if self._observations is None:
            self._observations = [
                Observation.create_from(observation)
                for observation in self._raw_data["sightings"]
            ]
        return self._observations
