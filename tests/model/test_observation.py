import uuid
from datetime import datetime, timedelta
from unittest import TestCase, mock
from unittest.mock import MagicMock

import pytz

import ornitho
from ornitho import (
    APIException,
    Detail,
    EstimationCode,
    ModificationType,
    Observation,
    Precision,
    Source,
)

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestObservation(TestCase):
    def setUp(self):
        self.observation_json = {
            "form": {"@id": "1", "full_form": "1"},
            "date": {"@notime": "1", "@offset": "3600", "@timestamp": "1573858800"},
            "species": {
                "@id": "94",
                "taxonomy": "1",
                "rarity": "common",
                "category": "B",
            },
            "place": {
                "@id": "779198",
                "id_universal": "28_43050307",
                "place_type": "place",
                "name": "Mohrbach-Aufstauung",
                "lat": "49.443127680501",
                "lon": "7.5751543757204",
                "loc_precision": "0",
            },
            "observers": [
                {
                    "@id": "10156",
                    "@uid": "53742",
                    "id_form": "1",
                    "traid": "10156",
                    "id_sighting": "43050307",
                    "id_universal": "28_43050307",
                    "guid": "2c789399-0939-41ea-ab12-01c00290e543",
                    "version": "0",
                    "timing": {
                        "@notime": "0",
                        "@offset": "3600",
                        "@timestamp": "1573899838",
                    },
                    "coord_lat": "49.443215",
                    "coord_lon": "7.574859",
                    "altitude": "233",
                    "precision": "precise",
                    "estimation_code": "EXACT_VALUE",
                    "count": "13",
                    "flight_number": "1",
                    "admin_hidden": "1",
                    "admin_hidden_type": "question",
                    "comment": "comment",
                    "hidden_comment": "hidden_comment",
                    "source": "WEB",
                    "insert_date": "1573995175",
                    "is_exported": "1",
                    "export_date": "1576641307",
                    "accuracy_of_location": {"@id": "2_1", "#text": "< 10 m"},
                    "resting_habitat": "1_5",
                    "observation_detail": "4_2",
                    "details": [
                        {"count": "1", "sex": "U", "age": "PULL"},
                        {"count": "12", "sex": "M", "age": "AD"},
                    ],
                    "atlas_code": {"@id": "3_3", "#text": "A2"},
                    "project": 1,
                    "extended_info": {
                        "colony": {
                            "couples": "3",
                            "nests": "18",
                            "nests_is_min": "1",
                            "occupied_nests": "2",
                        },
                        "colony_extended": {
                            "couples": "2",
                            "nb_natural_nests": "1",
                            "nb_artificial_nests": "17",
                            "nb_natural_occup_nests": "0",
                            "nb_artificial_occup_nests": "2",
                            "nb_natural_other_species_nests": "0",
                            "nb_artificial_other_species_nests": "0",
                            "nb_natural_destructed_nests": "1",
                            "nb_artificial_destructed_nests": "0",
                            "nb_construction_nests": "0",
                        },
                    },
                }
            ],
        }
        self.observation = Observation.create_from_ornitho_json(self.observation_json)

    def test_create_from(self):
        observation = Observation.create_from_ornitho_json(self.observation_json)
        self.assertEqual(43050307, observation.id_)
        self.assertEqual(self.observation_json, observation._raw_data)

        # Test Exception
        self.assertRaises(
            APIException,
            lambda: Observation.create_from_ornitho_json({"observers": ["1", "2"]}),
        )

    def test_id_observer(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["@id"]),
            self.observation.id_observer,
        )

        obs = Observation()
        obs._raw_data = {"observers": [{"id": 2}]}
        self.assertEqual(2, obs.id_observer)

        obs = Observation()
        obs.id_observer = 3
        self.assertEqual(3, obs.id_observer)

    def test_traid(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["traid"]), self.observation.traid
        )

    def test_guid(self):
        self.assertEqual(
            uuid.UUID(self.observation_json["observers"][0]["guid"]),
            self.observation.guid,
        )

        obs = Observation()
        guid = uuid.uuid4()
        obs.guid = guid
        self.assertEqual(guid, obs.guid)

        guid2 = uuid.uuid4()
        obs.guid = guid2
        self.assertEqual(guid2, obs.guid)

    def test_timing(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.observation_json["observers"][0]["timing"]["@timestamp"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.observation.timing,
        )

        obs = Observation()
        now = datetime.now().replace(microsecond=0)
        obs.timing = now
        self.assertEqual(now.astimezone(), obs.timing)
        now2 = datetime.now().replace(microsecond=0).astimezone()
        obs.timing = now2
        self.assertEqual(now2, obs.timing)

    def test_coord_lat(self):
        self.assertEqual(
            float(self.observation_json["observers"][0]["coord_lat"]),
            self.observation.coord_lat,
        )

        obs = Observation()
        coord_lat = 1.23
        obs.coord_lat = coord_lat
        self.assertEqual(coord_lat, obs.coord_lat)
        coord_lat2 = 2.34
        obs.coord_lat = coord_lat2
        self.assertEqual(coord_lat2, obs.coord_lat)

    def test_coord_lon(self):
        self.assertEqual(
            float(self.observation_json["observers"][0]["coord_lon"]),
            self.observation.coord_lon,
        )

        obs = Observation()
        coord_lon = 1.23
        obs.coord_lon = coord_lon
        self.assertEqual(coord_lon, obs.coord_lon)
        coord_lon2 = 2.34
        obs.coord_lon = coord_lon2
        self.assertEqual(coord_lon2, obs.coord_lon)

    def test_altitude(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["altitude"]),
            self.observation.altitude,
        )

        obs = Observation()
        altitude = 1
        obs.altitude = altitude
        self.assertEqual(altitude, obs.altitude)
        altitude2 = 2
        obs.altitude = altitude2
        self.assertEqual(altitude2, obs.altitude)

    def test_id_form(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["id_form"]),
            self.observation.id_form,
        )
        obs = Observation()
        id_form = 1
        obs.id_form = id_form
        self.assertEqual(id_form, obs.id_form)
        id_form2 = 2
        obs.id_form = id_form2
        self.assertEqual(id_form2, obs.id_form)

    def test_precision(self):
        self.assertEqual(
            Precision(self.observation_json["observers"][0]["precision"]),
            self.observation.precision,
        )

        obs = Observation()
        precision = Precision.PRECISE
        obs.precision = precision
        self.assertEqual(precision, obs.precision)
        precision2 = Precision.PLACE
        obs.precision = precision2
        self.assertEqual(precision2, obs.precision)

    def test_estimation_code(self):
        self.assertEqual(
            EstimationCode(self.observation_json["observers"][0]["estimation_code"]),
            self.observation.estimation_code,
        )

        obs = Observation()
        estimation_code = EstimationCode.EXACT_VALUE
        obs.estimation_code = estimation_code
        self.assertEqual(estimation_code, obs.estimation_code)
        estimation_code2 = EstimationCode.ESTIMATION
        obs.estimation_code = estimation_code2
        self.assertEqual(estimation_code2, obs.estimation_code)

    def test_id_species(self):
        self.assertEqual(
            int(self.observation_json["species"]["@id"]), self.observation.id_species
        )

        obs = Observation()
        obs._raw_data = {"species": {"id": 1}}
        self.assertEqual(1, obs.id_species)

        obs.id_species = 2
        self.assertEqual(2, obs.id_species)

    def test_count(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["count"]), self.observation.count
        )

        obs = Observation()
        count = 1
        obs.count = count
        self.assertEqual(count, obs.count)
        count2 = 2
        obs.count = count2
        self.assertEqual(count2, obs.count)

    def test_flight_number(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["flight_number"]),
            self.observation.flight_number,
        )

    def test_admin_hidden(self):
        self.assertTrue(
            self.observation.admin_hidden,
        )

    def test_admin_hidden_type(self):
        self.assertEqual(
            self.observation_json["observers"][0]["admin_hidden_type"],
            self.observation.admin_hidden_type,
        )

    def test_source(self):
        self.assertEqual(
            Source(self.observation_json["observers"][0]["source"]),
            self.observation.source,
        )

    @mock.patch("ornitho.model.observation.Media")
    def test_medias(self, mock_media):
        mock_media.get.return_value = "Media retrieved"

        self.assertIsNone(self.observation.medias)

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "medias": [
                        {
                            "@id": "111111",
                        },
                        {
                            "@id": "2222222",
                        },
                    ],
                }
            ]
        }
        obs = Observation.create_from_ornitho_json(obs_json)
        medias = obs.medias
        self.assertIsNotNone(medias)
        self.assertEqual(len(obs_json["observers"][0]["medias"]), len(medias))
        mock_media.get.assert_called_with(obs_json["observers"][0]["medias"][1]["@id"])

    def test_media_urls(self):
        self.assertIsNone(self.observation.media_urls)

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "medias": [
                        {
                            "@id": "111111",
                            "path": "https://test.media/www.ornitho.de/1970-01",
                            "filename": "file1.jpg",
                        },
                        {
                            "@id": "2222222",
                            "path": "https://test.media/www.ornitho.de/1970-01",
                            "filename": "file2.jpg",
                        },
                    ],
                }
            ]
        }
        obs = Observation.create_from_ornitho_json(obs_json)
        media_urls = obs.media_urls
        self.assertIsNotNone(media_urls)
        self.assertEqual(len(obs_json["observers"][0]["medias"]), len(media_urls))
        self.assertEqual(
            f"{obs_json['observers'][0]['medias'][0]['path']}/{obs_json['observers'][0]['medias'][0]['filename']}",
            media_urls[0],
        )
        self.assertEqual(
            f"{obs_json['observers'][0]['medias'][1]['path']}/{obs_json['observers'][0]['medias'][1]['filename']}",
            media_urls[1],
        )

    def test_comment(self):
        self.assertEqual(
            self.observation_json["observers"][0]["comment"],
            self.observation.comment,
        )

        obs = Observation()
        comment = "comment"
        obs.comment = comment
        self.assertEqual(comment, obs.comment)
        comment2 = "comment2"
        obs.comment = comment2
        self.assertEqual(comment2, obs.comment)

    def test_hidden_comment(self):
        self.assertEqual(
            self.observation_json["observers"][0]["hidden_comment"],
            self.observation.hidden_comment,
        )

        obs = Observation()
        hidden_comment = "hidden_comment"
        obs.hidden_comment = hidden_comment
        self.assertEqual(hidden_comment, obs.hidden_comment)
        hidden_comment2 = "hidden_comment2"
        obs.hidden_comment = hidden_comment2
        self.assertEqual(hidden_comment2, obs.hidden_comment)

    def test_hidden(self):
        self.assertFalse(self.observation.hidden)

        obs = Observation()
        hidden = True
        obs.hidden = hidden
        self.assertTrue(obs.hidden)
        hidden2 = False
        obs.hidden = hidden2
        self.assertFalse(obs.hidden_comment)

    def test_id_atlas_code(self):
        self.assertEqual(
            self.observation_json["observers"][0]["atlas_code"]["@id"],
            self.observation.id_atlas_code,
        )

        obs = Observation()
        obs.id_atlas_code = "3_1"
        self.assertEqual("3_1", obs.id_atlas_code)

        obs.id_atlas_code = "3_2"
        self.assertEqual("3_2", obs.id_atlas_code)

    def test_atlas_code_text(self):
        self.assertEqual(
            self.observation_json["observers"][0]["atlas_code"]["#text"],
            self.observation.atlas_code_text,
        )

    def test_details(self):
        details = [Detail(1, "U", "PULL"), Detail(12, "M", "AD")]
        self.assertEqual(details, self.observation.details)

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "details": [
                        {
                            "count": "1",
                            "sex": {"@id": "U", "#text": "unbekannt"},
                            "age": {"@id": "PULL", "#text": "Pullus / nicht-flügge"},
                        },
                        {
                            "count": "12",
                            "sex": {"@id": "M", "#text": "Männchen"},
                            "age": {"@id": "AD", "#text": "adult"},
                        },
                    ],
                }
            ]
        }
        self.assertEqual(
            details, Observation.create_from_ornitho_json(obs_json).details
        )

        obs = Observation()
        obs.details = details
        self.assertEqual(details, obs.details)
        details2 = [Detail(1, "U", "PULL"), Detail(12, "M", "AD"), Detail(4, "F", "AD")]
        obs.details = details2
        self.assertEqual(details2, obs.details)

    def test_insert_date(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.observation_json["observers"][0]["insert_date"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.observation.insert_date,
        )

    def test_update_date(self):
        self.assertEqual(None, self.observation.update_date)

    def test_id_place(self):
        self.assertEqual(
            int(self.observation_json["place"]["@id"]), self.observation.id_place
        )

        obs_json = {"place": {"id": 1}, "observers": [{}]}
        self.assertEqual(1, Observation.create_from_ornitho_json(obs_json).id_place)

        with mock.patch("ornitho.model.observation.Place") as mock_place:
            obs_json = {
                "observers": [
                    {
                        "coord_lat": "49.443215",
                        "coord_lon": "7.574859",
                    }
                ]
            }
            mock_place.id_.return_value = 1
            mock_place._raw_data.return_value = {"id": 1}
            mock_place.find_closest_place.return_value = mock_place
            self.assertEqual(
                1,
                Observation.create_from_ornitho_json(obs_json).id_place,
            )

    def test_id_accuracy_of_location(self):
        self.assertEqual(
            self.observation_json["observers"][0]["accuracy_of_location"]["@id"],
            self.observation.id_accuracy_of_location,
        )

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                }
            ]
        }
        self.assertIsNone(
            Observation.create_from_ornitho_json(obs_json).id_accuracy_of_location
        )

    def test_id_resting_habitat(self):
        self.assertEqual(
            self.observation_json["observers"][0]["resting_habitat"],
            self.observation.id_resting_habitat,
        )

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "resting_habitat": {"@id": "1_5", "#text": "Grünland"},
                }
            ]
        }
        self.assertEqual(
            obs_json["observers"][0]["resting_habitat"]["@id"],
            Observation.create_from_ornitho_json(obs_json).id_resting_habitat,
        )

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                }
            ]
        }
        self.assertIsNone(
            Observation.create_from_ornitho_json(obs_json).id_resting_habitat
        )

        obs = Observation()
        obs.id_resting_habitat = "1_1"
        self.assertEqual("1_1", obs.id_resting_habitat)

        obs.id_resting_habitat = "2_2"
        self.assertEqual("2_2", obs.id_resting_habitat)

    def test_id_observation_detail(self):
        self.assertEqual(
            self.observation_json["observers"][0]["observation_detail"],
            self.observation.id_observation_detail,
        )

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "observation_detail": {"@id": "4_2", "#text": "Nahrung suchend"},
                }
            ]
        }
        self.assertEqual(
            obs_json["observers"][0]["observation_detail"]["@id"],
            Observation.create_from_ornitho_json(obs_json).id_observation_detail,
        )

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                }
            ]
        }
        self.assertIsNone(
            Observation.create_from_ornitho_json(obs_json).id_observation_detail
        )

        obs = Observation()
        obs.id_observation_detail = "4_1"
        self.assertEqual("4_1", obs.id_observation_detail)

        obs.id_observation_detail = "4_2"
        self.assertEqual("4_2", obs.id_observation_detail)

    def test_species(self):
        species = self.observation.species
        self.assertEqual(species._raw_data, self.observation_json["species"])

        with mock.patch("ornitho.model.observation.Species") as mock_species:
            mock_species.id_.return_value = 1
            mock_species._raw_data.return_value = {"id": 1}
            mock_species.get.return_value = mock_species

            obs = Observation()
            obs.species = mock_species.get(1)
            self.assertEqual(mock_species.get.return_value, obs.species)

            obs2 = Observation()
            obs2._raw_data = {"species": {"id": 2}}
            self.assertEqual(mock_species.get.return_value, obs2.species)
            mock_species.get.assert_called_with(2)

    def test_observer(self):
        observer = self.observation.observer
        self.assertEqual(observer._raw_data, self.observation_json["observers"][0])

        with mock.patch("ornitho.model.observation.Observer") as mock_observer:
            mock_observer.id_.return_value = 1
            mock_observer._raw_data.return_value = {"id": 1}
            mock_observer.get.return_value = mock_observer

            obs = Observation()
            obs.observer = mock_observer
            self.assertEqual(mock_observer.get.return_value, obs.observer)

    def test_place(self):
        place = self.observation.place
        self.assertEqual(place._raw_data, self.observation_json["place"])

        with mock.patch("ornitho.model.observation.Place") as mock_place:
            mock_place.get.return_value = "Place"
            mock_place.id_.return_value = "1"
            obs = Observation()
            obs.place = mock_place
            self.assertEqual(mock_place.id_, obs.place.id_)

    def test_form(self):
        form = self.observation.form
        self.assertEqual(form._raw_data, self.observation_json["form"])

    @mock.patch("ornitho.model.observation.FieldOption")
    def test_accuracy_of_location(self, mock_field_option):
        mock_field_option.get.return_value = "accuracy_of_location retrieved"
        mock_field_option.id_.return_value = "2_1"

        accuracy_of_location = self.observation.accuracy_of_location
        mock_field_option.get.assert_called_with(
            self.observation.id_accuracy_of_location
        )
        self.assertEqual(accuracy_of_location, "accuracy_of_location retrieved")

    @mock.patch("ornitho.model.observation.FieldOption")
    def test_resting_habitat(self, mock_field_option):
        mock_field_option.get.return_value = "Resting habitat retrieved"
        mock_field_option.id_.return_value = "1_1"

        resting_habitat = self.observation.resting_habitat
        mock_field_option.get.assert_called_with(self.observation.id_resting_habitat)
        self.assertEqual(resting_habitat, "Resting habitat retrieved")

        obs = Observation()
        obs.resting_habitat = mock_field_option
        self.assertEqual(mock_field_option.id_, obs.resting_habitat.id_)

    @mock.patch("ornitho.model.observation.FieldOption")
    def test_observation_detail(self, mock_field_option):
        mock_field_option.get.return_value = "Observation Detail retrieved"
        mock_field_option.id_.return_value = "4_1"

        observation_detail = self.observation.observation_detail
        mock_field_option.get.assert_called_with(self.observation.id_observation_detail)
        self.assertEqual(observation_detail, "Observation Detail retrieved")

        obs = Observation()
        obs.observation_detail = mock_field_option
        self.assertEqual(mock_field_option.id_, obs.observation_detail.id_)

    @mock.patch("ornitho.model.observation.FieldOption")
    def test_atlas_code(self, mock_field_option):
        mock_field_option.get.return_value = "Atlas Code retrieved"
        mock_field_option.id_.return_value = "2"

        atlas_code = self.observation.atlas_code
        mock_field_option.get.assert_called_with(f"3_{self.observation.id_atlas_code}")
        self.assertEqual(atlas_code, "Atlas Code retrieved")

        obs = Observation()
        obs.atlas_code = mock_field_option
        self.assertEqual(mock_field_option.id_, obs.atlas_code.id_)

    def test_is_exported(self):
        self.assertTrue(self.observation.is_exported)
        self.observation.is_exported = False
        self.assertFalse(self.observation.is_exported)
        self.observation.is_exported = True
        self.assertTrue(self.observation.is_exported)

        observation = Observation()
        self.assertFalse(observation.is_exported)
        observation.is_exported = True
        self.assertTrue(observation.is_exported)

    def test_export_date(self):
        self.observation.is_exported = False
        self.assertIsNone(self.observation.export_date)
        now = datetime.now().astimezone().replace(microsecond=0)
        self.observation.is_exported = True
        self.observation.export_date = now
        self.assertEqual(now, self.observation.export_date)

        observation = Observation()
        observation.export_date = now
        observation.is_exported = True
        self.assertEqual(now, observation.export_date)

    def test_notime(self):
        self.assertFalse(self.observation.notime)
        self.observation.notime = True
        self.assertTrue(self.observation.notime)

        observation = Observation()
        observation.notime = True
        self.assertTrue(observation.notime)

        observation = Observation.create_from_ornitho_json(
            {"observers": [{"id_sighting": 42}]}
        )
        observation.notime = True
        self.assertTrue(observation.notime)

    def test_project(self):
        self.assertEqual(1, self.observation.project)

    def test_project_code(self):
        self.assertIsNone(self.observation.project_code)

    def test_cavs(self):
        self.assertIsNone(self.observation.cavs)

    def test_id_observer_vowa(self):
        self.assertIsNone(self.observation.id_observer_vowa)

    def test_second_hand(self):
        self.assertFalse(self.observation.second_hand)

    def test_colony_couples(self):
        self.assertEqual(3, self.observation.colony_couples)

    def test_colony_nests(self):
        self.assertEqual(18, self.observation.colony_nests)

    def test_colony_occupied_nests(self):
        self.assertEqual(2, self.observation.colony_occupied_nests)

    def test_colony_nests_is_min(self):
        self.assertTrue(self.observation.colony_nests_is_min)

    def test_colony_extended_couples(self):
        self.assertEqual(2, self.observation.colony_extended_couples)

    def test_colony_extended_nb_natural_nests(self):
        self.assertEqual(1, self.observation.colony_extended_nb_natural_nests)

    def test_colony_extended_nb_natural_nests_is_min(self):
        self.assertFalse(self.observation.colony_extended_nb_natural_nests_is_min)

    def test_colony_extended_nb_artificial_nests(self):
        self.assertEqual(17, self.observation.colony_extended_nb_artificial_nests)

    def test_colony_extended_nb_artificial_nests_is_min(self):
        self.assertFalse(self.observation.colony_extended_nb_artificial_nests_is_min)

    def test_colony_extended_nb_natural_occup_nests(self):
        self.assertEqual(0, self.observation.colony_extended_nb_natural_occup_nests)

    def test_colony_extended_nb_artificial_occup_nests(self):
        self.assertEqual(2, self.observation.colony_extended_nb_artificial_occup_nests)

    def test_colony_extended_nb_natural_other_species_nests(self):
        self.assertEqual(
            0, self.observation.colony_extended_nb_natural_other_species_nests
        )

    def test_colony_extended_nb_artificial_other_species_nests(self):
        self.assertEqual(
            0, self.observation.colony_extended_nb_artificial_other_species_nests
        )

    def test_colony_extended_nb_natural_destructed_nests(self):
        self.assertEqual(
            1, self.observation.colony_extended_nb_natural_destructed_nests
        )

    def test_colony_extended_nb_artificial_destructed_nests(self):
        self.assertEqual(
            0, self.observation.colony_extended_nb_artificial_destructed_nests
        )

    def test_colony_extended_nb_construction_nests(self):
        self.assertEqual(0, self.observation.colony_extended_nb_construction_nests)

    def test_by_observer(self):
        Observation.list = MagicMock(return_value=["obs", "pk"])
        Observation.by_observer(id_observer=1)
        Observation.list.assert_called_with(
            request_all=False, pagination_key=None, short_version=False, id_observer=1
        )

    def test_by_observer_all(self):
        Observation.list_all = MagicMock(return_value=["obs", "pk"])
        Observation.by_observer_all(id_observer=1)
        Observation.list_all.assert_called_with(id_observer=1, short_version=False)

    def test_diff(self):
        Observation.request = MagicMock(
            return_value=[
                {
                    "id_sighting": "1",
                    "id_universal": "1",
                    "modification_type": "updated",
                },
                {
                    "id_sighting": "2",
                    "id_universal": "2",
                    "modification_type": "deleted",
                },
            ]
        )

        # Case 1: without retrieving
        date = datetime.now() - timedelta(hours=1)
        observations = Observation.diff(
            date,
            modification_type=ModificationType.ALL,
            id_taxo_group=1,
            only_protocol="CBBM",
            only_form=True,
        )
        self.assertEqual(len(observations), 2)
        Observation.request.assert_called_with(
            method="get",
            url="observations/diff",
            params={
                "date": date.replace(microsecond=0).isoformat(),
                "modification_type": ModificationType.ALL.value,
                "id_taxo_group": "1",
                "only_protocol": "CBBM",
                "only_form": "1",
            },
        )

        # Case 2: with retrieving

        mock_protocol = MagicMock(spec=ornitho.Protocol)
        type(mock_protocol).name = mock.PropertyMock(return_value="CBBM-Mock")
        Observation.get = MagicMock(return_value=self.observation)
        date = datetime.now().astimezone(pytz.timezone("Asia/Tokyo")) - timedelta(
            hours=1
        )
        observations = Observation.diff(
            date, only_protocol=mock_protocol, retrieve_observations=True
        )
        self.assertEqual(len(observations), 2)
        self.assertEqual(observations[0], self.observation)
        Observation.request.assert_called_with(
            method="get",
            url="observations/diff",
            params={
                "date": date.replace(microsecond=0)
                .astimezone(datetime.now().astimezone().tzinfo)
                .replace(tzinfo=None)
                .isoformat(),
                "only_protocol": "CBBM-Mock",
            },
        )

    @mock.patch("ornitho.model.observation.CreateableModel.create_in_ornitho")
    def test_create(self, mock_createable_model):
        mock_createable_model.return_value = 1
        mock_detail = mock.Mock(spec=Detail)
        mock_detail.count = 1
        mock_detail.sex = "F"
        mock_detail.age = "AD"

        obs = Observation.create(
            observer=1,
            species=1,
            timing=datetime.now(),
            coord_lat=1.23,
            coord_lon=4.56,
            altitude=1,
            precision=Precision.PRECISE,
            estimation_code=EstimationCode.EXACT_VALUE,
            count=2,
            comment="TEST",
            hidden_comment="HIDDEN TEST",
            hidden=True,
            atlas_code="3_2",
            details=[mock_detail],
            resting_habitat="1_1",
            observation_detail="4_1",
        )
        mock_createable_model.assert_called()
        self.assertEqual(1, obs.id_)
        self.assertEqual(1, obs.observer.id_)
        self.assertEqual(1, obs.species.id_)
        self.assertEqual(1.23, obs.coord_lat)
        self.assertEqual(4.56, obs.coord_lon)
        self.assertEqual(1, obs.altitude)
        self.assertEqual(2, obs.count)
        self.assertEqual("TEST", obs.comment)
        self.assertEqual("HIDDEN TEST", obs.hidden_comment)
        self.assertTrue(obs.hidden)
        self.assertEqual([mock_detail], obs.details)

        mock_createable_model.return_value = 2
        mock_observer = mock.Mock(spec=ornitho.Observer)
        mock_observer.id_ = 2
        mock_species = mock.Mock(spec=ornitho.Species)
        mock_species.id_ = 2
        mock_atlas_code = mock.Mock(spec=ornitho.FieldOption)
        mock_atlas_code.id_ = "3_4"
        mock_resting_habitat = mock.Mock(spec=ornitho.FieldOption)
        mock_resting_habitat.id_ = "1_4"
        mock_observation_detail = mock.Mock(spec=ornitho.FieldOption)
        mock_observation_detail.id_ = "4_4"

        obs2 = Observation.create(
            observer=mock_observer,
            species=mock_species,
            guid=uuid.uuid4(),
            timing=datetime.now(),
            place=1,
            coord_lat=1.23,
            coord_lon=4.56,
            altitude=1,
            precision=Precision.PRECISE,
            estimation_code=EstimationCode.EXACT_VALUE,
            count=2,
            comment="TEST",
            hidden_comment="HIDDEN TEST",
            hidden=True,
            atlas_code=mock_atlas_code,
            resting_habitat=mock_resting_habitat,
            observation_detail=mock_observation_detail,
        )
        mock_createable_model.assert_called()
        self.assertEqual(2, obs2.id_)
        self.assertEqual(2, obs2.observer.id_)
        self.assertEqual(2, obs2.species.id_)
        self.assertEqual(Precision.PRECISE, obs2.precision)
        self.assertEqual(EstimationCode.EXACT_VALUE, obs2.estimation_code)
        self.assertEqual("3_4", obs2.atlas_code.id_)
        self.assertEqual("1_4", obs2.resting_habitat.id_)
        self.assertEqual("4_4", obs2.observation_detail.id_)
        self.assertEqual(1, obs2.id_place)

        mock_place = mock.Mock(spec=ornitho.Place)
        mock_place.id_ = 2
        mock_place._raw_data = {"id": 2}
        obs3 = Observation.create(
            observer=mock_observer,
            species=mock_species,
            guid=uuid.uuid4(),
            timing=datetime.now(),
            id_form=1,
            place=mock_place,
            coord_lat=1.23,
            coord_lon=4.56,
            altitude=1,
            precision=Precision.PRECISE,
            estimation_code=EstimationCode.EXACT_VALUE,
            count=2,
            comment="TEST",
            hidden_comment="HIDDEN TEST",
            hidden=True,
            atlas_code=mock_atlas_code,
            resting_habitat=mock_resting_habitat,
            observation_detail=mock_observation_detail,
        )
        mock_createable_model.assert_called()
        self.assertEqual(2, obs3.id_)
        self.assertEqual(2, obs3.observer.id_)
        self.assertEqual(2, obs3.species.id_)
        self.assertEqual(Precision.PRECISE, obs3.precision)
        self.assertEqual(EstimationCode.EXACT_VALUE, obs3.estimation_code)
        self.assertEqual("3_4", obs3.atlas_code.id_)
        self.assertEqual("1_4", obs3.resting_habitat.id_)
        self.assertEqual("4_4", obs3.observation_detail.id_)
        self.assertEqual(1, obs3.id_form)
        self.assertEqual(2, obs3.place.id_)

    @mock.patch("ornitho.model.observation.BaseModel.refresh")
    @mock.patch("ornitho.model.observation.UpdateableModel.update")
    def test_mark_as_exported(self, mock_updateable_model, mock_base_model):
        self.observation.mark_as_exported()
        mock_updateable_model.assert_called_once()
        self.observation.mark_as_exported(datetime.now())
        mock_updateable_model.assert_called()
        self.assertEqual(2, mock_updateable_model.call_count)

        obs = Observation()
        obs.mark_as_exported()
        mock_base_model.assert_called_once()
