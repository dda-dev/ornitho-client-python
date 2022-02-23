from abc import ABC
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

from ornitho.api_exception import ObjectNotFoundException
from ornitho.api_requester import APIRequester

# Create a generic variable that can be 'BaseModel', or any subclass.
T = TypeVar("T", bound="BaseModel")


class BaseModel(ABC):
    """Abstract base class for all models"""

    ENDPOINT: str

    def __init__(self, id_: Union[int, str] = None):
        """Base model constructor
        :param id_: Unique identifier
        :type id_: Union[int, str]
        """
        super(BaseModel, self).__init__()
        self._id: Optional[Union[int, str]] = id_
        self._raw_data: Dict[str, Any] = dict()
        self._previous: Dict[str, Any] = dict()
        self._refreshed: bool = False

    @property
    def id_(self) -> Optional[Union[int, str]]:
        """Unique identifier"""
        if self._id is None:
            if "id" in self._raw_data:
                self._id = self._raw_data["id"]
            elif "@id" in self._raw_data:
                self._id = self._raw_data["@id"]
        return self._id

    @classmethod
    def get(
        cls: Type[T],
        id_: Union[int, str],
        short_version: bool = False,
    ) -> T:
        """Retrieve Object from Biolovision with given ID
        :param id_: Unique identifier
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :type id_: Union[int, str]
        :type short_version: bool
        :return: Instance, retrieved from Biolovision with given ID
        :rtype: T
        """
        instance = cls(id_)
        instance.refresh(short_version=short_version)
        return instance

    @staticmethod
    def request(
        method: str,
        url: str,
        params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
        short_version: bool = False,
        retries: int = 0,
    ) -> List[Any]:
        """Send request to Biolovision and returns response
        :param method: HTTP Method (e.g. 'GET', 'POST', ...)
        :param url: Url to request
        :param params: Additional URL parameters.
        :param body: Request body
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param retries: Indicates how many retries should be performed
        :type method: str
        :type url: str
        :type params: Dict[str, Any]
        :type body: Dict[str, Any]
        :type short_version: bool
        :type retries: int
        :return: Response map from Biolovision
        :rtype: List[Any]
        """
        with APIRequester() as requester:
            response, pagination_key = requester.request(
                method=method,
                url=url,
                params=params,
                body=body,
                short_version=short_version,
                retries=retries,
            )
        # noinspection PyTypeChecker
        return response

    @classmethod
    def create_from_ornitho_json(cls: Type[T], data: Dict[str, Any]) -> T:
        identifier: Union[int, str]
        if "@id" in data:
            identifier = int(data["@id"]) if data["@id"].isdigit() else data["@id"]
        else:
            identifier = int(data["id"]) if data["id"].isdigit() else data["id"]
        obj = cls(identifier)
        obj._raw_data = data
        return obj

    def refresh(self: T, short_version: bool = False, retries: int = 0) -> T:
        """Refresh local model
        Call the api and refresh fields from response
        :return: Refreshed Object
        :rtype: T
        :raise ObjectNotFoundException: No or more than one objects retrieved
        """
        data = self.request(
            method="GET",
            url=self.instance_url(),
            short_version=short_version,
            retries=retries,
        )
        if len(data) != 1:
            raise ObjectNotFoundException(
                f"Get {len(data)} objects for {self.instance_url()}"
            )
        self._previous = self._raw_data
        self._raw_data = data[0]
        self._refreshed = True
        return self

    def instance_url(self) -> str:
        """Returns url for this instance
        :return: Instance's url
        :rtype: str
        """
        return f"{self.ENDPOINT}/{self.id_}"

    def raw_data_trim_field_ids(self) -> Dict[str, Any]:
        """Returns raw data with removed field id from field options ('2_3' -> '3').
        Only need to be reimplemented by models that use fields and are createable/updateable.
        :return: Raw data dict, with trimmed field options
        :rtype: Dict[str, Any]
        """
        return self._raw_data


def check_refresh(func):
    def wrapper(self: T):
        if func.__name__ not in self._raw_data and not self._refreshed:
            self.refresh()
        return func(self)

    return wrapper


def check_raw_data(key):
    def decorator(func):
        def wrapper(self: T):
            if key not in self._raw_data and not self._refreshed:
                if self._id is not None:
                    self.refresh()
            return func(self)

        return wrapper

    return decorator
