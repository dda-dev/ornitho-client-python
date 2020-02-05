from abc import ABC
from typing import List, Optional, Tuple, Union

from ornitho.api_requester import APIRequester
from ornitho.model.abstract import BaseModel


class SearchableModel(BaseModel, ABC):
    """Abstract class for searchable models via POST /ENDPOINT/search"""

    @classmethod
    def search(
        cls,
        request_all: Optional[bool] = False,
        pagination_key: Optional[str] = None,
        **kwargs: Union[str, int, float, bool]
    ) -> Tuple[List["BaseModel"], Optional[str]]:
        """ Search for instances at Biolovision via POST search
        If the list is chunked, a pagination key ist returned
        :param request_all: Indicates, if all instances should be retrieved (may result in many API calls)
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param kwargs: Search values
        :type kwargs: Union[str, int, float, bool]
        :type body: Dict[str, Any]s
        :return: Tuple of instances and pagination key
        :rtype: Tuple[List[BaseModel], Optional[str]]
        """
        with APIRequester() as requester:
            url = "%s/search" % cls.ENDPOINT
            response, pk = requester.request(
                method="post",
                url=url,
                request_all=request_all,
                pagination_key=pagination_key,
                body=kwargs,
            )
            model_list: List[BaseModel] = []
            for ele in response:
                obj = cls.create_from(ele)
                model_list.append(obj)
        return model_list, pk

    @classmethod
    def search_all(cls, **kwargs: Union[str, int, float, bool]) -> List["BaseModel"]:
        """Search for instances at Biolovision via POST search
        :param kwargs: Search values
        :type kwargs: Union[str, int, float, bool]
        :return: List of instances
        :rtype: List[BaseModel]
        """
        object_list, pk = cls.search(request_all=True, pagination_key=None, **kwargs)
        return object_list
