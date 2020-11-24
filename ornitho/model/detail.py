class Detail:
    def __init__(self, count: int, sex: str, age: str) -> None:
        """Detail constructor
        :param count: Count
        :param sex: Sex
        :param age: Age
        :type count: int
        :type sex: str
        :type age: str
        """
        self.count: int = count
        self.sex: str = sex
        self.age: str = age

    def __str__(self) -> str:
        return f"{self.count}-{self.sex}-{self.age}"

    def __eq__(self, other):
        return (
            self.count == other.count
            and self.sex == other.sex
            and self.age == other.age
        )
