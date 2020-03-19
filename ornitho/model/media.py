from datetime import datetime
from typing import Optional

from ornitho.model.abstract import BaseModel


class Media(BaseModel):
    ENDPOINT: str = "media"

    @property
    def obid(self) -> int:
        return int(self._raw_data["obid"])

    @property
    def obs_hidden(self) -> bool:
        return False if self._raw_data["obs_hidden"] == "0" else True

    @property
    def surname(self) -> str:
        return self._raw_data["surname"]

    @property
    def name(self) -> str:
        return self._raw_data["name"]

    @property
    def advanced_observer(self) -> bool:
        return False if self._raw_data["advanced_observer"] == "0" else True

    @property
    def traid(self) -> int:
        return int(self._raw_data["traid"])

    @property
    def tra_hidden(self) -> bool:
        return False if self._raw_data["tra_hidden"] == "0" else True

    @property
    def tra_surname(self) -> str:
        return self._raw_data["tra_surname"]

    @property
    def tra_name(self) -> str:
        return self._raw_data["tra_name"]

    @property
    def obs_power_user(self) -> bool:
        return False if self._raw_data["obs_power_user"] == "0" else True

    @property
    def tra_power_user(self) -> bool:
        return False if self._raw_data["tra_power_user"] == "0" else True

    @property
    def media(self) -> str:
        return self._raw_data["media"]

    @property
    def has_large(self) -> bool:
        return False if self._raw_data["has_large"] == "0" else True

    @property
    def insert_date(self) -> datetime:
        timing = datetime.fromtimestamp(
            int(self._raw_data["insert_date"]["@timestamp"]),
            datetime.now().astimezone().tzinfo,
        )
        return timing

    @property
    def photo(self) -> str:
        if self.has_large and self.media == "PHOTO":
            return self._raw_data["photo"].replace("xsmall", "large")
        elif self.media == "PHOTO":
            return self._raw_data["photo"].replace("xsmall/", "")
        else:
            return self._raw_data["photo"]

    @property
    def photo_small(self) -> Optional[str]:
        return self._raw_data["photo"] if self.media == "PHOTO" else None
