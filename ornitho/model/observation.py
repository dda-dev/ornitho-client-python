from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from ornitho.model.abstract import BaseModel, ListableModel, SearchableModel
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

    def __init__(self, id_: int) -> None:
        """ Observation constructor
        :param id_: ID, which is used to get the observation from Biolovison
        :type id_: int
        """
        super(Observation, self).__init__(id_)
        self._species: Optional[Species] = None
        self._observer: Optional[Observer] = None
        self._place: Optional[Place] = None

    @classmethod
    def create_from(cls, data: Dict[str, Any]) -> "BaseModel":
        identifier: int = int(data["observers"][0]["id_sighting"])
        obj = cls(identifier)
        obj._raw_data = data
        return obj

    @property
    def id_observer(self) -> int:
        return int(self._raw_data["observers"][0]["@id"])

    @property
    def traid(self) -> int:
        return int(self._raw_data["observers"][0]["traid"])

    @property
    def timing(self) -> datetime:
        timing = datetime.fromtimestamp(
            int(self._raw_data["observers"][0].get("timing")["@timestamp"]),
            datetime.now().astimezone().tzinfo,
        )
        return timing

    @property
    def coord_lat(self) -> float:
        return float(self._raw_data["observers"][0]["coord_lat"])

    @property
    def coord_lon(self) -> float:
        return float(self._raw_data["observers"][0]["coord_lon"])

    @property
    def altitude(self) -> int:
        return int(self._raw_data["observers"][0]["altitude"])

    @property
    def id_form(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["id_form"])
            if "id_form" in self._raw_data["observers"][0]
            else None
        )

    @property
    def precision(self) -> str:
        return self._raw_data["observers"][0]["precision"]

    @property
    def id_species(self) -> int:
        return int(self._raw_data["species"]["@id"])

    @property
    def count(self) -> int:
        return int(self._raw_data["observers"][0]["count"])

    @property
    def flight_number(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["flight_number"])
            if "flight_number" in self._raw_data["observers"][0]
            else None
        )

    @property
    def atlas_code(self) -> Optional[int]:
        atlas_code = (
            None
            if "atlas_code" not in self._raw_data["observers"][0]
            else self._raw_data["observers"][0]["atlas_code"]["@id"]
            if type(self._raw_data["observers"][0]["atlas_code"]) is dict
            else self._raw_data["observers"][0]["atlas_code"]
        )
        return atlas_code

    @property
    def insert_date(self) -> datetime:
        insert_date = datetime.fromtimestamp(
            int(self._raw_data["observers"][0]["insert_date"]["@timestamp"])
            if type(self._raw_data["observers"][0]["insert_date"]) is dict
            else int(self._raw_data["observers"][0]["insert_date"]),
            datetime.now().astimezone().tzinfo,
        )
        return insert_date

    @property
    def update_date(self) -> Optional[datetime]:
        update_date = (
            datetime.fromtimestamp(
                int(self._raw_data["observers"][0]["update_date"]["@timestamp"])
                if type(self._raw_data["observers"][0]["update_date"]) is dict
                else int(self._raw_data["observers"][0]["update_date"]),
                datetime.now().astimezone().tzinfo,
            )
            if "update_date" in self._raw_data["observers"][0]
            else None
        )
        return update_date

    @property
    def id_place(self) -> int:
        return int(self._raw_data["place"]["@id"])

    @property
    def species(self) -> Species:
        """ Observed Species """
        if self._species is None:
            self._species = Species.get(self.id_species)
        return self._species

    @property
    def observer(self) -> Observer:
        """ Observing user """
        if self._observer is None:
            self._observer = Observer.get(self.id_observer)
        return self._observer

    @property
    def place(self) -> Place:
        """ Place of the observation """
        if self._place is None:
            self._place = Place.get(self.id_place)
        return self._place

    @classmethod
    def by_observer(
        cls,
        id_observer: int,
        pagination_key: Optional[str] = None,
        **kwargs: Union[str, int, float, bool],
    ) -> Tuple[List[BaseModel], Optional[str]]:
        """ Retrieves a (paged) list of observations from one observer
        :param id_observer: Current data, probably received from the API
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param kwargs: Additional filter values
        :type id_observer: int
        :type pagination_key: Optional[str]
        :type kwargs: Union[str, int, float, bool]
        :return: Tuple of observations and an optional pagination key
        :rtype: Tuple[List[BaseModel], Optional[str]]
        """
        observations, pk = cls.list(
            request_all=False,
            pagination_key=pagination_key,
            id_observer=id_observer,
            **kwargs,
        )
        return observations, pk

    @classmethod
    def by_observer_all(
        cls, id_observer: int, **kwargs: Union[str, int, float, bool]
    ) -> List[BaseModel]:
        """Retrieves a list of all observations from one observer
        :param id_observer: Current data, probably received from the API
        :param kwargs: Additional filter values
        :type id_observer: int
        :type kwargs: Union[str, int, float, bool]
        :return: List of observations
        :rtype: List[BaseModel]
        """
        observations = cls.list_all(id_observer=id_observer, **kwargs)
        return observations

    @classmethod
    def diff(
        cls,
        date: datetime,
        modification_type: ModificationType = None,
        id_taxo_group: int = None,
        only_form: bool = None,
        retrieve_observations: bool = False,
    ) -> List[BaseModel]:
        """Retrieves a list of observations which changed in between now and a given date
        :param date: Date in the past, to which changed observation should be searched
        :param modification_type: Type of modification.
        :param id_taxo_group: Optional taxo group, to which the observerd species must belong to
        :param only_form: Return only observation which are part of a form
        :param retrieve_observations: Indicates if the observation object should be retrieved. Default: False
        :type date: datetime
        :type modification_type: ModificationType
        :type id_taxo_group: int
        :type only_form: bool
        :type retrieve_observations: bool
        :return: List of observations
        :rtype: List[BaseModel]
        """
        url = f"{cls.ENDPOINT}/diff"
        params = dict()
        if modification_type:
            params["modification_type"] = modification_type.value
        if id_taxo_group:
            params["id_taxo_group"] = id_taxo_group
        if only_form:
            params["only_form"] = 1

        # Converte timezone to local timezone and make it naive, since ornitho can't handle timezone in parameters
        if date.tzinfo:
            params["date"] = date.astimezone(
                datetime.now().astimezone().tzinfo
            ).replace(tzinfo=None)
        else:
            params["date"] = date

        changed_observations = cls.request(method="get", url=url, params=params)
        observations = []
        for obs in changed_observations:
            if retrieve_observations:
                observations.append(cls.get(int(obs["id_sighting"])))
            else:
                observations.append(cls(id_=int(obs["id_sighting"])))
        return observations
