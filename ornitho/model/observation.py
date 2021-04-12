import uuid
from copy import deepcopy
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import ornitho.model.form
from ornitho import APIException
from ornitho.model.abstract import (
    BaseModel,
    CreateableModel,
    DeletableModel,
    ListableModel,
    SearchableModel,
    UpdateableModel,
)
from ornitho.model.abstract.base_model import check_raw_data
from ornitho.model.detail import Detail
from ornitho.model.field_option import FieldOption
from ornitho.model.media import Media
from ornitho.model.observer import Observer
from ornitho.model.place import Place
from ornitho.model.relation import Relation, RelationType
from ornitho.model.species import Species


class ModificationType(Enum):
    ONLY_MODIFIED = "only_modified"
    ONLY_DELETED = "only_deleted"
    ALL = "all"


class EstimationCode(Enum):
    EXACT_VALUE = "EXACT_VALUE"
    ESTIMATION = "ESTIMATION"
    MINIMUM = "MINIMUM"
    NO_VALUE = "NO_VALUE"


class Precision(Enum):
    PRECISE = "precise"
    SQUARE = "square"
    PLACE = "place"
    MUNICIPALITY = "municipality"
    POLYGON = "polygone"
    TRANSECT = "transect"
    SUBPLACE = "subplace"
    POLYGON_PRECISE = "polygone_precise"
    TRANSECT_PRECISE = "transect_precise"
    SUBPLACE_PRECISE = "subplace_precise"


class Source(Enum):
    WEB = "WEB"
    MOBILE_DELAYED = "MOBILE_DELAYED"
    MOBILE_LIVE = "MOBILE_LIVE"
    MOBILE_FORM_LIVE = "MOBILE_FORM_LIVE"
    MOBILE_FORM_DELAYED = "MOBILE_FORM_DELAYED"
    MOBILE_LIVE_IOS = "MOBILE_LIVE_IOS"
    MOBILE_DELAYED_IOS = "MOBILE_DELAYED_IOS"
    MOBILE_FORM_LIVE_IOS = "MOBILE_FORM_LIVE_IOS"
    MOBILE_FORM_DELAYED_IOS = "MOBILE_FORM_DELAYED_IOS"


class Observation(
    ListableModel, SearchableModel, CreateableModel, DeletableModel, UpdateableModel
):
    """Representation of on Observation"""

    ENDPOINT: str = "observations"

    def __init__(
        self, id_: int = None, modification_type: ModificationType = None
    ) -> None:
        """Observation constructor
        :param id_: ID, which is used to get the observation from Biolovison – None if a new observation will be created
        :param modification_type: Set if the observation was retrieved via the 'diff' method
        :type id_: int
        :type modification_type: ModificationType
        """
        super(Observation, self).__init__(id_)
        self.modification_type = modification_type
        self._species: Optional[Species] = None
        self._observer: Optional[Observer] = None
        self._place: Optional[Place] = None
        self._form: Optional[ornitho.model.form.Form] = None
        self._resting_habitat: Optional[FieldOption] = None
        self._accuracy_of_location: Optional[FieldOption] = None
        self._observation_detail: Optional[FieldOption] = None
        self._atlas_code: Optional[FieldOption] = None
        self._medias: Optional[List[Media]] = None

    @classmethod
    def create_from_ornitho_json(cls, data: Dict[str, Any]) -> "Observation":
        if len(data["observers"]) > 1:
            raise APIException(
                f"More than one observer in sightings json found!\n{data['observers']}"
            )
        identifier: Optional[int] = (
            int(data["observers"][0]["id_sighting"])
            if "observers" in data and "id_sighting" in data["observers"][0]
            else None
        )
        obj = cls(identifier)
        obj._raw_data = data
        return obj

    @property  # type: ignore
    @check_raw_data("observers")
    def id_observer(self) -> int:
        if "id" in self._raw_data["observers"][0]:
            return int(self._raw_data["observers"][0]["id"])
        else:
            return int(self._raw_data["observers"][0]["@id"])

    @id_observer.setter
    def id_observer(self, value: int):
        self._observer = None
        self._raw_data["observers"] = [{"@id": value.__str__()}]

    @property  # type: ignore
    @check_raw_data("observers")
    def traid(self) -> int:
        return int(self._raw_data["observers"][0]["traid"])

    @property  # type: ignore
    @check_raw_data("observers")
    def guid(self) -> uuid.UUID:
        return uuid.UUID(self._raw_data["observers"][0]["guid"])

    @guid.setter
    def guid(self, value: uuid.UUID):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["guid"] = value.__str__()
        else:
            self._raw_data["observers"] = [{"guid": value.__str__()}]

    @property  # type: ignore
    @check_raw_data("observers")
    def timing(self) -> datetime:
        timing = datetime.fromtimestamp(
            int(self._raw_data["observers"][0]["timing"]["@timestamp"]),
        ).astimezone()
        return timing

    @timing.setter
    def timing(self, value: datetime):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["timing"] = {
                "@timestamp": int(value.timestamp()).__str__()
            }
        else:
            self._raw_data["observers"] = [
                {"timing": {"@timestamp": int(value.timestamp()).__str__()}}
            ]
        # Add date to raw_data, so ornitho can process it
        self._raw_data["date"] = {"@timestamp": int(value.timestamp()).__str__()}

    @property  # type: ignore
    @check_raw_data("observers")
    def coord_lat(self) -> float:
        return float(self._raw_data["observers"][0]["coord_lat"])

    @coord_lat.setter
    def coord_lat(self, value: float):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["coord_lat"] = value.__str__()
        else:
            self._raw_data["observers"] = [{"coord_lat": value.__str__()}]

    @property  # type: ignore
    @check_raw_data("observers")
    def coord_lon(self) -> float:
        return float(self._raw_data["observers"][0]["coord_lon"])

    @coord_lon.setter
    def coord_lon(self, value: float):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["coord_lon"] = value.__str__()
        else:
            self._raw_data["observers"] = [{"coord_lon": value.__str__()}]

    @property  # type: ignore
    @check_raw_data("observers")
    def altitude(self) -> int:
        return int(self._raw_data["observers"][0]["altitude"])

    @altitude.setter
    def altitude(self, value: int):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["altitude"] = value.__str__()
        else:
            self._raw_data["observers"] = [{"altitude": value.__str__()}]

    @property  # type: ignore
    @check_raw_data("observers")
    def id_form(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["id_form"])
            if "id_form" in self._raw_data["observers"][0]
            else None
        )

    @id_form.setter
    def id_form(self, value: int):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["id_form"] = value
        else:
            self._raw_data["observers"] = [{"id_form": value}]

    @property  # type: ignore
    @check_raw_data("observers")
    def precision(self) -> Precision:
        return Precision(self._raw_data["observers"][0]["precision"])

    @precision.setter
    def precision(self, value: Precision):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["precision"] = value.value
        else:
            self._raw_data["observers"] = [{"precision": value.value}]

    @property  # type: ignore
    @check_raw_data("observers")
    def estimation_code(self) -> Optional[EstimationCode]:
        return (
            EstimationCode(self._raw_data["observers"][0]["estimation_code"])
            if "estimation_code" in self._raw_data["observers"][0]
            else None
        )

    @estimation_code.setter
    def estimation_code(self, value: EstimationCode):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["estimation_code"] = value.value
        else:
            self._raw_data["observers"] = [{"estimation_code": value.value}]

    @property  # type: ignore
    @check_raw_data("species")
    def id_species(self) -> int:
        if "id" in self._raw_data["species"]:
            return int(self._raw_data["species"]["id"])
        else:
            return int(self._raw_data["species"]["@id"])

    @id_species.setter
    def id_species(self, value: int):
        self._species = None
        self._raw_data["species"] = {"@id": value.__str__()}

    @property  # type: ignore
    @check_raw_data("observers")
    def count(self) -> int:
        return int(self._raw_data["observers"][0]["count"])

    @count.setter
    def count(self, value: str):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["count"] = value.__str__()
        else:
            self._raw_data["observers"] = [{"count": value.__str__()}]

    @property  # type: ignore
    @check_raw_data("observers")
    def flight_number(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["flight_number"])
            if "flight_number" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def admin_hidden(self) -> bool:
        return (
            False
            if "admin_hidden" not in self._raw_data["observers"][0]
            or self._raw_data["observers"][0]["admin_hidden"] == "0"
            else True
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def admin_hidden_type(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["admin_hidden_type"]
            if "admin_hidden_type" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def source(self) -> Source:
        return Source(self._raw_data["observers"][0]["source"])

    @property  # type: ignore
    @check_raw_data("observers")
    def medias(self) -> Optional[List[Media]]:
        if self._medias is None and "medias" in self._raw_data["observers"][0]:
            self._medias = [
                Media.get(media["@id"])
                for media in self._raw_data["observers"][0]["medias"]
            ]
        return self._medias

    @property  # type: ignore
    @check_raw_data("observers")
    def media_urls(self) -> Optional[List[str]]:
        if "medias" in self._raw_data["observers"][0]:
            return [
                f"{media['path']}/{media['filename']}"
                for media in self._raw_data["observers"][0]["medias"]
            ]
        return None

    @property  # type: ignore
    @check_raw_data("observers")
    def comment(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["comment"]
            if "comment" in self._raw_data["observers"][0]
            else None
        )

    @comment.setter
    def comment(self, value: str):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["comment"] = value
        else:
            self._raw_data["observers"] = [{"comment": value}]

    @property  # type: ignore
    @check_raw_data("observers")
    def hidden_comment(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["hidden_comment"]
            if "hidden_comment" in self._raw_data["observers"][0]
            else None
        )

    @hidden_comment.setter
    def hidden_comment(self, value: str):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["hidden_comment"] = value
        else:
            self._raw_data["observers"] = [{"hidden_comment": value}]

    @property  # type: ignore
    @check_raw_data("observers")
    def hidden(self) -> bool:
        return (
            False
            if "hidden" not in self._raw_data["observers"][0]
            or self._raw_data["observers"][0]["hidden"] == "0"
            else True
        )

    @hidden.setter
    def hidden(self, value: bool):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["hidden"] = "1" if value else "0"
        else:
            self._raw_data["observers"] = [{"hidden": "1" if value else "0"}]

    @property  # type: ignore
    @check_raw_data("observers")
    def id_atlas_code(self) -> Optional[str]:
        id_atlas_code = (
            None
            if "atlas_code" not in self._raw_data["observers"][0]
            else self._raw_data["observers"][0]["atlas_code"]["@id"]
            if type(self._raw_data["observers"][0]["atlas_code"]) is dict
            else f"3_{self._raw_data['observers'][0]['atlas_code']}"
        )
        return id_atlas_code

    @id_atlas_code.setter
    def id_atlas_code(self, value: str):
        self._atlas_code = None
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["atlas_code"] = {"@id": value}
        else:
            self._raw_data["observers"] = [{"atlas_code": {"@id": value}}]

    @property  # type: ignore
    @check_raw_data("observers")
    def atlas_code_text(self) -> Optional[str]:
        atlas_code_text = (
            self._raw_data["observers"][0]["atlas_code"]["#text"]
            if "atlas_code" in self._raw_data["observers"][0]
            and "#text" in self._raw_data["observers"][0]["atlas_code"]
            else None
        )
        return atlas_code_text

    @property  # type: ignore
    @check_raw_data("observers")
    def details(self) -> Optional[List[Detail]]:
        details = None
        if "details" in self._raw_data["observers"][0]:
            if "@id" in self._raw_data["observers"][0]["details"][0]["sex"]:
                details = [
                    Detail(
                        int(detail["count"]), detail["sex"]["@id"], detail["age"]["@id"]
                    )
                    for detail in self._raw_data["observers"][0]["details"]
                ]
            else:
                details = [
                    Detail(int(detail["count"]), detail["sex"], detail["age"])
                    for detail in self._raw_data["observers"][0]["details"]
                ]
        return details

    @details.setter
    def details(self, value: List[Detail]):
        details_ornitho_format = [
            {
                "count": detail.count.__str__(),
                "sex": {"@id": detail.sex},
                "age": {"@id": detail.age},
            }
            for detail in value
        ]
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["details"] = details_ornitho_format
        else:
            self._raw_data["observers"] = [{"details": details_ornitho_format}]

    @property  # type: ignore
    @check_raw_data("observers")
    def insert_date(self) -> datetime:
        insert_date = datetime.fromtimestamp(
            int(self._raw_data["observers"][0]["insert_date"]["@timestamp"])
            if type(self._raw_data["observers"][0]["insert_date"]) is dict
            else int(self._raw_data["observers"][0]["insert_date"]),
        ).astimezone()
        return insert_date

    @property  # type: ignore
    @check_raw_data("observers")
    def update_date(self) -> Optional[datetime]:
        update_date = (
            datetime.fromtimestamp(
                int(self._raw_data["observers"][0]["update_date"]["@timestamp"])
                if type(self._raw_data["observers"][0]["update_date"]) is dict
                else int(self._raw_data["observers"][0]["update_date"]),
            ).astimezone()
            if "update_date" in self._raw_data["observers"][0]
            else None
        )
        return update_date

    @property  # type: ignore
    @check_raw_data("place")
    def id_place(self) -> int:
        if "place" not in self._raw_data:
            id_place = Place.find_closest_place(
                self.coord_lat, self.coord_lon, get_hidden=True
            ).id_
            if id_place is not None:
                self.id_place = int(id_place)
                return int(id_place)
        if "@id" in self._raw_data["place"]:
            return int(self._raw_data["place"]["@id"])
        else:
            return int(self._raw_data["place"]["id"])

    @id_place.setter
    def id_place(self, value: int):
        self._place = None
        self._raw_data["place"] = {"@id": value.__str__()}

    @property  # type: ignore
    @check_raw_data("observers")
    def id_resting_habitat(self) -> Optional[str]:
        if "resting_habitat" in self._raw_data["observers"][0]:
            if type(self._raw_data["observers"][0]["resting_habitat"]) is dict:
                return self._raw_data["observers"][0]["resting_habitat"]["@id"]
            else:
                return self._raw_data["observers"][0]["resting_habitat"]
        return None

    @id_resting_habitat.setter
    def id_resting_habitat(self, value: str):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["resting_habitat"] = value
        else:
            self._raw_data["observers"] = [{"resting_habitat": value}]

    @property  # type: ignore
    @check_raw_data("observers")
    def id_accuracy_of_location(self) -> Optional[str]:
        if "accuracy_of_location" in self._raw_data["observers"][0]:
            if type(self._raw_data["observers"][0]["accuracy_of_location"]) is dict:
                return self._raw_data["observers"][0]["accuracy_of_location"]["@id"]
            else:
                # return self._raw_data["observers"][0]["accuracy_of_location"]
                # pass, since accuracy_of_location isn't available in short version
                pass
        return None

    @property  # type: ignore
    @check_raw_data("observers")
    def id_observation_detail(self) -> Optional[str]:
        if "observation_detail" in self._raw_data["observers"][0]:
            if type(self._raw_data["observers"][0]["observation_detail"]) is dict:
                return self._raw_data["observers"][0]["observation_detail"]["@id"]
            else:
                return self._raw_data["observers"][0]["observation_detail"]
        return None

    @id_observation_detail.setter
    def id_observation_detail(self, value: str):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["observation_detail"] = value
        else:
            self._raw_data["observers"] = [{"observation_detail": value}]

    @property  # type: ignore
    @check_raw_data("species")
    def species(self) -> Species:
        """ Observed Species """
        if self._species is None:
            if "@id" in self._raw_data["species"]:
                self._species = Species.create_from_ornitho_json(
                    self._raw_data["species"]
                )
            else:
                self._species = Species.get(self._raw_data["species"]["id"])
                self._raw_data["species"] = self._species._raw_data
        return self._species

    @species.setter
    def species(self, value: Species):
        self.id_species = value.id_
        self._species = value

    @property  # type: ignore
    @check_raw_data("observers")
    def observer(self) -> Observer:
        """ Observing user """
        if self._observer is None:
            self._observer = Observer.create_from_ornitho_json(
                self._raw_data["observers"][0]
            )
        return self._observer

    @observer.setter
    def observer(self, value: Observer):
        self.id_observer = value.id_
        self._observer = value

    @property  # type: ignore
    @check_raw_data("place")
    def place(self) -> Place:
        """ Place of the observation """
        if self._place is None:
            self._place = Place.create_from_ornitho_json(self._raw_data["place"])
        return self._place

    @place.setter
    def place(self, value: Place):
        self._raw_data["place"] = value._raw_data
        self._place = value

    @property
    def form(self):
        if self._form is None and self.id_form is not None:
            self._form = ornitho.model.form.Form.create_from_ornitho_json(
                self._raw_data["form"]
            )
        return self._form

    @property
    def resting_habitat(self) -> Optional[FieldOption]:
        """ Resting habitat of the observation """
        if self._resting_habitat is None and self.id_resting_habitat:
            self._resting_habitat = FieldOption.get(self.id_resting_habitat)
        return self._resting_habitat

    @resting_habitat.setter
    def resting_habitat(self, value: FieldOption):
        self.id_resting_habitat = value.id_
        self._resting_habitat = value

    @property
    def accuracy_of_location(self) -> Optional[FieldOption]:
        """ Resting habitat of the observation """
        if self._accuracy_of_location is None and self.id_accuracy_of_location:
            self._accuracy_of_location = FieldOption.get(self.id_accuracy_of_location)
        return self._accuracy_of_location

    @property
    def observation_detail(self) -> Optional[FieldOption]:
        """ Observation detail of the observation """
        if self._observation_detail is None and self.id_observation_detail:
            self._observation_detail = FieldOption.get(self.id_observation_detail)
        return self._observation_detail

    @observation_detail.setter
    def observation_detail(self, value: FieldOption):
        self.id_observation_detail = value.id_
        self._observation_detail = value

    @property
    def atlas_code(self) -> Optional[FieldOption]:
        """ Atlas Code of the observation """
        if self._atlas_code is None and self.id_atlas_code:
            self._atlas_code = FieldOption.get(f"3_{self.id_atlas_code}")
        return self._atlas_code

    @atlas_code.setter
    def atlas_code(self, value: FieldOption):
        self.id_atlas_code = value.id_
        self._atlas_code = value

    @property  # type: ignore
    @check_raw_data("observers")
    def is_exported(self) -> bool:
        return (
            True
            if "observers" in self._raw_data
            and "is_exported" in self._raw_data["observers"][0]
            and self._raw_data["observers"][0]["is_exported"] == "1"
            else False
        )

    @is_exported.setter
    def is_exported(self, value: bool):
        value_as_str = "1" if value else "0"
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["is_exported"] = value_as_str
        else:
            self._raw_data["observers"] = [{"is_exported": value_as_str}]

    @property  # type: ignore
    @check_raw_data("observers")
    def export_date(self) -> Optional[datetime]:
        return (
            datetime.fromtimestamp(
                int(self._raw_data["observers"][0]["export_date"]["@timestamp"]),
            ).astimezone()
            if self.is_exported
            else None
        )

    @export_date.setter
    def export_date(self, value: datetime):
        if "observers" in self._raw_data:
            self._raw_data["observers"][0]["export_date"] = {
                "@timestamp": int(value.timestamp()).__str__()
            }
        else:
            self._raw_data["observers"] = [
                {"export_date": {"@timestamp": int(value.timestamp()).__str__()}}
            ]

    @property  # type: ignore
    @check_raw_data("observers")
    def notime(self) -> bool:
        return (
            False
            if "@notime" not in self._raw_data["observers"][0]["timing"]
            or self._raw_data["observers"][0]["timing"]["@notime"] == "0"
            else True
        )

    @notime.setter
    def notime(self, value: bool):
        if "observers" in self._raw_data:
            if "timing" in self._raw_data["observers"][0]:
                self._raw_data["observers"][0]["timing"]["@notime"] = (
                    "1" if value else "0"
                )
            else:
                self._raw_data["observers"][0]["timing"] = {
                    "@notime": "1" if value else "0"
                }
        else:
            self._raw_data["observers"] = [
                {"timing": {"@notime": "1" if value else "0"}}
            ]

    @property  # type: ignore
    @check_raw_data("observers")
    def project(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["project"])
            if "project" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def project_code(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["project_code"]
            if "project_code" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def cavs(self) -> Optional[str]:
        return (
            self._raw_data["observers"][0]["committees_validation"]["cavs"]
            if "committees_validation" in self._raw_data["observers"][0]
            and "cavs" in self._raw_data["observers"][0]["committees_validation"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def id_observer_vowa(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["vowa_id"])
            if "vowa_id" in self._raw_data["observers"][0]
            else int(self._raw_data["observers"][0]["@vowa_id"])
            if "@vowa_id" in self._raw_data["observers"][0]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def second_hand(self) -> bool:
        return (
            False
            if "second_hand" not in self._raw_data["observers"][0]
            or self._raw_data["observers"][0]["second_hand"] == "0"
            else True
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_couples(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["extended_info"]["colony"]["couples"])
            if "extended_info" in self._raw_data["observers"][0]
            and "colony" in self._raw_data["observers"][0]["extended_info"]
            and "couples" in self._raw_data["observers"][0]["extended_info"]["colony"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_nests(self) -> Optional[int]:
        return (
            int(self._raw_data["observers"][0]["extended_info"]["colony"]["nests"])
            if "extended_info" in self._raw_data["observers"][0]
            and "colony" in self._raw_data["observers"][0]["extended_info"]
            and "nests" in self._raw_data["observers"][0]["extended_info"]["colony"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_occupied_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony"][
                    "occupied_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony" in self._raw_data["observers"][0]["extended_info"]
            and "occupied_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_nests_is_min(self) -> Optional[bool]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony"][
                    "nests_is_min"
                ]
            )
            == 1
            if "extended_info" in self._raw_data["observers"][0]
            and "colony" in self._raw_data["observers"][0]["extended_info"]
            and "nests_is_min"
            in self._raw_data["observers"][0]["extended_info"]["colony"]
            else False
            if self.colony_nests is not None
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_couples(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "couples"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "couples"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_natural_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_natural_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_natural_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_natural_nests_is_min(self) -> Optional[bool]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_natural_nests_is_min"
                ]
            )
            == 1
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_natural_nests_is_min"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else False
            if self.colony_extended_nb_natural_nests is not None
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_artificial_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_artificial_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_artificial_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_artificial_nests_is_min(self) -> Optional[bool]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_artificial_nests_is_min"
                ]
            )
            == 1
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_artificial_nests_is_min"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else False
            if self.colony_extended_nb_artificial_nests is not None
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_natural_occup_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_natural_occup_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_natural_occup_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_artificial_occup_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_artificial_occup_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_artificial_occup_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_natural_other_species_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_natural_other_species_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_natural_other_species_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_artificial_other_species_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_artificial_other_species_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_artificial_other_species_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_natural_destructed_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_natural_destructed_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_natural_destructed_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_artificial_destructed_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_artificial_destructed_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_artificial_destructed_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def colony_extended_nb_construction_nests(self) -> Optional[int]:
        return (
            int(
                self._raw_data["observers"][0]["extended_info"]["colony_extended"][
                    "nb_construction_nests"
                ]
            )
            if "extended_info" in self._raw_data["observers"][0]
            and "colony_extended" in self._raw_data["observers"][0]["extended_info"]
            and "nb_construction_nests"
            in self._raw_data["observers"][0]["extended_info"]["colony_extended"]
            else None
        )

    @property  # type: ignore
    @check_raw_data("observers")
    def nest_number(self) -> Optional[int]:
        if (
            "protocol" in self._raw_data["observers"][0]
            and "nest_number" in self._raw_data["observers"][0]["protocol"]
        ):
            if type(self._raw_data["observers"][0]["protocol"]["nest_number"]) is dict:
                return int(
                    self._raw_data["observers"][0]["protocol"]["nest_number"]["@id"]
                )
            else:
                return int(self._raw_data["observers"][0]["protocol"]["nest_number"])
        return None

    @property  # type: ignore
    @check_raw_data("observers")
    def occupied_nest_number(self) -> Optional[int]:
        if (
            "protocol" in self._raw_data["observers"][0]
            and "occupied_nest_number" in self._raw_data["observers"][0]["protocol"]
        ):
            if (
                type(self._raw_data["observers"][0]["protocol"]["occupied_nest_number"])
                is dict
            ):
                return int(
                    self._raw_data["observers"][0]["protocol"]["occupied_nest_number"][
                        "@id"
                    ]
                )
            else:
                return int(
                    self._raw_data["observers"][0]["protocol"]["occupied_nest_number"]
                )
        return None

    @property  # type: ignore
    @check_raw_data("observers")
    def relations(self) -> List[Relation]:
        return (
            [
                Relation(
                    with_id=int(relation["with"]), type=RelationType(relation["type"])
                )
                for relation in self._raw_data["observers"][0]["protocol"]["relations"]
            ]
            if "protocol" in self._raw_data["observers"][0]
            and "relations" in self._raw_data["observers"][0]["protocol"]
            else []
        )

    # @relations.setter
    # def relations(self, value: List[Relation]):
    #     relations_ornitho_format = [
    #         {
    #             "with": str(relation.with_id),
    #             "type": relation.type.value,
    #         }
    #         for relation in value
    #     ]
    #     if "observers" in self._raw_data:
    #         if "protocol" in self._raw_data["observers"][0]:
    #             self._raw_data["observers"][0]["protocol"]["relations"] = relations_ornitho_format
    #         else:
    #             self._raw_data["observers"][0] = {"protocol": {"relations": relations_ornitho_format}}
    #     else:
    #         self._raw_data["observers"] = [{"protocol": {"relations": relations_ornitho_format}}]

    @property  # type: ignore
    @check_raw_data("observers")
    def direction(self) -> List[Relation]:
        return (
            self._raw_data["observers"][0]["protocol"]["direction"]
            if "protocol" in self._raw_data["observers"][0]
            and "direction" in self._raw_data["observers"][0]["protocol"]
            else None
        )

    @classmethod
    def by_observer(
        cls,
        id_observer: int,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        **kwargs: Union[str, int, float, bool],
    ) -> Tuple[List["Observation"], Optional[str]]:
        """Retrieves a (paged) list of observations from one observer
        :param id_observer: Current data, probably received from the API
        :param pagination_key: Pagination key, which can be used to retrieve the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param kwargs: Additional filter values
        :type id_observer: int
        :type pagination_key: Optional[str]
        :type short_version: bool
        :type kwargs: Union[str, int, float, bool]
        :return: Tuple of observations and an optional pagination key
        :rtype: Tuple[List[Observation], Optional[str]]
        """
        observations, pk = cls.list(
            request_all=False,
            pagination_key=pagination_key,
            short_version=short_version,
            id_observer=id_observer,
            **kwargs,
        )
        return observations, pk

    @classmethod
    def by_observer_all(
        cls,
        id_observer: int,
        short_version: bool = False,
        **kwargs: Union[str, int, float, bool],
    ) -> List["Observation"]:
        """Retrieves a list of all observations from one observer
        :param id_observer: Current data, probably received from the API
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
        :param kwargs: Additional filter values
        :type id_observer: int
        :type short_version: bool
        :type kwargs: Union[str, int, float, bool]
        :return: List of observations
        :rtype: List[Observation]
        """
        observations = cls.list_all(
            id_observer=id_observer, short_version=short_version, **kwargs
        )
        return observations

    @classmethod
    def diff(
        cls,
        date: datetime,
        modification_type: ModificationType = None,
        id_taxo_group: int = None,
        only_protocol: Union[str, BaseModel] = None,
        only_form: bool = None,
        retrieve_observations: bool = False,
    ) -> List["Observation"]:
        """Retrieves a list of observations which changed in between now and a given date
        :param date: Date in the past, to which changed observation should be searched
        :param modification_type: Type of modification.
        :param id_taxo_group: Optional taxo group, to which the observerd species must belong to
        :param only_protocol: Return only observation which are part of the given Protocol (Protocol Instance or Name)
        :param only_form: Return only observation which are part of a form
        :param retrieve_observations: Indicates if the observation object should be retrieved. Default: False
        :type date: datetime
        :type modification_type: ModificationType
        :type id_taxo_group: int
        :type only_protocol: Union[str, "Protocol"]
        :type only_form: bool
        :type retrieve_observations: bool
        :return: List of observations
        :rtype: List[Observation]
        """
        url = f"{cls.ENDPOINT}/diff"
        params = dict()
        if modification_type:
            params["modification_type"] = modification_type.value
        if id_taxo_group:
            params["id_taxo_group"] = id_taxo_group.__str__()
        if only_protocol:
            from ornitho.model.protocol import Protocol

            if isinstance(only_protocol, Protocol):
                params["only_protocol"] = only_protocol.name
            else:
                params["only_protocol"] = only_protocol.__str__()
        if only_form:
            params["only_form"] = "1"

        date = date.replace(microsecond=0)
        if date.tzinfo:
            date = date.astimezone(datetime.now().astimezone().tzinfo).replace(
                tzinfo=None
            )
        params[
            "date"
        ] = (
            date.isoformat()
        )  # Format here, because isoformat is mostly ignored, except here

        changed_observations = cls.request(method="get", url=url, params=params)
        observations = []
        for obs in changed_observations:
            if obs["modification_type"] == "updated":
                modification_type = ModificationType.ONLY_MODIFIED
            else:
                modification_type = ModificationType.ONLY_DELETED
            if (
                retrieve_observations
                and modification_type == ModificationType.ONLY_MODIFIED
            ):
                observations.append(cls.get(int(obs["id_sighting"])))
            else:
                observations.append(
                    cls(
                        id_=int(obs["id_sighting"]), modification_type=modification_type
                    )
                )
        return observations

    @classmethod
    def create(  # type: ignore
        cls,
        observer: Union[int, Observer],
        species: Union[int, Species],
        timing: datetime,
        coord_lat: float,
        coord_lon: float,
        precision: Precision,
        estimation_code: EstimationCode,
        guid: uuid.UUID = None,
        id_form: int = None,
        place: Optional[Union[int, Place]] = None,
        notime: bool = False,
        count: int = None,
        altitude: int = None,
        comment: str = None,
        hidden_comment: str = None,
        hidden: bool = False,
        export_date: datetime = None,
        atlas_code: Union[str, FieldOption] = None,
        details: List[Detail] = None,
        resting_habitat: Union[str, FieldOption] = None,
        observation_detail: Union[str, FieldOption] = None,
        # relations: List[Relation] = None,
        create_in_ornitho: bool = True,
    ) -> "Observation":
        observation = cls()

        if isinstance(observer, Observer):
            observation.observer = observer
        else:
            observation.id_observer = observer

        if isinstance(species, Species):
            observation.species = species
        else:
            observation.id_species = species

        if guid:
            observation.guid = guid
        else:
            observation.guid = uuid.uuid4()

        if id_form:
            observation.id_form = id_form

        if place:
            if isinstance(place, Place):
                observation.place = place
            else:
                observation.id_place = place

        observation.timing = timing
        observation.notime = notime
        observation.coord_lat = coord_lat
        observation.coord_lon = coord_lon
        observation.precision = precision
        observation.estimation_code = estimation_code
        if count:
            observation.count = count
        if altitude:
            observation.altitude = altitude
        if comment:
            observation.comment = comment

        if hidden_comment:
            observation.hidden_comment = hidden_comment

        if hidden:
            observation.hidden = hidden

        if export_date:
            observation.is_exported = True
            observation.export_date = (
                export_date  # Doesn't work as expected, will always be 1970-01-01 ...
            )

        if atlas_code:
            if isinstance(atlas_code, FieldOption):
                observation.atlas_code = atlas_code
            else:
                observation.id_atlas_code = atlas_code

        if details:
            observation.details = details

        if resting_habitat:
            if isinstance(resting_habitat, FieldOption):
                observation.resting_habitat = resting_habitat
            else:
                observation.id_resting_habitat = resting_habitat

        if observation_detail:
            if isinstance(observation_detail, FieldOption):
                observation.observation_detail = observation_detail
            else:
                observation.id_observation_detail = observation_detail

        # if relations:
        #     observation.relations = relations

        if create_in_ornitho:
            observation._id = cls.create_in_ornitho(
                data={"sightings": [observation.raw_data_trim_field_ids()]}
            )
        return observation

    def mark_as_exported(self, export_date: Optional[datetime] = None):
        if self.id_ is None:
            self.refresh()
        self.is_exported = True
        if export_date:
            self.export_date = export_date
        else:
            self.export_date = datetime.now() - timedelta(
                seconds=2
            )  # Subtract 2 seconds, because the ornitho time is a little ahead
        self.update()

    def raw_data_trim_field_ids(self) -> Dict[str, Any]:
        raw_data = deepcopy(self._raw_data)

        if self.id_resting_habitat:
            raw_data["observers"][0]["resting_habitat"] = self.id_resting_habitat.split(
                "_"
            )[1]

        if self.id_observation_detail:
            raw_data["observers"][0][
                "observation_detail"
            ] = self.id_observation_detail.split("_")[1]

        return raw_data
