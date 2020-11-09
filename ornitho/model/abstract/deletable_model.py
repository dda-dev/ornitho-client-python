from abc import ABC
from typing import Optional, TypeVar

from ornitho.model.abstract import BaseModel

# Create a generic variable that can be 'DeletableModel', or any subclass.
T = TypeVar("T", bound="DeletableModel")


class DeletableModel(BaseModel, ABC):
    """Abstract class for deletable models via DELETE /ENDPOINT"""

    DELETE_METHOD: str = "DELETE"
    DELETE_ENDPOINT: Optional[str] = None

    def delete(self: T):
        """ Delete an instance on ornitho
        """
        url = f"{self.DELETE_ENDPOINT if self.DELETE_ENDPOINT is not None else self.ENDPOINT}/{self.id_}"
        self.request(method=self.DELETE_METHOD, url=url)
