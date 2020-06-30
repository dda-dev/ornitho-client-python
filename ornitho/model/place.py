from typing import Optional

from ornitho.model.abstract import ListableModel
from ornitho.model.abstract.base_model import check_refresh
from ornitho.model.local_admin_unit import LocalAdminUnit


class Place(ListableModel):
    ENDPOINT: str = "places"

    def __init__(self, id_: int) -> None:
        super(Place, self).__init__(id_)
        self._local_admin_unit: Optional[LocalAdminUnit] = None

    @property  # type: ignore
    @check_refresh
    def id_commune(self) -> int:
        """ ID, in which the place is located"""
        return int(self._raw_data["id_commune"])

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def coord_lon(self) -> float:
        return (
            float(self._raw_data["coord_lon"])
            if "coord_lon" in self._raw_data
            else self._raw_data["lon"]
        )

    @property
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

    @property
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

    # Following Properties appear only when requesting an Observation. Mapping to the species API is done here
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

    @classmethod
    def find_closest_place(
        cls, coord_lat: float, coord_lon: float, get_hidden: bool = False, **kwargs
    ) -> "Place":
        return cls.list_all(
            find_closest_place="1",
            coord_lat=coord_lat,
            coord_lon=coord_lon,
            get_hidden=get_hidden,
            **kwargs
        )[0]
