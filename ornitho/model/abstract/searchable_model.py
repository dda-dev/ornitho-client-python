from abc import ABC
from datetime import date, datetime
from typing import List, Optional, Tuple, Type, TypeVar, Union

from ornitho.api_requester import APIRequester
from ornitho.model.abstract import BaseModel

# Create a generic variable that can be 'SearchableModel', or any subclass.
T = TypeVar("T", bound="SearchableModel")


class SearchableModel(BaseModel, ABC):
    """Abstract class for searchable models via POST /ENDPOINT/search"""

    @classmethod
    def search(
        cls: Type[T],
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        **kwargs: Union[str, int, float, bool, date, datetime]
    ) -> Tuple[List[T], Optional[str]]:
        """ Search for instances at Biolovision via POST search
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :type short_version: bool
        :param kwargs: Search values
        :type kwargs: Union[str, int, float, bool]
        :type body: Dict[str, Any]s
        :return: Tuple of instances and pagination key
        :rtype: Tuple[List[T], Optional[str]]
        """
        with APIRequester() as requester:
            url = "%s/search" % cls.ENDPOINT
            response, pk = requester.request(
                method="post",
                url=url,
                request_all=request_all,
                pagination_key=pagination_key,
                short_version=short_version,
                body=kwargs,
            )
            model_list: List[T] = []
            for ele in response:
                obj = cls.create_from_ornitho_json(ele)
                model_list.append(obj)
        return model_list, pk

    @classmethod
    def search_all(
        cls: Type[T],
        short_version: bool = False,
        **kwargs: Union[str, int, float, bool, date, datetime]
    ) -> List[T]:
        """Search for instances at Biolovision via POST search
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param kwargs: Search values
        :type short_version: bool
        :type kwargs: Union[str, int, float, bool]
        :return: List of instances
        :rtype: List[T]
        """
        object_list, pk = cls.search(
            request_all=True, pagination_key=None, short_version=short_version, **kwargs
        )
        return object_list
