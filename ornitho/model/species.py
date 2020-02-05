from ornitho.model.abstract import ListableModel


class Species(ListableModel):
    ENDPOINT: str = "species"

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
