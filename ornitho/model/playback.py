from .species import Species


class Playback:
    def __init__(self, form_id: int, species_id: int, played: bool) -> None:
        self.form_id: int = form_id
        self.species_id: int = species_id
        self.played: bool = played

    @property
    def species(self) -> Species:
        return Species(id_=self.species_id)

    def __str__(self) -> str:
        return f"{self.form_id}-{self.species_id}-{self.played}"

    def __eq__(self, other):
        return (
            self.form_id == other.form_id
            and self.species_id == other.species_id
            and self.played == other.played
        )

    def __hash__(self):
        return hash((self.form_id, self.species_id, self.played))

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__qualname__} {self}>"
