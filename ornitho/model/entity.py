from ornitho.model.abstract import ListableModel


class Entity(ListableModel):
    ENDPOINT: str = "entities"

    @property
    def short_name(self) -> str:
        return self._raw_data["short_name"]

    @property
    def full_name_german(self) -> str:
        return self._raw_data["full_name_german"]

    @property
    def address(self) -> str:
        return self._raw_data["address"]

    @property
    def url(self) -> str:
        return self._raw_data["url"]

    @property
    def description_german(self) -> str:
        return self._raw_data["description_german"]
