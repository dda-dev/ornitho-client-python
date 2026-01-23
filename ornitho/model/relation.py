from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .observation import Observation


class RelationType(Enum):
    SAME = "same"
    PROBABLE = "probable"
    DIFF = "diff"


class Relation:
    def __init__(
        self,
        with_id: int,
        type: RelationType,
        first_observation: "Observation" = None,
        second_observation: "Observation" = None,
    ) -> None:
        """Detail constructor
        :param with_id: Id of the related observation
        :param type: Type of the relation
        :type with_id: int
        :type type: RelationType
        """
        self.with_id: int = with_id
        self.type: RelationType = type
        self.first_observation: Observation = first_observation
        self.second_observation: Observation = second_observation

    def __str__(self) -> str:
        return f"{self.with_id}-{self.type.value}-{self.first_observation}-{self.second_observation}"

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__qualname__} {self}>"

    def __eq__(self, other):
        return self.with_id == other.with_id and self.type == other.type

    def __hash__(self):
        return hash((self.with_id, self.type))
