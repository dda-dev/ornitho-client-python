from .species import Species


class Playback:
    def __init__(self, id_form: int, id_species: int, played: bool) -> None:
        self.id_form: int = id_form
        self.id_species: int = id_species
        self.played: bool = played

    @property
    def species(self) -> Species:
        return Species(id_=self.id_species)

    def __str__(self) -> str:
        return f"{self.id_form}-{self.id_species}-{self.played}"

    def __eq__(self, other):
        return (
            self.id_form == other.id_form
            and self.id_species == other.id_species
            and self.played == other.played
        )

    def __hash__(self):
        return hash((self.id_form, self.id_species, self.played))

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__qualname__} {self}>"
