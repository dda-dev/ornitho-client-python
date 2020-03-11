from typing import List, Optional, Union

from ornitho import APIException
from ornitho.api_requester import APIRequester
from ornitho.model.abstract import ListableModel
from ornitho.model.field_option import FieldOption


class Field(ListableModel):
    ENDPOINT: str = "fields"

    def __init__(self, id_: int) -> None:
        """ Form constructor
        :param id_: ID, which is used to get the form from Biolovison
        :type id_: int
        """
        super(Field, self).__init__(id_)
        self._options: Optional[List[FieldOption]] = None

    @classmethod
    def get(cls, id_: Union[int, str]) -> "Field":
        """ Retrieve Object from Biolovision with given ID
        :param id_: Unique identifier
        :type id_: Union[int, str]
        :return: Instance, retrieved from Biolovision with given ID
        :rtype: Field
        """
        fields = cls.list_all(short_version=False)
        for field in fields:
            if field.id_ == id_:
                return field
        raise APIException(f"Can't find field with ID {id_}")

    def refresh(self) -> "Field":
        raise NotImplementedError

    @property
    def group(self) -> str:
        return self._raw_data["group"]

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def text(self) -> str:
        return self._raw_data["text"]

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
                response, pagination_key = requester.request(
                    method="GET", url=url, params={"short_version": False}
                )
                self._options = [FieldOption.create_from(option) for option in response]
        return self._options
