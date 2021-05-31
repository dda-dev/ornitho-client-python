from typing import Optional

from ornitho.model.abstract import ListableModel
from ornitho.model.abstract.base_model import check_refresh
from ornitho.model.territorial_unit import TerritorialUnit


class LocalAdminUnit(ListableModel):
    ENDPOINT: str = "local_admin_units"

    def __init__(self, id_: int) -> None:
        super(LocalAdminUnit, self).__init__(id_)
        self._territorial_unit: Optional[TerritorialUnit] = None

    @property  # type: ignore
    @check_refresh
    def id_canton(self) -> int:
        return int(self._raw_data["id_canton"])

    @property  # type: ignore
    @check_refresh
    def name(self) -> str:
        return self._raw_data["name"]

    @property  # type: ignore
    @check_refresh
    def insee(self) -> str:
        return self._raw_data["insee"]

    @property  # type: ignore
    @check_refresh
    def coord_lon(self) -> float:
        return float(self._raw_data["coord_lon"])

    @property  # type: ignore
    @check_refresh
    def coord_lat(self) -> float:
        return float(self._raw_data["coord_lat"])

    @property
    def territorial_unit(self) -> TerritorialUnit:
        if self._territorial_unit is None:
            self._territorial_unit = TerritorialUnit(id_=self.id_canton)
        return self._territorial_unit

    @property
    def canton(self):
        return self.territorial_unit
