from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import ornitho.model.form
from ornitho import APIException
from ornitho.model.abstract import BaseModel, ListableModel, SearchableModel
from ornitho.model.abstract.base_model import check_raw_data
from ornitho.model.detail import Detail
from ornitho.model.field_option import FieldOption
from ornitho.model.media import Media
from ornitho.model.observer import Observer
from ornitho.model.place import Place
from ornitho.model.species import Species


class ModificationType(Enum):
    ONLY_MODIFIED = "only_modified"
    ONLY_DELETED = "only_deleted"
    ALL = "all"


class Observation(ListableModel, SearchableModel):
    """Representation of on Observation"""

    ENDPOINT: str = "observations"

    def __init__(self, id_: int, modification_type: ModificationType = None) -> None:
        """ Observation constructor
        :param id_: ID, which is used to get the observation from Biolovison
        :param modification_type: Set, if the observation was retrieved via the 'diff' method
        :type id_: int
        :type modification_type: ModificationType
        """
        super(Observation, self).__init__(id_)
        self.modification_type = modification_type
        self._species: Optional[Species] = None
        self._observer: Optional[Observer] = None
        self._place: Optional[Place] = None
        self._form: Optional[ornitho.model.form.Form] = None
        self._resting_habitat: Optional[FieldOption] = None
        self._observation_detail: Optional[FieldOption] = None
        self._atlas_code: Optional[FieldOption] = None
        self._medias: Optional[List[Media]] = None

    @classmethod
    def create_from(cls, data: Dict[str, Any]) -> "Observation":
        if len(data["observers"]) > 1:
            raise APIException(
                f"More than one observer in sightings json found!\n{data['observers']}"
            )
        identifier: int = int(data["observers"][0]["id_sighting"])
        obj = cls(identifier)
        obj._raw_data = data
        return obj

    @property  # type: ignore
    @check_raw_data("observers")
    def id_observer(self) -> int:
        return int(self._raw_data["observers"][0]["@id"])

    @property  # type: ignore
    @check_raw_data("observers")
    def traid(self) -> int:
        return int(self._raw_data["observers"][0]["traid"])

    @property  # type: ignore
    @check_raw_data("observers")
    def timing(self) -> datetime:
        timing = datetime.fromtimestamp(
            int(self._raw_data["observers"][0].get("timing")["@timestamp"]),
        ).astimezone()
        return timing

    @property  # type: ignore
    @check_raw_data("observers")
    def coord_lat(self) -> float:
        return float(self._raw_data["observers"][0]["coord_lat"])

    @property  # type: ignore
    @check_raw_data("observers")
    def coord_lon(self) -> float:
        return float(self._raw_data["observers"][0]["coord_lon"])

    @property  # type: ignore
    @check_raw_data("observers")
    def altitude(self) -> int:
        return int(self._raw_data["observers"][0]["altitude"])

    @property  # type: ignore
    @check_raw_data("observers")
    def id_form(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["id_form"])
            if "id_form" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def precision(self) -> str:
        return self._raw_data["observers"][0]["precision"]

    @property  # type: ignore
    @check_raw_data("observers")
    def estimation_code(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["estimation_code"]
            if "estimation_code" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("species")
    def id_species(self) -> int:
        return int(self._raw_data["species"]["@id"])

    @property  # type: ignore
    @check_raw_data("observers")
    def count(self) -> int:
        return int(self._raw_data["observers"][0]["count"])

    @property  # type: ignore
    @check_raw_data("observers")
    def flight_number(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["flight_number"])
            if "flight_number" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def admin_hidden(self) -> bool:
        return (
            False
            if "admin_hidden" not in self._raw_data["observers"][0]
            or self._raw_data["observers"][0]["admin_hidden"] == "0"
            else True
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def admin_hidden_type(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["admin_hidden_type"]
            if "admin_hidden_type" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def source(self) -> str:
        return self._raw_data["observers"][0]["source"]

    @property  # type: ignore
    @check_raw_data("observers")
    def medias(self) -> Optional[List[Media]]:
        if self._medias is None and "medias" in self._raw_data["observers"][0]:
            self._medias = [
                Media.get(media["@id"])
                for media in self._raw_data["observers"][0]["medias"]
            ]
        return self._medias

    @property  # type: ignore
    @check_raw_data("observers")
    def media_urls(self) -> Optional[List[str]]:
        if "medias" in self._raw_data["observers"][0]:
            return [
                f"{media['path']}/{media['filename']}"
                for media in self._raw_data["observers"][0]["medias"]
            ]
        return None

    @property  # type: ignore
    @check_raw_data("observers")
    def comment(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["comment"]
            if "comment" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def hidden_comment(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["hidden_comment"]
            if "hidden_comment" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def hidden(self) -> bool:
        return (
            False
            if "hidden" not in self._raw_data["observers"][0]
            or self._raw_data["observers"][0]["hidden"] == "0"
            else True
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def id_atlas_code(self) -> Optional[int]:
        id_atlas_code = (
            None
            if "atlas_code" not in self._raw_data["observers"][0]
            else self._raw_data["observers"][0]["atlas_code"]["@id"].split("_")[1]
            if type(self._raw_data["observers"][0]["atlas_code"]) is dict
            else self._raw_data["observers"][0]["atlas_code"]
        )
        return id_atlas_code

    @property  # type: ignore
    @check_raw_data("observers")
    def atlas_code_text(self) -> Optional[str]:
        atlas_code_text = (
            self._raw_data["observers"][0]["atlas_code"]["#text"]
            if "atlas_code" in self._raw_data["observers"][0]
            and "#text" in self._raw_data["observers"][0]["atlas_code"]
            else None
        )
        return atlas_code_text

    @property  # type: ignore
    @check_raw_data("observers")
    def details(self) -> Optional[List[Detail]]:
        details = None
        if "details" in self._raw_data["observers"][0]:
            if "@id" in self._raw_data["observers"][0]["details"][0]["sex"]:
                details = [
                    Detail(
                        int(detail["count"]), detail["sex"]["@id"], detail["age"]["@id"]
                    )
                    for detail in self._raw_data["observers"][0]["details"]
                ]
            else:
                details = [
                    Detail(int(detail["count"]), detail["sex"], detail["age"])
                    for detail in self._raw_data["observers"][0]["details"]
                ]
        return details

    @property  # type: ignore
    @check_raw_data("observers")
    def insert_date(self) -> datetime:
        insert_date = datetime.fromtimestamp(
            int(self._raw_data["observers"][0]["insert_date"]["@timestamp"])
            if type(self._raw_data["observers"][0]["insert_date"]) is dict
            else int(self._raw_data["observers"][0]["insert_date"]),
        ).astimezone()
        return insert_date

    @property  # type: ignore
    @check_raw_data("observers")
    def update_date(self) -> Optional[datetime]:
        update_date = (
            datetime.fromtimestamp(
                int(self._raw_data["observers"][0]["update_date"]["@timestamp"])
                if type(self._raw_data["observers"][0]["update_date"]) is dict
                else int(self._raw_data["observers"][0]["update_date"]),
            ).astimezone()
            if "update_date" in self._raw_data["observers"][0]
            else None
        )
        return update_date

    @property  # type: ignore
    @check_raw_data("place")
    def id_place(self) -> int:
        return int(self._raw_data["place"]["@id"])

    @property  # type: ignore
    @check_raw_data("observers")
    def id_resting_habitat(self) -> Optional[str]:
        if "resting_habitat" in self._raw_data["observers"][0]:
            if type(self._raw_data["observers"][0]["resting_habitat"]) is dict:
                return self._raw_data["observers"][0]["resting_habitat"]["@id"]
            else:
                return self._raw_data["observers"][0]["resting_habitat"]
        return None

    @property  # type: ignore
    @check_raw_data("observers")
    def id_observation_detail(self) -> Optional[str]:
        if "observation_detail" in self._raw_data["observers"][0]:
            if type(self._raw_data["observers"][0]["observation_detail"]) is dict:
                return self._raw_data["observers"][0]["observation_detail"]["@id"]
            else:
                return self._raw_data["observers"][0]["observation_detail"]
        return None

    @property  # type: ignore
    @check_raw_data("species")
    def species(self) -> Species:
        """ Observed Species """
        if self._species is None:
            self._species = Species.create_from(self._raw_data["species"])
        return self._species

    @property  # type: ignore
    @check_raw_data("observers")
    def observer(self) -> Observer:
        """ Observing user """
        if self._observer is None:
            self._observer = Observer.create_from(self._raw_data["observers"][0])
        return self._observer

    @property
    def place(self) -> Place:
        """ Place of the observation """
        if self._place is None:
            self._place = Place.create_from(self._raw_data["place"])
        return self._place

    @property
    def form(self):
        if self._form is None and self.id_form is not None:
            self._form = ornitho.model.form.Form.create_from(self._raw_data["form"])
        return self._form

    @property
    def resting_habitat(self) -> Optional[FieldOption]:
        """ Resting habitat of the observation """
        if self._resting_habitat is None and self.id_resting_habitat:
            self._resting_habitat = FieldOption.get(self.id_resting_habitat)
        return self._resting_habitat

    @property
    def observation_detail(self) -> Optional[FieldOption]:
        """ Observation detail of the observation """
        if self._observation_detail is None and self.id_observation_detail:
            self._observation_detail = FieldOption.get(self.id_observation_detail)
        return self._observation_detail

    @property
    def atlas_code(self) -> Optional[FieldOption]:
        """ Atlas Code of the observation """
        if self._atlas_code is None and self.id_atlas_code:
            self._atlas_code = FieldOption.get(f"3_{self.id_atlas_code}")
        return self._atlas_code

    @classmethod
    def by_observer(
        cls,
        id_observer: int,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        **kwargs: Union[str, int, float, bool],
    ) -> Tuple[List["Observation"], Optional[str]]:
        """ Retrieves a (paged) list of observations from one observer
        :param id_observer: Current data, probably received from the API
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param kwargs: Additional filter values
        :type id_observer: int
        :type pagination_key: Optional[str]
        :type short_version: bool
        :type kwargs: Union[str, int, float, bool]
        :return: Tuple of observations and an optional pagination key
        :rtype: Tuple[List[Observation], Optional[str]]
        """
        observations, pk = cls.list(
            request_all=False,
            pagination_key=pagination_key,
            short_version=short_version,
            id_observer=id_observer,
            **kwargs,
        )
        return observations, pk

    @classmethod
    def by_observer_all(
        cls,
        id_observer: int,
        short_version: bool = False,
        **kwargs: Union[str, int, float, bool],
    ) -> List["Observation"]:
        """Retrieves a list of all observations from one observer
        :param id_observer: Current data, probably received from the API
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param kwargs: Additional filter values
        :type id_observer: int
        :type short_version: bool
        :type kwargs: Union[str, int, float, bool]
        :return: List of observations
        :rtype: List[Observation]
        """
        observations = cls.list_all(
            id_observer=id_observer, short_version=short_version, **kwargs
        )
        return observations

    @classmethod
    def diff(
        cls,
        date: datetime,
        modification_type: ModificationType = None,
        id_taxo_group: int = None,
        only_protocol: Union[str, BaseModel] = None,
        only_form: bool = None,
        retrieve_observations: bool = False,
    ) -> List["Observation"]:
        """Retrieves a list of observations which changed in between now and a given date
        :param date: Date in the past, to which changed observation should be searched
        :param modification_type: Type of modification.
        :param id_taxo_group: Optional taxo group, to which the observerd species must belong to
        :param only_protocol: Return only observation which are part of the given Protocol (Protocol Instance or Name)
        :param only_form: Return only observation which are part of a form
        :param retrieve_observations: Indicates if the observation object should be retrieved. Default: False
        :type date: datetime
        :type modification_type: ModificationType
        :type id_taxo_group: int
        :type only_protocol: Union[str, "Protocol"]
        :type only_form: bool
        :type retrieve_observations: bool
        :return: List of observations
        :rtype: List[Observation]
        """
        url = f"{cls.ENDPOINT}/diff"
        params = dict()
        if modification_type:
            params["modification_type"] = modification_type.value
        if id_taxo_group:
            params["id_taxo_group"] = id_taxo_group
        if only_protocol:
            from ornitho.model.protocol import Protocol

            if isinstance(only_protocol, Protocol):
                params["only_protocol"] = only_protocol.name
            else:
                params["only_protocol"] = only_protocol
        if only_form:
            params["only_form"] = 1

        date = date.replace(microsecond=0)
        if date.tzinfo:
            date = date.astimezone(datetime.now().astimezone().tzinfo).replace(
                tzinfo=None
            )
        params[
            "date"
        ] = (
            date.isoformat()
        )  # Format here, because isoformat is mostly ignored, except here

        changed_observations = cls.request(method="get", url=url, params=params)
        observations = []
        for obs in changed_observations:
            if obs["modification_type"] == "updated":
                modification_type = ModificationType.ONLY_MODIFIED
            else:
                modification_type = ModificationType.ONLY_DELETED
            if (
                retrieve_observations
                and modification_type == ModificationType.ONLY_MODIFIED
            ):
                observations.append(cls.get(int(obs["id_sighting"])))
            else:
                observations.append(
                    cls(
                        id_=int(obs["id_sighting"]), modification_type=modification_type
                    )
                )
        return observations
