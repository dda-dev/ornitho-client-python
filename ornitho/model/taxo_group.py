from ornitho.model.abstract import ListableModel


class TaxonomicGroup(ListableModel):
    ENDPOINT: str = "taxo_groups"

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def latin_name(self) -> str:
        return self._raw_data["latin_name"]

    @property
    def name_constant(self) -> str:
        return self._raw_data["name_constant"]

    @property
    def access_mode(self) -> str:
        return self._raw_data["access_mode"]
