from typing import List, Optional, Union

from ornitho import APIException
from ornitho.api_requester import APIRequester
from ornitho.model.abstract import ListableModel
from ornitho.model.field_option import FieldOption


class Field(ListableModel):
    ENDPOINT: str = "fields"

    def __init__(self, id_: int) -> None:
        """Form constructor
        :param id_: ID, which is used to get the form from Biolovison
        :type id_: int
        """
        super(Field, self).__init__(id_)
        self._options: Optional[List[FieldOption]] = None

    @classmethod
    def get(cls, id_: Union[int, str], short_version: bool = False) -> "Field":
        """Retrieve Object from Biolovision with given ID
        :param id_: Unique identifier
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :type id_: Union[int, str]
        :type short_version: bool
        :return: Instance, retrieved from Biolovision with given ID
        :rtype: Field
        """
        fields = cls.list_all(short_version=short_version)
        for field in fields:
            if field.id_ == id_:
                return field
        raise APIException(f"Can't find field with ID {id_}")

    def refresh(self, short_version: bool = False) -> "Field":
        raise NotImplementedError

    @property
    def group(self) -> str:
        return self._raw_data["group"]

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def text(self) -> Optional[str]:
        return self._raw_data["text"] if "text" in self._raw_data else None

    @property
    def default(self) -> int:
        return int(self._raw_data["default"])

    @property
    def mandatory(self) -> bool:
        return False if self._raw_data.get("mandatory") == "0" else True

    @property
    def empty_choice(self) -> bool:
        return False if self._raw_data.get("empty_choice") == "0" else True

    @property
    def options(self) -> List[FieldOption]:
        if self._options is None:
            with APIRequester() as requester:
                url = f"fields/{self.id_}"
                response, pagination_key = requester.request(method="GET", url=url)
                self._options = [
                    FieldOption.create_from_ornitho_json(option) for option in response
                ]
        return self._options
