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
