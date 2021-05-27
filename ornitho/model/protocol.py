from datetime import date, datetime
from typing import List, Optional, Tuple, Union

from ornitho.model.abstract import ListableModel
from ornitho.model.entity import Entity
from ornitho.model.observation import Observation
from ornitho.model.site import Site


class Protocol(ListableModel):
    ENDPOINT: str = "protocol"

    def __init__(self, id_: int) -> None:
        """Protocol constructor
        :param id_: ID, which is used to get the protocol from Biolovison
        :type id_: int
        """
        super(Protocol, self).__init__(id_)
        self._entity: Optional[Entity] = None
        self._sites: Optional[List[Site]] = None

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def nbre_points_min(self) -> int:
        return int(self._raw_data["nbre_points_min"])

    @property
    def nbre_points_max(self) -> int:
        return int(self._raw_data["nbre_points_max"])

    @property
    def time_point(self) -> Optional[int]:
        return (
            int(self._raw_data["time_point"]) if self._raw_data["time_point"] else None
        )

    @property
    def taxo_point(self) -> int:
        return int(self._raw_data["taxo_point"])

    @property
    def additional_taxo_point(self) -> Optional[int]:
        return (
            int(self._raw_data["additional_taxo_point"])
            if self._raw_data["additional_taxo_point"]
            else None
        )

    @property
    def nbre_transects_min(self) -> int:
        return int(self._raw_data["nbre_transects_min"])

    @property
    def nbre_transects_max(self) -> int:
        return int(self._raw_data["nbre_transects_max"])

    @property
    def time_transect(self) -> Optional[int]:
        return (
            int(self._raw_data["time_transect"])
            if self._raw_data["time_transect"]
            else None
        )

    @property
    def taxo_transect(self) -> int:
        return int(self._raw_data["taxo_transect"])

    @property
    def additional_taxo_transect(self) -> Optional[int]:
        return (
            int(self._raw_data["additional_taxo_transect"])
            if self._raw_data["additional_taxo_transect"]
            else None
        )

    @property
    def nbre_polygones_min(self) -> int:
        return int(self._raw_data["nbre_polygones_min"])

    @property
    def nbre_polygones_max(self) -> int:
        return int(self._raw_data["nbre_polygones_max"])

    @property
    def time_polygone(self) -> Optional[int]:
        return (
            int(self._raw_data["time_polygone"])
            if self._raw_data["time_polygone"]
            else None
        )

    @property
    def taxo_poly(self) -> int:
        return int(self._raw_data["taxo_poly"])

    @property
    def additional_taxo_poly(self) -> Optional[int]:
        return (
            int(self._raw_data["additional_taxo_poly"])
            if self._raw_data["additional_taxo_poly"]
            else None
        )

    @property
    def project_id(self) -> Optional[int]:
        return (
            int(self._raw_data["project_id"]) if self._raw_data["project_id"] else None
        )

    @property
    def id_entity(self) -> int:
        return int(self._raw_data["id_entity"])

    @property
    def nbre_bounding_box_max(self) -> int:
        return int(self._raw_data["nbre_bounding_box_max"])

    @property
    def nbre_passage(self) -> Optional[int]:
        return (
            int(self._raw_data["nbre_passage"])
            if self._raw_data["nbre_passage"]
            else None
        )

    @property
    def auto_hidden(self) -> int:
        return False if self._raw_data["auto_hidden"] == "0" else True

    @property
    def only_admin_create(self) -> int:
        return False if self._raw_data["only_admin_create"] == "0" else True

    @property
    def start_month(self) -> int:
        return int(self._raw_data["start_month"])

    @property
    def default_atlas_code(self) -> Optional[int]:
        return (
            int(self._raw_data["default_atlas_code"])
            if self._raw_data["default_atlas_code"]
            else None
        )

    @property
    def default_count(self) -> Optional[int]:
        return (
            int(self._raw_data["default_count"])
            if self._raw_data["default_count"]
            else None
        )

    @property
    def entity(self) -> Entity:
        """ Entity of the protocol """
        if self._entity is None:
            self._entity = Entity.get(self.id_entity)
        return self._entity

    @property
    def sites(self) -> List[Site]:
        """Get sites linked to the protocol
        :return: List of sites
        :rtype: List[Site]
        """
        if not self._sites:
            url = f"{self.ENDPOINT}/sites"
            params = {"id_protocol": self.id_}

            sites_object = self.request(method="get", url=url, params=params)[0]
            self._sites = [Site(id_=site_id) for site_id in sites_object.keys()]
        return self._sites

    def get_observations(
        self,
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        **kwargs: Union[str, int, float, bool, date, datetime],
    ) -> Tuple[List[Observation], Optional[str]]:
        """Get observations linked to the protocol
        The same search parameters can be used as for the observations (except 'only_protocol' which is automatically set)
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param kwargs: Additional filter values
        :type request_all: Optional[bool]
        :type pagination_key: Optional[str]
        :type short_version: bool
        :type kwargs: Union[str, int, float, bool, datetime]
        :return: List of observations
        :rtype: Tuple[List[Observation], Optional[str]]
        """
        if "period_choice" not in kwargs.keys():
            kwargs["period_choice"] = "all"
        return Observation.search(
            request_all=request_all,
            pagination_key=pagination_key,
            short_version=short_version,
            only_protocol=self.name,
            **kwargs,
        )

    def get_all_observations(
        self,
        short_version: bool = False,
        **kwargs: Union[str, int, float, bool, date, datetime],
    ) -> List[Observation]:
        """Get observations linked to the protocol
        The same search parameters can be used as for the observations (except 'only_protocol' which is automatically set)
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param kwargs: Additional filter values
        :type short_version: bool
        :type kwargs: Union[str, int, float, bool, datetime]
        :return: List of observations
        :rtype: List[Observation]
        """
        return self.get_observations(
            request_all=True, pagination_key=None, short_version=short_version, **kwargs
        )[0]
