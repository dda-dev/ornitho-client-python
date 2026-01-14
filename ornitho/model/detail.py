from typing import List


class Detail:
    def __init__(
        self, count: int, sex: str, age: str, id_observation: int = None
    ) -> None:
        """Detail constructor
        :param count: Count
        :param sex: Sex
        :param age: Age
        :param id_observation: ID of an observation
        :type count: int
        :type sex: str
        :type age: str
        :type id_observation: int
        """
        self.count: int = count
        self.sex: str = sex
        self.age: str = age
        self.id_observation: int | None = id_observation

    @property
    def excel_str_german(self):
        excel_str = f"{self.count}x"
        if self.sex == "M":
            excel_str = f"{excel_str} Männchen"
        elif self.sex == "F":
            excel_str = f"{excel_str} Weibchen"
        elif self.sex == "FT":
            excel_str = (
                f"{excel_str} weibchenfarbig"
                if self.count == 1
                else f"{excel_str} weibchenfarbige"
            )

        if self.age == "PULL":
            excel_str = (
                f"{excel_str} Pullus / nicht-flügge"
                if self.count == 1
                else f"{excel_str} Pulli / nicht-flügge"
            )
        elif self.age == "1Y":
            excel_str = (
                f"{excel_str} 1. KJ / diesjährig"
                if self.count == 1
                else f"{excel_str} 1. KJ / diesjährige"
            )
        elif self.age == "2Y":
            excel_str = (
                f"{excel_str} 2. KJ / vorjährig"
                if self.count == 1
                else f"{excel_str} 2. KJ / vorjährige"
            )
        elif self.age == "3Y":
            excel_str = f"{excel_str} 3. KJ"
        elif self.age == "4Y":
            excel_str = f"{excel_str} 4. KJ"
        elif self.age == "5Y":
            excel_str = f"{excel_str} 5. KJ"
        elif self.age == "IMM":
            excel_str = (
                f"{excel_str} immatur" if self.count == 1 else f"{excel_str} immature"
            )
        elif self.age == "AD":
            excel_str = (
                f"{excel_str} adult" if self.count == 1 else f"{excel_str} adulte"
            )

        return excel_str

    def __str__(self) -> str:
        return f"{self.count}-{self.sex}-{self.age}"

    def __eq__(self, other):
        return (
            self.count == other.count
            and self.sex == other.sex
            and self.age == other.age
        )

    def __hash__(self):
        return hash((self.count, self.sex, self.age, self.id_observation))

    @staticmethod
    def list_to_excel_str(details: List["Detail"]):
        excel_str = ""
        for detail in details:
            if excel_str:
                excel_str = f"{excel_str} / {detail.excel_str_german}"
            else:
                excel_str = f"{detail.excel_str_german}"
        return excel_str
