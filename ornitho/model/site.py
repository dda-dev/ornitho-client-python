from enum import Enum
from typing import List, Optional

from ornitho.api_requester import APIRequester
from ornitho.model.abstract.base_model import BaseModel, check_raw_data, check_refresh
from ornitho.model.access import Access
from ornitho.model.observation import Observation
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
        self._place: Optional[Place] = None
        self._point_places: Optional[List[Place]] = None
        self._transect_places: Optional[List[Place]] = None
        self._polygon_places: Optional[List[Place]] = None
        self._pdf: Optional[bytes] = None
        self._access: Optional[List[Access]] = None
        self._observations: Optional[List[Observation]] = None

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

    @property
    def place(self) -> Place:
        if self._place is None:
            self._place = Place(id_=self.id_reference_locality)
        return self._place

    @property  # type: ignore
    @check_raw_data("transects")
    def transect_places(self) -> Optional[List[Place]]:
        if self._transect_places is None:
            if "transects" in self._raw_data:
                self._transect_places = [
                    Place.create_from_site(raw_transect)
                    for raw_transect in self._raw_data["transects"]
                ]
        return self._transect_places

    @property  # type: ignore
    @check_raw_data("points")
    def point_places(self) -> Optional[List[Place]]:
        if self._point_places is None:
            if "points" in self._raw_data:
                self._point_places = [
                    Place.create_from_site(raw_transect)
                    for raw_transect in self._raw_data["points"]
                ]
        return self._point_places

    @property  # type: ignore
    @check_raw_data("polygons")
    def polygon_places(self) -> Optional[List[Place]]:
        if self._polygon_places is None:
            if "polygons" in self._raw_data:
                self._polygon_places = [
                    Place.create_from_site(raw_transect)
                    for raw_transect in self._raw_data["polygons"]
                ]
        return self._polygon_places

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
        retries: int = 0,
    ) -> bytes:
        """Request the site pdf map
        :param map_layer: Used map layer
        :param greyscale: Switch for a greyscaled map layer
        :param greyline: Switch for a grey dashed route
        :param alpha: Switch for 50% transparency
        :param boundary: Switch for disable the outer buffer
        :param retries: Indicates how many retries should be performed
        :type map_layer: MapLayer
        :type greyscale: bool
        :type greyline: bool
        :type alpha: bool
        :type boundary: bool
        :type retries: int
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
                method="GET", url=url, params=params, retries=retries
            )
        return response

    @property
    def access(self) -> List[Access]:
        """Get the list of observers with access to this sites
        :return: List of access information
        :rtype: List[Access]
        """
        if self._access is None:
            with APIRequester() as requester:
                url = "protocol/access"
                response, pk = requester.request(
                    method="get",
                    url=url,
                    params={"id_site": self.id_},
                )
                if len(response) > 0:
                    self._access = [
                        Access(
                            id_observer=int(ac["id"]),
                            anonymous=False if ac["anonymous"] == "0" else True,
                            id_access=int(ac["id_access"]),
                        )
                        for ac in response[0][str(self.id_)]["observers"]
                    ]
                else:
                    self._access = []

        return self._access

    @property
    def observations(self) -> List[Observation]:
        """Get the list of observations for this site
        :return: List of observations
        :rtype: List[Observation]
        """
        if self._observations is None:
            self._observations = []
            if self.transect_places:
                for place in self.transect_places:
                    self._observations += Observation.list_all(id_place=place.id_)
            if self.point_places:
                for place in self.point_places:
                    self._observations += Observation.list_all(id_place=place.id_)
            if self.polygon_places:
                for place in self.polygon_places:
                    self._observations += Observation.list_all(id_place=place.id_)

        return self._observations
