from ornitho.model.abstract import ListableModel


class Place(ListableModel):
    ENDPOINT: str = "places"

    @property
    def id_commune(self) -> int:
        """ ID, in which the place is located"""
        return int(self._raw_data["id_commune"])

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def coord_lon(self) -> float:
        return float(self._raw_data["coord_lon"])

    @property
    def coord_lat(self) -> float:
        return float(self._raw_data["coord_lat"])

    @property
    def altitude(self) -> int:
        return int(self._raw_data["altitude"])

    @property
    def id_region(self) -> int:
        return int(self._raw_data["id_region"])

    @property
    def visible(self) -> bool:
        return False if self._raw_data.get("visible") == "0" else True

    @property
    def is_private(self) -> bool:
        return False if self._raw_data.get("is_private") == "0" else True

    @property
    def place_type(self) -> str:
        return self._raw_data["place_type"]

    @property
    def loc_precision(self) -> int:
        return int(self._raw_data["loc_precision"])
