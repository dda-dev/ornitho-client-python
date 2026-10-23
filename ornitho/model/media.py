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
        return self._raw_data.get("obs_hidden") == "1"

    @property
    def surname(self) -> str:
        return self._raw_data.get("surname") or ""

    @property
    def name(self) -> str:
        return self._raw_data.get("name") or "unknown"

    @property
    def advanced_observer(self) -> bool:
        return self._raw_data.get("advanced_observer") == "1"

    @property
    def traid(self) -> int:
        return int(self._raw_data.get("traid")) or -1

    @property
    def tra_hidden(self) -> bool:
        return self._raw_data.get("tra_hidden") == "1"

    @property
    def tra_surname(self) -> str:
        return self._raw_data.get("tra_surname") or ""

    @property
    def tra_name(self) -> str:
        return self._raw_data.get("tra_name") or ""

    @property
    def obs_power_user(self) -> bool:
        return self._raw_data.get("obs_power_user") == "1"

    @property
    def tra_power_user(self) -> bool:
        return self._raw_data.get("tra_power_user") == "1"

    @property
    def media(self) -> str:
        return self._raw_data.get("media") or self._raw_data.get("type")

    @property
    def has_large(self) -> bool:
        return self._raw_data.get("has_large") == "1"

    @property
    def insert_date(self) -> datetime:
        if self._raw_data.get("insert_date") is None:
            return datetime.now()
        timing = datetime.fromtimestamp(
            int(self._raw_data["insert_date"]["@timestamp"]),
        ).astimezone()
        return timing

    @property
    def url(self) -> str:
        url = self.photo
        if url is None and self._raw_data.get("path") is not None and self._raw_data.get("filename") is not None:
          url = self._raw_data.get("path")+"/"+self._raw_data.get("filename")
        return url

    @property
    def photo(self) -> str:
        if self._raw_data.get("photo") is None:
            return "unknown"
        if self.has_large and self.media == "PHOTO":
            return self._raw_data["photo"].replace("xsmall", "large")
        elif self.media == "PHOTO":
            return self._raw_data["photo"].replace("xsmall/", "")
        else:
            return self._raw_data["photo"]

    @property
    def photo_small(self) -> Optional[str]:
        if self._raw_data.get("photo") is None:
            return None
        return self._raw_data["photo"] if self.media == "PHOTO" else None
