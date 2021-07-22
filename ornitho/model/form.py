from copy import deepcopy
from datetime import date, time
from typing import Any, Dict, List, Optional, Union

import ornitho.model.observation
from ornitho.api_exception import APIException
from ornitho.api_requester import APIRequester
from ornitho.model.abstract import CreateableModel, DeletableModel
from ornitho.model.observation import Observation
from ornitho.model.place import Place
from ornitho.model.protocol import Protocol
from ornitho.model.species import Species


class Form(CreateableModel, DeletableModel):
    ENDPOINT = "observations/search"
    CREATE_ENDPOINT = "observations"
    DELETE_METHOD = "POST"
    DELETE_ENDPOINT = "observations/delete_list"

    def __init__(self, id_: int = None) -> None:
        """Form constructor
        :param id_: ID, which is used to get the form from Biolovison
        :type id_: int
        """
        super(Form, self).__init__(id_)
        self._observations: Optional[List[Observation]] = None
        self._id_place: Optional[Union[str, int]] = None

    def instance_url(self) -> str:
        """Returns url for this instance
        :return: Instance's url
        :rtype: str
        """
        return f"{self.ENDPOINT}"

    def refresh(self, short_version: bool = False) -> "Form":
        """Refresh local model
        Call the api and refresh fields from response
        :return: Refreshed Object
        :rtype: Form
        """
        with APIRequester() as requester:
            data, pagination_key = requester.request_raw(
                method="POST",
                url=self.instance_url(),
                short_version=short_version,
                body={"id_form": self.id_},
            )
            if "data" in data and "forms" in data["data"]:
                data = data["data"]["forms"][0]
                self._previous = self._raw_data
                self._raw_data = data
                self._observations = None
            else:
                raise APIException(f"Unrecognized response: {data}")
        return self

    @property
    def id_form_universal(self) -> str:
        return self._raw_data["id_form_universal"]

    @property
    def day(self) -> Optional[date]:
        if "day" in self._raw_data:
            return date.fromtimestamp(
                int(self._raw_data["day"]["@timestamp"]),
            )
        elif self.observations is not None:
            return self.observations[0].timing.date()
        else:
            return None

    @property
    def time_start(self) -> time:
        splitted = self._raw_data["time_start"].split(":")
        return time(
            hour=int(splitted[0]),
            minute=int(splitted[1]),
            second=int(splitted[2]),
        )

    @time_start.setter
    def time_start(self, value: time):
        self._raw_data["time_start"] = value.strftime("%H:%M:%S")

    @property
    def time_stop(self) -> time:
        splitted = self._raw_data["time_stop"].split(":")
        return time(
            hour=int(splitted[0]),
            minute=int(splitted[1]),
            second=int(splitted[2]),
        )

    @time_stop.setter
    def time_stop(self, value: time):
        self._raw_data["time_stop"] = value.strftime("%H:%M:%S")

    @property
    def full_form(self) -> bool:
        return False if self._raw_data.get("full_form") == "0" else True

    @full_form.setter
    def full_form(self, value: bool):
        self._raw_data["full_form"] = "1" if value else "0"

    @property
    def version(self) -> int:
        return int(self._raw_data["version"])

    @property
    def lat(self) -> float:
        return float(self._raw_data["lat"])

    @property
    def lon(self) -> float:
        return float(self._raw_data["lon"])

    @property
    def id_form_mobile(self) -> Optional[str]:
        return (
            self._raw_data["id_form_mobile"]
            if "id_form_mobile" in self._raw_data
            else None
        )

    @property
    def comment(self) -> Optional[str]:
        return self._raw_data["comment"] if "comment" in self._raw_data else None

    @comment.setter
    def comment(self, value: str):
        self._raw_data["comment"] = value

    @property
    def protocol_name(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["protocol_name"]
            if "protocol" in self._raw_data
            else None
        )

    @protocol_name.setter
    def protocol_name(self, value: str):
        if "protocol" in self._raw_data:
            self._raw_data["protocol"]["protocol_name"] = value
        else:
            self._raw_data["protocol"] = {"protocol_name": value}

    @property
    def site_code(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["site_code"]
            if "protocol" in self._raw_data
            else None
        )

    @site_code.setter
    def site_code(self, value: str):
        if "protocol" in self._raw_data:
            self._raw_data["protocol"]["site_code"] = value
        else:
            self._raw_data["protocol"] = {"site_code": value}

    @property
    def local_site_code(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["local_site_code"]
            if "protocol" in self._raw_data
            else None
        )

    @property
    def advanced(self) -> Optional[bool]:
        return (
            self._raw_data["protocol"]["advanced"] != "0"
            if "protocol" in self._raw_data
            else None
        )

    @property
    def visit_number(self) -> Optional[int]:
        return (
            int(self._raw_data["protocol"]["visit_number"])
            if "protocol" in self._raw_data
            else None
        )

    @visit_number.setter
    def visit_number(self, value: int):
        if "protocol" in self._raw_data:
            self._raw_data["protocol"]["visit_number"] = value.__str__()
        else:
            self._raw_data["protocol"] = {"visit_number": value.__str__()}

    @property
    def sequence_number(self) -> Optional[int]:
        return (
            int(self._raw_data["protocol"]["sequence_number"])
            if "protocol" in self._raw_data
            else None
        )

    @sequence_number.setter
    def sequence_number(self, value: int):
        if "protocol" in self._raw_data:
            self._raw_data["protocol"]["sequence_number"] = value.__str__()
        else:
            self._raw_data["protocol"] = {"sequence_number": value.__str__()}

    @property
    def list_type(self) -> Optional[str]:
        return (
            self._raw_data["protocol"]["list_type"]
            if "protocol" in self._raw_data
            else None
        )

    @property
    def wkt(self) -> Optional[str]:
        """
        Well-known text representation of the recorded track
        :return: LINESTRING geometry, if a valid LINESTRING WKT is received, None otherwise
        """
        return (
            self._raw_data["protocol"]["wkt"]
            if "protocol" in self._raw_data
            and "wkt" in self._raw_data["protocol"]
            and "LINESTRING" in self._raw_data["protocol"]["wkt"]  # check if Linestring
            and ","
            in self._raw_data["protocol"][
                "wkt"
            ]  # check if Linestring contains 2 points
            else None
        )

    @property
    def id_waterbird_conditions(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_conditions" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_conditions"]) is dict:
                return self._raw_data["protocol"]["waterbird_conditions"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_conditions"].split(",")[0]
        return None

    @id_waterbird_conditions.setter
    def id_waterbird_conditions(self, value: str):
        if "protocol" in self._raw_data:
            self._raw_data["protocol"]["waterbird_conditions"] = {"@id": value}
        else:
            self._raw_data["protocol"] = {"waterbird_conditions": {"@id": value}}

    @property
    def id_waterbird_coverage(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_coverage" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_coverage"]) is dict:
                return self._raw_data["protocol"]["waterbird_coverage"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_coverage"].split(",")[0]
        return None

    @property
    def id_waterbird_optical(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_optical" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_optical"]) is dict:
                return self._raw_data["protocol"]["waterbird_optical"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_optical"].split(",")[0]
        return None

    @property
    def id_waterbird_countmethod(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_countmethod" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_countmethod"]) is dict:
                return self._raw_data["protocol"]["waterbird_countmethod"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_countmethod"].split(",")[0]
        return None

    @property
    def id_waterbird_ice(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_ice" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_ice"]) is dict:
                return self._raw_data["protocol"]["waterbird_ice"]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"]["waterbird_ice"].split(",")[0]
        return None

    @property
    def id_waterbird_snowcover(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_snowcover" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_snowcover"]) is dict:
                return self._raw_data["protocol"]["waterbird_snowcover"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_snowcover"].split(",")[0]
        return None

    @property
    def id_waterbird_waterlevel(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_waterlevel" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_waterlevel"]) is dict:
                return self._raw_data["protocol"]["waterbird_waterlevel"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_waterlevel"].split(",")[0]
        return None

    @property
    def id_waterbird_counttype(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_counttype" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_counttype"]) is dict:
                return self._raw_data["protocol"]["waterbird_counttype"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_counttype"].split(",")[0]
        return None

    @property
    def id_waterbird_visibility(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_visibility" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_visibility"]) is dict:
                return self._raw_data["protocol"]["waterbird_visibility"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_visibility"].split(",")[0]
        return None

    @property
    def id_waterbird_waves(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_waves" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_waves"]) is dict:
                return self._raw_data["protocol"]["waterbird_waves"]["@id"].split(",")[
                    0
                ]
            else:
                return self._raw_data["protocol"]["waterbird_waves"].split(",")[0]
        return None

    @property
    def id_waterbird_conditions_reason(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_conditions_reason" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_conditions_reason"]) is dict:
                return self._raw_data["protocol"]["waterbird_conditions_reason"][
                    "@id"
                ].split(",")[0]
            else:
                return self._raw_data["protocol"]["waterbird_conditions_reason"].split(
                    ","
                )[0]
        return None

    @property
    def id_waterbird_count_payed(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_count_payed" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_count_payed"]) is dict:
                return self._raw_data["protocol"]["waterbird_count_payed"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["waterbird_count_payed"].split(",")[0]
        return None

    @property
    def id_waterbird_activity_persons_on_shore(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_activity_persons_on_shore" in self._raw_data["protocol"]
        ):
            if (
                type(self._raw_data["protocol"]["waterbird_activity_persons_on_shore"])
                is dict
            ):
                return self._raw_data["protocol"][
                    "waterbird_activity_persons_on_shore"
                ]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"][
                    "waterbird_activity_persons_on_shore"
                ].split(",")[0]
        return None

    @property
    def id_waterbird_activity_boats_rowing(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_activity_boats_rowing" in self._raw_data["protocol"]
        ):
            if (
                type(self._raw_data["protocol"]["waterbird_activity_boats_rowing"])
                is dict
            ):
                return self._raw_data["protocol"]["waterbird_activity_boats_rowing"][
                    "@id"
                ].split(",")[0]
            else:
                return self._raw_data["protocol"][
                    "waterbird_activity_boats_rowing"
                ].split(",")[0]
        return None

    @property
    def id_waterbird_activity_boats_motor(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_activity_boats_motor" in self._raw_data["protocol"]
        ):
            if (
                type(self._raw_data["protocol"]["waterbird_activity_boats_motor"])
                is dict
            ):
                return self._raw_data["protocol"]["waterbird_activity_boats_motor"][
                    "@id"
                ].split(",")[0]
            else:
                return self._raw_data["protocol"][
                    "waterbird_activity_boats_motor"
                ].split(",")[0]
        return None

    @property
    def id_waterbird_activity_boats_sailing(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_activity_boats_sailing" in self._raw_data["protocol"]
        ):
            if (
                type(self._raw_data["protocol"]["waterbird_activity_boats_sailing"])
                is dict
            ):
                return self._raw_data["protocol"]["waterbird_activity_boats_sailing"][
                    "@id"
                ].split(",")[0]
            else:
                return self._raw_data["protocol"][
                    "waterbird_activity_boats_sailing"
                ].split(",")[0]
        return None

    @property
    def id_waterbird_activity_boats_kayak(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_activity_boats_kayak" in self._raw_data["protocol"]
        ):
            if (
                type(self._raw_data["protocol"]["waterbird_activity_boats_kayak"])
                is dict
            ):
                return self._raw_data["protocol"]["waterbird_activity_boats_kayak"][
                    "@id"
                ].split(",")[0]
            else:
                return self._raw_data["protocol"][
                    "waterbird_activity_boats_kayak"
                ].split(",")[0]
        return None

    @property
    def id_waterbird_activity_boats_fisherman(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_activity_boats_fisherman" in self._raw_data["protocol"]
        ):
            if (
                type(self._raw_data["protocol"]["waterbird_activity_boats_fisherman"])
                is dict
            ):
                return self._raw_data["protocol"]["waterbird_activity_boats_fisherman"][
                    "@id"
                ].split(",")[0]
            else:
                return self._raw_data["protocol"][
                    "waterbird_activity_boats_fisherman"
                ].split(",")[0]
        return None

    @property
    def id_waterbird_activity_divers(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_activity_divers" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_activity_divers"]) is dict:
                return self._raw_data["protocol"]["waterbird_activity_divers"][
                    "@id"
                ].split(",")[0]
            else:
                return self._raw_data["protocol"]["waterbird_activity_divers"].split(
                    ","
                )[0]
        return None

    @property
    def id_waterbird_activity_surfers(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "waterbird_activity_surfers" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["waterbird_activity_surfers"]) is dict:
                return self._raw_data["protocol"]["waterbird_activity_surfers"][
                    "@id"
                ].split(",")[0]
            else:
                return self._raw_data["protocol"]["waterbird_activity_surfers"].split(
                    ","
                )[0]
        return None

    @property
    def id_moving_harvest(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "moving_harvest" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["moving_harvest"]) is dict:
                return self._raw_data["protocol"]["moving_harvest"]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"]["moving_harvest"].split(",")[0]
        return None

    @property
    def id_coverage(self) -> Optional[str]:
        if "protocol" in self._raw_data and "coverage" in self._raw_data["protocol"]:
            if type(self._raw_data["protocol"]["coverage"]) is dict:
                return self._raw_data["protocol"]["coverage"]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"]["coverage"].split(",")[0]
        return None

    @property
    def id_condition(self) -> Optional[str]:
        if "protocol" in self._raw_data and "condition" in self._raw_data["protocol"]:
            if type(self._raw_data["protocol"]["condition"]) is dict:
                return self._raw_data["protocol"]["condition"]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"]["condition"].split(",")[0]
        return None

    @property
    def id_chiro_identify(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "chiro_identify" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["chiro_identify"]) is dict:
                return self._raw_data["protocol"]["chiro_identify"]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"]["chiro_identify"].split(",")[0]
        return None

    @property
    def id_additional_observer(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "additional_observer" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["additional_observer"]) is dict:
                return self._raw_data["protocol"]["additional_observer"]["@id"].split(
                    ","
                )[0]
            else:
                return self._raw_data["protocol"]["additional_observer"].split(",")[0]
        return None

    @property
    def id_changes(self) -> Optional[str]:
        if "protocol" in self._raw_data and "changes" in self._raw_data["protocol"]:
            if type(self._raw_data["protocol"]["changes"]) is dict:
                return self._raw_data["protocol"]["changes"]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"]["changes"].split(",")[0]
        return None

    @property
    def id_drone_used(self) -> Optional[str]:
        if "protocol" in self._raw_data and "drone_used" in self._raw_data["protocol"]:
            if type(self._raw_data["protocol"]["drone_used"]) is dict:
                return self._raw_data["protocol"]["drone_used"]["@id"].split(",")[0]
            else:
                return self._raw_data["protocol"]["drone_used"].split(",")[0]
        return None

    @property
    def id_tmp_water_bodies(self) -> Optional[str]:
        if (
            "protocol" in self._raw_data
            and "tmp_water_bodies" in self._raw_data["protocol"]
        ):
            if type(self._raw_data["protocol"]["tmp_water_bodies"]) is dict:
                return self._raw_data["protocol"]["tmp_water_bodies"]["@id"].split(",")[
                    0
                ]
            else:
                return self._raw_data["protocol"]["tmp_water_bodies"].split(",")[0]
        return None

    @property
    def playbacks(self) -> Optional[Dict[int, bool]]:
        if "protocol" in self._raw_data and "playback" in self._raw_data["protocol"]:
            species_ids: Dict[int, bool] = {}
            for key, value in self._raw_data["protocol"]["playback"].items():
                species_id = key.replace("Id_species_", "")
                species_ids[int(species_id)] = value == "1"
            return species_ids
        return None

    @property
    def observations(self) -> Optional[List[Observation]]:
        if "sightings" not in self._raw_data:
            self.refresh()
        if self._observations is None and "sightings" in self._raw_data:
            self._observations = [
                ornitho.model.observation.Observation.create_from_ornitho_json(
                    observation
                )
                for observation in self._raw_data["sightings"]
            ]

        return self._observations

    @observations.setter
    def observations(self, value: List[Observation]):
        for observation in value:
            if self._id_place is not None:
                observation.id_place = self._id_place
            else:
                self._id_place = observation.id_place
        self._raw_data["sightings"] = [observation._raw_data for observation in value]
        self._observations = value

    def playblack_played(self, species: Union[int, Species]) -> Optional[bool]:
        if isinstance(species, Species):
            species = int(species.id_) if species.id_ is not None else 0
        return (
            self.playbacks[species]
            if self.playbacks is not None and species in self.playbacks
            else None
        )

    @classmethod
    def create(  # type: ignore
        cls,
        time_start: time,
        time_stop: time,
        observations: List[Observation],
        protocol: Optional[Union[Protocol, str]] = None,
        comment: str = None,
        place: Optional[Union[Place, int]] = None,
        visit_number: Optional[int] = None,
        sequence_number: Optional[int] = None,
        full_form: bool = True,
        protocol_headers: Dict[str, Union[int, str]] = {},
        create_in_ornitho: bool = True,
    ) -> "Form":
        form = cls()
        form.time_start = time_start
        form.time_stop = time_stop
        form.full_form = full_form

        if comment is not None:
            form.comment = comment

        if place is not None:
            if isinstance(place, Place):
                form._id_place = place.id_
            else:
                form._id_place = place

        if protocol is not None:
            if isinstance(protocol, Protocol):
                form.protocol_name = protocol.name
            else:
                form.protocol_name = protocol
            for key, value in protocol_headers.items():
                if key.startswith("id_"):
                    form._raw_data["protocol"][key.lstrip("id_")] = {"@id": str(value)}
                else:
                    form._raw_data["protocol"][key] = value

        if visit_number is not None:
            form.visit_number = visit_number
        if sequence_number is not None:
            form.sequence_number = sequence_number

        if create_in_ornitho:
            # Form must be created first,
            # otherwise ornitho will ignore the given GUID/UUID for observations (╯°□°）╯︵ ┻━┻)

            # Create Form with an "Keine Art" observation, to create form in ornitho
            form.observations = [
                Observation.create(
                    observer=observations[0].id_observer,
                    species=10000,
                    place=place,
                    timing=observations[0].timing,
                    coord_lat=observations[0].coord_lat,
                    coord_lon=observations[0].coord_lon,
                    precision=observations[0].precision,
                    estimation_code=ornitho.EstimationCode.EXACT_VALUE,
                    count=0,
                    create_in_ornitho=False,
                )
            ]
            first_observation_id = cls.create_in_ornitho(
                data={"forms": [form.raw_data_trim_field_ids()]}
            )
            form_id = Observation.get(first_observation_id).id_form

            # Create observations with form id in ornitho
            try:
                # Add form id to every observation
                for observation in observations:
                    observation.id_form = form_id

                chunk_size = 32
                for observation_chunk in [
                    observations[i : i + chunk_size]
                    for i in range(0, len(observations), chunk_size)
                ]:
                    Observation.create_in_ornitho(
                        data={
                            "sightings": [
                                observation.raw_data_trim_field_ids()
                                for observation in observation_chunk
                            ]
                        }
                    )
                # Retrieve form again, to get acces to observation ids
                form = cls.get(form_id)
            except Exception as ex:
                form = cls(id_=form_id)
                form.delete()
                raise ex
        else:
            form.observations = observations
        return form

    def raw_data_trim_field_ids(self) -> Dict[str, Any]:
        raw_data = deepcopy(self._raw_data)
        if self.observations:
            trimmed_observations = [
                observation.raw_data_trim_field_ids()
                for observation in self.observations
            ]
            raw_data["sightings"] = trimmed_observations
        return raw_data
