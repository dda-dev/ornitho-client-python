from datetime import date, time
from typing import List, Optional

import ornitho.model.observation
from ornitho.api_exception import APIException
from ornitho.api_requester import APIRequester
from ornitho.model.abstract import BaseModel


class Form(BaseModel):
    ENDPOINT: str = "observations/search"

    def __init__(self, id_: int) -> None:
        """ Form constructor
        :param id_: ID, which is used to get the form from Biolovison
        :type id_: int
        """
        super(Form, self).__init__(id_)
        self._observations: Optional[List[ornitho.model.observation.Observation]] = None

    def instance_url(self) -> str:
        """ Returns url for this instance
        :return: Instance's url
        :rtype: str
        """
        return f"{self.ENDPOINT}"

    def refresh(self, short_version: bool = False) -> "Form":
        """ Refresh local model
        Call the api and refresh fields from response
        :return: Refreshed Object
        :rtype: Form
        """
        with APIRequester() as requester:
            data, pagination_key = requester.request_raw(
                method="POST",
                url=self.instance_url(),
                short_version=short_version,
                body={"id_form": self.id_},
            )
            if "data" in data and "forms" in data["data"]:
                data = data["data"]["forms"][0]
                self._previous = self._raw_data
                self._raw_data = data
                self._observations = None
            else:
                raise APIException(f"Unrecognized response: {data}")
        return self

    @property
    def id_form_universal(self) -> str:
        return self._raw_data["id_form_universal"]

    @property
    def day(self) -> date:
        if "day" in self._raw_data:
            return date.fromtimestamp(int(self._raw_data["day"]["@timestamp"]),)
        return self.observations[0].timing.date()

    @property
    def time_start(self) -> time:
        splitted = self._raw_data["time_start"].split(":")
        return time(
            hour=int(splitted[0]), minute=int(splitted[1]), second=int(splitted[2]),
        )

    @property
    def time_stop(self) -> time:
        splitted = self._raw_data["time_stop"].split(":")
        return time(
            hour=int(splitted[0]), minute=int(splitted[1]), second=int(splitted[2]),
        )

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
    def comment(self) -> Optional[str]:
        return self._raw_data["comment"] if "comment" in self._raw_data else None

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
    def id_waterbird_conditions(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_conditions" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_conditions"]) is dict:
                return self._raw_data["protocol"]["waterbird_conditions"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_conditions"].split(",")[0]
        return None

    @property
    def id_waterbird_coverage(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_coverage" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_coverage"]) is dict:
                return self._raw_data["protocol"]["waterbird_coverage"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_coverage"].split(",")[0]
        return None

    @property
    def id_waterbird_optical(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_optical" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_optical"]) is dict:
                return self._raw_data["protocol"]["waterbird_optical"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_optical"].split(",")[0]
        return None

    @property
    def id_waterbird_countmethod(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_countmethod" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_countmethod"]) is dict:
                return self._raw_data["protocol"]["waterbird_countmethod"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_countmethod"].split(",")[0]
        return None

    @property
    def id_waterbird_ice(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_ice" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_ice"]) is dict:
                return self._raw_data["protocol"]["waterbird_ice"]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"]["waterbird_ice"].split(",")[0]
        return None

    @property
    def id_waterbird_snowcover(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_snowcover" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_snowcover"]) is dict:
                return self._raw_data["protocol"]["waterbird_snowcover"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_snowcover"].split(",")[0]
        return None

    @property
    def id_waterbird_waterlevel(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_waterlevel" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_waterlevel"]) is dict:
                return self._raw_data["protocol"]["waterbird_waterlevel"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_waterlevel"].split(",")[0]
        return None

    @property
    def nest_number(self) -> Optional[int]:
        if "protocol" in self._raw_data and "nest_number" in self._raw_data["protocol"]:
            if type(self._raw_data["protocol"]["nest_number"]) is dict:
                return int(self._raw_data["protocol"]["nest_number"]["@id"])
            else:
                return int(self._raw_data["protocol"]["nest_number"])
        return None

    @property
    def occupied_nest_number(self) -> Optional[int]:
        if (
            "protocol" in self._raw_data
            and "occupied_nest_number" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["occupied_nest_number"]) is dict:
                return int(self._raw_data["protocol"]["occupied_nest_number"]["@id"])
            else:
                return int(self._raw_data["protocol"]["occupied_nest_number"])
        return None

    @property
    def observations(self):
        if "sightings" not in self._raw_data:
            self.refresh()
        if self._observations is None and "sightings" in self._raw_data:
            self._observations = [
                ornitho.model.observation.Observation.create_from(observation)
                for observation in self._raw_data["sightings"]
            ]
        return self._observations
