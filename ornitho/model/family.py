from typing import Optional

from ornitho.model.abstract import ListableModel
from ornitho.model.taxo_group import TaxonomicGroup


class Family(ListableModel):

    ENDPOINT: str = "families"

    def __init__(self, id_: int) -> None:
        """ Family constructor
        :param id_: ID, which is used to get the observation from Biolovison
        :type id_: int
        """
        super(Family, self).__init__(id_)
        self._taxo_group: Optional[TaxonomicGroup] = None

    @property
    def id_taxo_group(self) -> int:
        return int(self._raw_data["id_taxo_group"])

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def latin_name(self) -> str:
        return self._raw_data["latin_name"]

    @property
    def generic(self) -> bool:
        return False if self._raw_data.get("generic") == "0" else True

    @property
    def taxo_group(self) -> TaxonomicGroup:
        if self._taxo_group is None:
            self._taxo_group = TaxonomicGroup.get(self.id_taxo_group)
        return self._taxo_group
