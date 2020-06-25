from abc import ABC
from typing import TypeVar

from ornitho.model.abstract import BaseModel

# Create a generic variable that can be 'DeletableModel', or any subclass.
T = TypeVar("T", bound="DeletableModel")


class DeletableModel(BaseModel, ABC):
    """Abstract class for deletable models via DELETE /ENDPOINT"""

    def delete(self: T):
        """ Delete an instance on ornitho
        """
        url = f"{self.ENDPOINT}/{self.id_}"
        self.request(method="delete", url=url)
