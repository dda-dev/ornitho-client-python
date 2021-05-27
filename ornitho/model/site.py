from enum import Enum
from typing import List, Optional

from ornitho.api_requester import APIRequester
from ornitho.model.abstract.base_model import BaseModel, check_raw_data, check_refresh
from ornitho.model.observer import Observer
from ornitho.model.place import Place


class MapLayer(Enum):
    BKG = "BKG"
    TOPO_PLUS_OPEN = "TOPO_PLUS_OPEN"
    OSM2014 = "OSM2014"
    OSMLIVE = "OSMLIVE"


class Site(BaseModel):
    ENDPOINT: str = "protocol/sites"

    def __init__(self, id_: int) -> None:
        """Site constructor
        :param id_: ID, which is used to get the site from Biolovison
        :type id_: int
        """
        super(Site, self).__init__(id_)
        self._pdf: Optional[bytes] = None

    @property  # type: ignore
    @check_refresh
    def id_universal(self) -> str:
        return self._raw_data["id_universal"]

    @property  # type: ignore
    @check_refresh
    def custom_name(self) -> str:
        return self._raw_data["custom_name"]

    @property  # type: ignore
    @check_refresh
    def local_name(self) -> Optional[str]:
        return self._raw_data["local_name"] if "local_name" in self._raw_data else None

    @property  # type: ignore
    @check_refresh
    def id_reference_locality(self) -> int:
        return int(self._raw_data["id_reference_locality"])

    @property  # type: ignore
    @check_refresh
    def reference_locality(self) -> str:
        return self._raw_data["reference_locality"]

    @property  # type: ignore
    @check_refresh
    def id_protocol(self) -> int:
        return int(self._raw_data["id_protocol"])

    @property  # type: ignore
    @check_raw_data("transects")
    def transect_places(self) -> Optional[List[Place]]:
        places = None
        if "transects" in self._raw_data:
            places = [
                Place.create_from_site(raw_transect)
                for raw_transect in self._raw_data["transects"]
            ]
        return places

    @property  # type: ignore
    @check_raw_data("points")
    def point_places(self) -> Optional[List[Place]]:
        places = None
        if "points" in self._raw_data:
            places = [
                Place.create_from_site(raw_transect)
                for raw_transect in self._raw_data["points"]
            ]
        return places

    @property  # type: ignore
    @check_raw_data("polygons")
    def polygon_places(self) -> Optional[List[Place]]:
        places = None
        if "polygons" in self._raw_data:
            places = [
                Place.create_from_site(raw_transect)
                for raw_transect in self._raw_data["polygons"]
            ]
        return places

    @property  # type: ignore
    @check_raw_data("boundary_wkt")
    def boundary_wkt(self) -> Optional[str]:
        return (
            self._raw_data["boundary_wkt"] if "boundary_wkt" in self._raw_data else None
        )

    @property  # type: ignore
    @check_refresh
    def observers(self) -> List[Observer]:
        observers = []
        if "observers" in self._raw_data:
            observers = [
                Observer(id_=int(observer_id))
                for observer_id in self._raw_data["observers"]
            ]
        return observers

    def pdf(
        self,
        map_layer: MapLayer = None,
        greyscale: bool = False,
        greyline: bool = False,
        alpha: bool = False,
        boundary: bool = False,
    ) -> bytes:
        """Request the site pdf map
        :param map_layer: Used map layer
        :param greyscale: Switch for a greyscaled map layer
        :param greyline: Switch for a grey dashed route
        :param alpha: Switch for 50% transparency
        :param boundary: Switch for disable the outer buffer
        :type map_layer: MapLayer
        :type greyscale: bool
        :type greyline: bool
        :type alpha: bool
        :type boundary: bool
        :return: PDF as bytes
        :rtype: bytes
        """
        with APIRequester() as requester:
            url = f"{self.instance_url()}.pdf"
            params = {"id": self.id_}
            if map_layer:
                params["map_layer"] = map_layer.value
            if greyscale:
                params["greyscale"] = 1
            if greyline:
                params["greyline"] = 1
            if alpha:
                params["alpha"] = 1
            if boundary:
                params["boundary"] = 1
            response, pagination_key = requester.request(
                method="GET", url=url, params=params
            )
        return response
