from abc import ABC
from datetime import date
from typing import List, Optional, Tuple, Type, TypeVar, Union

from ornitho.api_requester import APIRequester
from ornitho.model.abstract import BaseModel

# Create a generic variable that can be 'ListableModel', or any subclass.
T = TypeVar("T", bound="ListableModel")


class ListableModel(BaseModel, ABC):
    """Abstract class for listable models via GET /ENDPOINT"""

    @classmethod
    def list(
        cls: Type[T],
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        **kwargs: Union[str, int, float, bool, date]
    ) -> Tuple[List[T], Optional[str]]:
        """ Retrieves a (paged) list of instances from Biolovison
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param kwargs: Additional filter values
        :type request_all: bool
        :type pagination_key: Optional[str]
        :type kwargs: Union[str, int, float, bool, date]
        :return: Tuple of instances and pagination key
        :rtype: Tuple[List[T], Optional[str]]
        """
        with APIRequester() as requester:
            url = cls.ENDPOINT
            response, pk = requester.request(
                method="get",
                url=url,
                request_all=request_all,
                pagination_key=pagination_key,
                params=kwargs,
            )
            model_list: List[T] = []
            for ele in response:
                obj = cls.create_from(ele)
                model_list.append(obj)
        return model_list, pk

    @classmethod
    def list_all(cls: Type[T], **kwargs: Union[str, int, float, bool, date]) -> List[T]:
        """Retrieves a list of all instances from Biolovison
        :param kwargs: Additional filter values
        :type kwargs: Union[str, int, float, bool, date]
        :return: List of instances
        :rtype: List[T]
        """
        object_list, pk = cls.list(True, None, **kwargs)
        return object_list
