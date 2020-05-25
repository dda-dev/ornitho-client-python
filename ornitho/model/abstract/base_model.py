from abc import ABC
from typing import Any, Dict, List, Type, TypeVar, Union

from ornitho.api_exception import APIException
from ornitho.api_requester import APIRequester

# Create a generic variable that can be 'BaseModel', or any subclass.
T = TypeVar("T", bound="BaseModel")


class BaseModel(ABC):
    """Abstract base class for all models"""

    ENDPOINT: str

    def __init__(self, id_: Union[int, str]):
        """ Base model constructor
        :param id_: Unique identifier
        :type id_: Union[int, str]
        """
        super(BaseModel, self).__init__()
        self._id: Union[int, str] = id_
        self._raw_data: Dict[str, Any] = dict()
        self._previous: Dict[str, Any] = dict()

    @property
    def id_(self) -> Union[int, str]:
        """ Unique identifier """
        return self._id

    @classmethod
    def get(cls: Type[T], id_: Union[int, str]) -> T:
        """ Retrieve Object from Biolovision with given ID
        :param id_: Unique identifier
        :type id_: Union[int, str]
        :return: Instance, retrieved from Biolovision with given ID
        :rtype: T
        """
        instance = cls(id_)
        instance.refresh()
        return instance

    @staticmethod
    def request(
        method: str,
        url: str,
        params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
    ) -> List[Any]:
        """ Send request to Biolovision and returns response
        :param method: HTTP Method (e.g. 'GET', 'POST', ...)
        :param url: Url to request
        :param params: Additional URL parameters.
        :param body: Request body
        :type method: str
        :type url: str
        :type params: Dict[str, Any]
        :type body: Dict[str, Any]
        :return: Response map from Biolovision
        :rtype: List[Any]
        """
        with APIRequester() as requester:
            response, pagination_key = requester.request(
                method=method, url=url, params=params, body=body
            )
        # noinspection PyTypeChecker
        return response

    @classmethod
    def create_from(cls: Type[T], data: Dict[str, Any]) -> T:
        identifier: Union[int, str]
        if "@id" in data:
            identifier = int(data["@id"]) if data["@id"].isdigit() else data["@id"]
        else:
            identifier = int(data["id"]) if data["id"].isdigit() else data["id"]
        obj = cls(identifier)
        obj._raw_data = data
        return obj

    def refresh(self: T) -> T:
        """ Refresh local model
        Call the api and refresh fields from response
        :return: Refreshed Object
        :rtype: T
        :raise APIException: No or more than one objects retrieved
        """
        data = self.request(method="GET", url=self.instance_url())
        if len(data) != 1:
            raise APIException(f"Get {len(data)} objects for {self.instance_url()}")
        self._previous = self._raw_data
        self._raw_data = data[0]
        return self

    def instance_url(self) -> str:
        """ Returns url for this instance
        :return: Instance's url
        :rtype: str
        """
        return f"{self.ENDPOINT}/{self.id_}"


def check_refresh(func):
    def wrapper(self: T):
        if func.__name__ not in self._raw_data:
            self.refresh()
        return func(self)

    return wrapper
