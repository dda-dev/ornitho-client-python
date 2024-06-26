from typing import Optional

from ornitho.model.abstract import ListableModel
from ornitho.model.abstract.base_model import check_refresh
from ornitho.model.family import Family
from ornitho.model.taxo_group import TaxonomicGroup


class Species(ListableModel):
    ENDPOINT: str = "species"

    def __init__(self, id_: int) -> None:
        """Species constructor
        :param id_: ID, which is used to get the observation from Biolovison
        :type id_: int
        """
        super(Species, self).__init__(id_)
        self._taxo_group: Optional[TaxonomicGroup] = None
        self._family: Optional[Family] = None

    @property  # type: ignore
    @check_refresh
    def id_taxo_group(self) -> int:
        return int(self._raw_data["id_taxo_group"])

    @property  # type: ignore
    @check_refresh
    def sys_order(self) -> int:
        return int(self._raw_data["sys_order"])

    @property  # type: ignore
    @check_refresh
    def sempach_id_family(self) -> int:
        return int(self._raw_data["sempach_id_family"])

    @property  # type: ignore
    @check_refresh
    def category_1(self) -> str:
        return self._raw_data["category_1"]

    @property  # type: ignore
    @check_refresh
    def rarity(self) -> str:
        return self._raw_data["rarity"]

    @property  # type: ignore
    @check_refresh
    def atlas_start(self) -> int:
        return int(self._raw_data["atlas_start"])

    @property  # type: ignore
    @check_refresh
    def atlas_end(self) -> int:
        return int(self._raw_data["atlas_end"])

    @property  # type: ignore
    @check_refresh
    def latin_name(self) -> str:
        return self._raw_data["latin_name"]

    @property  # type: ignore
    @check_refresh
    def french_name(self) -> str:
        return self._raw_data["french_name"]

    @property  # type: ignore
    @check_refresh
    def french_name_plur(self) -> str:
        return self._raw_data["french_name_plur"]

    @property  # type: ignore
    @check_refresh
    def german_name(self) -> str:
        return self._raw_data["german_name"].replace("|", "")

    @property  # type: ignore
    @check_refresh
    def german_name_plur(self) -> str:
        return self._raw_data["german_name_plur"]

    @property  # type: ignore
    @check_refresh
    def english_name(self) -> str:
        return self._raw_data["english_name"]

    @property  # type: ignore
    @check_refresh
    def english_name_plur(self) -> str:
        return self._raw_data["english_name_plur"]

    @property  # type: ignore
    @check_refresh
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

    # Following Properties appear only when requesting an Observation. Mapping to the species API is done here
    @property
    def taxonomy(self) -> int:
        return (
            int(self._raw_data["taxonomy"])
            if "taxonomy" in self._raw_data
            else self.id_taxo_group
        )

    @property
    def category(self) -> str:
        return (
            self._raw_data["category"]
            if "category" in self._raw_data
            else self.category_1
        )

    @property
    def name(self) -> str:
        return self._raw_data["name"] if "name" in self._raw_data else self.german_name

    @property
    def dda_id_species(self) -> Optional[int]:
        return (
            int(self._raw_data["dda_id_species"]["#text"])
            if "dda_id_species" in self._raw_data
            else None
        )

    @property
    def euring_id_species(self) -> Optional[int]:
        return (
            int(self._raw_data["euring_id_species"]["#text"])
            if "euring_id_species" in self._raw_data
            else None
        )
