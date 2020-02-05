from abc import ABC
from typing import Any, Dict, List
from urllib.parse import quote_plus

from ornitho.api_requester import APIRequester


class BaseModel(ABC):
    """Abstract base class for all models"""

    ENDPOINT: str

    def __init__(self, id_: int):
        """ Base model constructor
        :param id_: Unique identifier
        :type id_: int
        """
        super(BaseModel, self).__init__()
        self._id: int = id_
        self._raw_data: Dict[str, Any] = dict()
        self._previous: Dict[str, Any] = dict()

    @property
    def id_(self) -> int:
        """ ID, in which the place is located"""
        return self._id

    @classmethod
    def retrieve(cls, id_: int):
        """ Retrieve Object from Biolovision with given ID
        :param id_: Unique identifier
        :type id_: int
        :return: Instance, retrieved from Biolovision with given ID
        :rtype: BaseModel
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
        :rtype: Dict[str, str]
        """
        with APIRequester() as requester:
            response, pagination_key = requester.request(
                method=method, url=url, params=params, body=body
            )
        # noinspection PyTypeChecker
        return response

    @classmethod
    def create_from(cls, data: Dict[str, Any]) -> "BaseModel":
        identifier: int = int(data["id"])
        obj = cls(identifier)
        obj._raw_data = data
        return obj

    def refresh(self) -> "BaseModel":
        """ Refresh local model
        Call the api and refresh fields from response
        :return: Refreshed Object
        :rtype: BaseModel
        """
        data = self.request(method="get", url=self.instance_url())[0]
        self._previous = self._raw_data
        self._raw_data = data
        return self

    def instance_url(self) -> str:
        """ Returns url for this instance
        :return: Instance's url
        :rtype: str
        """
        base = self.ENDPOINT
        extn = quote_plus(self._id.__str__())
        return f"{base}/{extn}"
