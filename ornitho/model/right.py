from typing import List, Union

from ornitho import APIRequester


class Right:
    ENDPOINT: str = "observers/rights"

    def __init__(self, id_: int, name: str, comment: str) -> None:
        """Detail constructor
        :param id: ID
        :param name: Name
        :param comment: Comment
        :type id: int
        :type name: str
        :type comment: str
        """
        self.id_: int = id_
        self.name: str = name
        self.comment: str = comment

    def __str__(self) -> str:
        return f"{self.id_}-{self.name}-{self.comment}"

    @classmethod
    def retrieve_for_observer(cls, id_observer: Union[int, str]) -> List["Right"]:
        with APIRequester() as requester:
            url = f"{cls.ENDPOINT}/{id_observer}"
            response, pk = requester.request_raw(
                method="get",
                url=url,
            )
        return (
            [
                cls(id_=int(right["id"]), name=right["name"], comment=right["comment"])
                for right in response["data"]["rights"]
            ]
            if "rights" in response["data"]
            else []
        )
