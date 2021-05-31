from ornitho.model.abstract import ListableModel
from ornitho.model.abstract.base_model import check_refresh


class TerritorialUnit(ListableModel):
    ENDPOINT: str = "territorial_units"

    @property  # type: ignore
    @check_refresh
    def id_country(self) -> int:
        return int(self._raw_data["id_country"])

    @property  # type: ignore
    @check_refresh
    def name(self) -> str:
        return self._raw_data["name"]

    @property  # type: ignore
    @check_refresh
    def short_name(self) -> str:
        return self._raw_data["short_name"]
