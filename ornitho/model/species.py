from typing import Optional

from ornitho.model.abstract import ListableModel
from ornitho.model.family import Family
from ornitho.model.taxo_group import TaxonomicGroup


class Species(ListableModel):

    ENDPOINT: str = "species"

    def __init__(self, id_: int) -> None:
        """ Species constructor
        :param id_: ID, which is used to get the observation from Biolovison
        :type id_: int
        """
        super(Species, self).__init__(id_)
        self._taxo_group: Optional[TaxonomicGroup] = None
        self._family: Optional[Family] = None

    @property
    def id_taxo_group(self) -> int:
        return int(self._raw_data["id_taxo_group"])

    @property
    def sys_order(self) -> int:
        return int(self._raw_data["sys_order"])

    @property
    def sempach_id_family(self) -> int:
        return int(self._raw_data["sempach_id_family"])

    @property
    def category_1(self) -> str:
        return self._raw_data["category_1"]

    @property
    def rarity(self) -> str:
        return self._raw_data["rarity"]

    @property
    def atlas_start(self) -> int:
        return int(self._raw_data["atlas_start"])

    @property
    def atlas_end(self) -> int:
        return int(self._raw_data["atlas_end"])

    @property
    def latin_name(self) -> str:
        return self._raw_data["latin_name"]

    @property
    def french_name(self) -> str:
        return self._raw_data["french_name"]

    @property
    def french_name_plur(self) -> str:
        return self._raw_data["french_name_plur"]

    @property
    def german_name(self) -> str:
        return self._raw_data["german_name"]

    @property
    def german_name_plur(self) -> str:
        return self._raw_data["german_name_plur"]

    @property
    def english_name(self) -> str:
        return self._raw_data["english_name"]

    @property
    def english_name_plur(self) -> str:
        return self._raw_data["english_name_plur"]

    @property
    def is_used(self) -> bool:
        return False if self._raw_data.get("is_used") == "0" else True

    @property
    def taxo_group(self) -> TaxonomicGroup:
        if self._taxo_group is None:
            self._taxo_group = TaxonomicGroup.get(self.id_taxo_group)
        return self._taxo_group

    @property
    def family(self) -> Family:
        if self._family is None:
            self._family = Family.get(self.sempach_id_family)
        return self._family
