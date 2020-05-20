from typing import Optional

import ornitho.model.territorial_unit
from ornitho.model.abstract import ListableModel


class LocalAdminUnit(ListableModel):
    ENDPOINT: str = "local_admin_units"

    def __init__(self, id_: int) -> None:
        super(LocalAdminUnit, self).__init__(id_)
        self._territorial_unit: Optional[
            ornitho.model.territorial_unit.TerritorialUnit
        ] = None

    @property
    def id_canton(self) -> int:
        return int(self._raw_data["id_canton"])

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def insee(self) -> str:
        return self._raw_data["insee"]

    @property
    def coord_lon(self) -> float:
        return float(self._raw_data["coord_lon"])

    @property
    def coord_lat(self) -> float:
        return float(self._raw_data["coord_lat"])

    @property
    def territorial_unit(self):
        if self._territorial_unit is None:
            self._territorial_unit = ornitho.model.territorial_unit.TerritorialUnit.get(
                self.id_canton
            )
        return self._territorial_unit

    @property
    def canton(self):
        return self.territorial_unit
