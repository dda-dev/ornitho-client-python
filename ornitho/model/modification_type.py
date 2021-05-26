from enum import Enum


class ModificationType(Enum):
    ONLY_MODIFIED = "only_modified"
    ONLY_DELETED = "only_deleted"
    ALL = "all"
