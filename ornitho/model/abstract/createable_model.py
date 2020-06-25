from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar

from ornitho.model.abstract import BaseModel

# Create a generic variable that can be 'CreateableModel', or any subclass.
T = TypeVar("T", bound="CreateableModel")


class CreateableModel(BaseModel, ABC):
    """Abstract class for createable models via POST /ENDPOINT"""

    @classmethod
    def create_in_ornitho(cls: Type[T], data: Dict[str, Any]) -> int:
        """ Create an instance on ornitho
        :param data: Data
        :type data: T
        :return:  Ornitho ID of the created object
        :rtype: T
        """
        url = cls.ENDPOINT
        body = {"data": data}
        response = cls.request(method="post", url=url, body=body)
        return response[0]["id"][0]

    @classmethod
    @abstractmethod
    def create(cls: Type[T], **kwargs) -> T:
        """ Create an instance on ornitho, respecting the specific model characteristics

        This method should implement an easy to use way for creating new instances on ornitho,
        respecting the specific model characteristics. I should use the general create_in_ornitho method.
        """
