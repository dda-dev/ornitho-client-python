from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from ornitho.model.abstract import ListableModel
from ornitho.model.abstract.base_model import BaseModel, check_refresh
from ornitho.model.local_admin_unit import LocalAdminUnit
from ornitho.model.modification_type import ModificationType
from ornitho.model.observer import Observer


class Place(ListableModel):
    ENDPOINT: str = "places"

    def __init__(self, id_: int, modification_type: ModificationType = None) -> None:
        super(Place, self).__init__(id_)
        self.modification_type = modification_type
        self._local_admin_unit: Optional[LocalAdminUnit] = None
        self._centroid: Optional[str] = None
        self._order: Optional[int] = None
        self._wkt: Optional[str] = None

    @property  # type: ignore
    @check_refresh
    def id_commune(self) -> int:
        """ ID, in which the place is located"""
        return int(self._raw_data["id_commune"])

    @property  # type: ignore
    @check_refresh
    def name(self) -> str:
        return self._raw_data["name"]

    @property  # type: ignore
    @check_refresh
    def coord_lon(self) -> float:
        return (
            float(self._raw_data["coord_lon"])
            if "coord_lon" in self._raw_data
            else self._raw_data["lon"]
        )

    @property  # type: ignore
    @check_refresh
    def coord_lat(self) -> float:
        return (
            float(self._raw_data["coord_lat"])
            if "coord_lat" in self._raw_data
            else self._raw_data["lat"]
        )

    @property  # type: ignore
    @check_refresh
    def altitude(self) -> int:
        return int(self._raw_data["altitude"])

    @property  # type: ignore
    @check_refresh
    def id_region(self) -> int:
        return int(self._raw_data["id_region"])

    @property  # type: ignore
    @check_refresh
    def visible(self) -> bool:
        return False if self._raw_data.get("visible") == "0" else True

    @property  # type: ignore
    @check_refresh
    def is_private(self) -> bool:
        return False if self._raw_data.get("is_private") == "0" else True

    @property  # type: ignore
    @check_refresh
    def place_type(self) -> str:
        return self._raw_data["place_type"]

    @property  # type: ignore
    @check_refresh
    def loc_precision(self) -> int:
        return int(self._raw_data["loc_precision"])

    @property
    def local_admin_unit(self) -> LocalAdminUnit:
        if self._local_admin_unit is None:
            self._local_admin_unit = LocalAdminUnit.get(self.id_commune)
        return self._local_admin_unit

    @property
    def commune(self) -> LocalAdminUnit:
        return self.local_admin_unit

    @property  # type: ignore
    @check_refresh
    def created_by(self) -> Observer:
        return Observer(id_=int(self._raw_data["created_by"]))

    @property  # type: ignore
    @check_refresh
    def created_date(self) -> datetime:
        created_date = datetime.fromtimestamp(
            int(self._raw_data["created_date"]["@timestamp"])
            if type(self._raw_data["created_date"]) is dict
            else int(self._raw_data["created_date"]),
        ).astimezone()
        return created_date

    @property  # type: ignore
    @check_refresh
    def last_updated_by(self) -> Observer:
        return Observer(id_=int(self._raw_data["last_updated_by"]))

    @property  # type: ignore
    @check_refresh
    def last_updated_date(self) -> datetime:
        last_updated_date = datetime.fromtimestamp(
            int(self._raw_data["last_updated_date"]["@timestamp"])
            if type(self._raw_data["last_updated_date"]) is dict
            else int(self._raw_data["last_updated_date"]),
        ).astimezone()
        return last_updated_date

    # Following Properties appear only when requesting an Observation
    @property
    def municipality(self) -> str:
        return (
            self._raw_data["municipality"]
            if "municipality" in self._raw_data
            else self.local_admin_unit.name
        )

    @property
    def county(self) -> Optional[str]:
        return self._raw_data["county"] if "county" in self._raw_data else None

    @property
    def country(self) -> Optional[str]:
        return self._raw_data["country"] if "country" in self._raw_data else None

    # Following Properties appear only when requesting a Site
    @property
    def centroid(self) -> Optional[str]:
        return self._centroid

    @property
    def order(self) -> Optional[int]:
        return self._order

    @property
    def wkt(self) -> Optional[str]:
        return self._wkt

    @classmethod
    def find_closest_place(
        cls, coord_lat: float, coord_lon: float, get_hidden: bool = False, **kwargs
    ) -> "Place":
        return cls.list_all(
            find_closest_place="1",
            coord_lat=coord_lat,
            coord_lon=coord_lon,
            get_hidden=get_hidden,
            **kwargs,
        )[0]

    @classmethod
    def create_from_site(cls, data: Dict[str, Any]):
        identifier: int = int(data["id"])
        obj = cls(identifier)
        obj._centroid = data["centroid"] if "centroid" in data else None
        obj._order = data["order"] if "order" in data else None
        obj._wkt = data["wkt"] if "wkt" in data else None
        return obj

    @classmethod
    def diff(
        cls,
        date: datetime,
        modification_type: ModificationType = None,
        only_protocol: Union[str, BaseModel] = None,
        retrieve_places: bool = False,
    ) -> List["Place"]:
        """Retrieves a list of places which changed in between now and a given date
        :param date: Date in the past, to which changed places should be searched
        :param modification_type: Type of modification.
        :param only_protocol: Return only observation which are part of the given Protocol (Protocol Instance or Name)
        :param retrieve_places: Indicates if the place objects should be retrieved. Default: False
        :type date: datetime
        :type modification_type: ModificationType
        :type only_protocol: Union[str, "Protocol"]
        :type retrieve_places: bool
        :return: List of observations
        :rtype: List[Observation]
        """
        url = f"{cls.ENDPOINT}/diff"
        params = dict()
        if modification_type:
            params["modification_type"] = modification_type.value
        if only_protocol:
            from ornitho.model.protocol import Protocol

            if isinstance(only_protocol, Protocol):
                params["only_protocol"] = only_protocol.name
            else:
                params["only_protocol"] = only_protocol.__str__()

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

        changed_places = cls.request(method="get", url=url, params=params)
        places = []
        for place in changed_places:
            if place["modification_type"] == "updated":
                modification_type = ModificationType.ONLY_MODIFIED
            else:
                modification_type = ModificationType.ONLY_DELETED
            if retrieve_places and modification_type == ModificationType.ONLY_MODIFIED:
                places.append(cls.get(int(place["id_place"])))
            else:
                places.append(
                    cls(id_=int(place["id_place"]), modification_type=modification_type)
                )
        return places
