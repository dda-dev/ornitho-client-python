from abc import ABC
from typing import TypeVar

from ornitho.model.abstract import BaseModel

# Create a generic variable that can be 'CreateableModel', or any subclass.
T = TypeVar("T", bound="UpdateableModel")


class UpdateableModel(BaseModel, ABC):
    """Abstract class for updateable models via POST /ENDPOINT"""

    def update(
        self: T,
        retries: int = 0,
    ):
        """Update an instance on ornitho, respecting the specific model characteristics"""
        url = f"{self.ENDPOINT}/{self.id_}"
        if self.__class__.__name__ == "Observation":
            body = {"data": {"sightings": [self.raw_data_trim_field_ids()]}}
        else:
            body = self.raw_data_trim_field_ids()
        response = self.request(method="put", url=url, body=body, retries=retries)
        return response
