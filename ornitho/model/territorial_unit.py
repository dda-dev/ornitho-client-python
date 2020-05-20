from ornitho.model.abstract import ListableModel


class TerritorialUnit(ListableModel):
    ENDPOINT: str = "territorial_units"

    @property
    def id_country(self) -> int:
        return int(self._raw_data["id_country"])

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def short_name(self) -> str:
        return self._raw_data["short_name"]
