from enum import Enum
from typing import Any, Dict, List, Optional

from ornitho.api_requester import APIRequester
from ornitho.model.abstract import BaseModel


class MapLayer(Enum):
    BKG = "BKG"
    TOPO_PLUS_OPEN = "TOPO_PLUS_OPEN"
    OSM2014 = "OSM2014"
    OSMLIVE = "OSMLIVE"


class Site(BaseModel):
    ENDPOINT_PDF: str = ""

    def __init__(self, id_: int) -> None:
        """ Site constructor
        :param id_: ID, which is used to get the site from Biolovison
        :type id_: int
        """
        super(Site, self).__init__(id_)
        self._pdf: Optional[bytes] = None

    @staticmethod
    def request(
        method: str,
        url: str,
        params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
    ) -> List[Any]:
        raise NotImplementedError

    @property
    def id_universal(self) -> str:
        return self._raw_data["id_universal"]

    @property
    def custom_name(self) -> str:
        return self._raw_data["custom_name"]

    @property
    def reference_locality(self) -> str:
        return self._raw_data["reference_locality"]

    def pdf(
        self, map_layer: MapLayer = None, greyscale: bool = None, alpha: bool = None, boundary: bool = None
    ) -> List[Any]:
        """ Send request to Biolovision and returns the content as a PDF
        :return: Response map from Biolovision
        :rtype: Dict[str, str]
        """
        with APIRequester() as requester:
            url = f"protocol/site_pdf"
            params = {"id": self.id_}
            if map_layer:
                params["map_layer"] = map_layer.value
            if greyscale:
                params["greyscale"] = 1
            if alpha:
                params["alpha"] = 1
            if boundary:
                params["boundary"] = 1
            response, pagination_key = requester.request(
                method="GET", url=url, params=params
            )
        # noinspection PyTypeChecker
        return response
