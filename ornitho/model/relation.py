from enum import Enum


class RelationType(Enum):
    SAME = "same"
    PROBABLE = "probable"
    DIFF = "diff"


class Relation:
    def __init__(self, with_id: int, type: RelationType) -> None:
        """Detail constructor
        :param with_id: Id of the related observation
        :param type: Type of the relation
        :type with_id: int
        :type type: RelationType
        """
        self.with_id: int = with_id
        self.type: RelationType = type

    def __str__(self) -> str:
        return f"{self.with_id}-{self.type.value}"

    def __eq__(self, other):
        return self.with_id == other.with_id and self.type == other.type
