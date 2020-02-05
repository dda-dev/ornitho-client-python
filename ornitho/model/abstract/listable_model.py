from abc import ABC
from typing import List, Optional, Tuple, Union

from ornitho.api_requester import APIRequester
from ornitho.model.abstract import BaseModel


class ListableModel(BaseModel, ABC):
    """Abstract class for listable models via GET /ENDPOINT"""

    @classmethod
    def list(
        cls,
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        **kwargs: Union[str, int, float, bool]
    ) -> Tuple[List["BaseModel"], Optional[str]]:
        """ Retrieves a (paged) list of instances from Biolovison
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param kwargs: Additional filter values
        :type request_all: bool
        :type pagination_key: Optional[str]
        :type kwargs: Union[str, int, float, bool]
        :return: Tuple of instances and pagination key
        :rtype: Tuple[List[BaseModel], Optional[str]]
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
            model_list: List[BaseModel] = []
            for ele in response:
                obj = cls.create_from(ele)
                model_list.append(obj)
        return model_list, pk

    @classmethod
    def list_all(cls, **kwargs: Union[str, int, float, bool]) -> List["BaseModel"]:
        """Retrieves a list of all instances from Biolovison
        :param kwargs: Additional filter values
        :type kwargs: Union[str, int, float, bool]
        :return: List of instances
        :rtype: List[BaseModel]
        """
        object_list, pk = cls.list(True, None, **kwargs)
        return object_list
