class Project:
    def __init__(self, id_: int, project_code: str, project_name: str) -> None:
        """project constructor
        :param id_: ID in th ornitho system
        :param project_code: Shot project Code
        :param project_name: Full project name
        :type id_: int
        :type project_code: str
        :type project_name: str
        """
        self.id_: int = id_
        self.project_code: str = project_code
        self.project_name: str = project_name

    def __str__(self) -> str:
        return f"{self.id_}:{self.project_code}"

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__qualname__} {self}>"

    def __eq__(self, other):
        return (
            self.id_ == other.id_
            and self.project_code == other.project_code
            and self.project_name == other.project_name
        )

    def __hash__(self):
        return hash((self.id_, self.project_code, self.project_name))
