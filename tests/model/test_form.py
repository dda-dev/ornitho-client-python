from datetime import date, datetime
from unittest import TestCase, mock
from unittest.mock import MagicMock

import ornitho
from ornitho import Form, Place, Protocol
from ornitho.api_exception import APIException

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestForm(TestCase):
    def setUp(self):
        self.form_json = {
            "@id": "446171",
            "id_form_universal": "28_446171",
            "time_start": "09:06:00",
            "time_stop": "09:31:00",
            "full_form": "1",
            "version": "0",
            "lat": "52.532542",
            "lon": "13.257572",
            "id_form_mobile": "40232_1583395608201_1",
            "comment": "Begehung 3, 7 Grad , heiter",
            "protocol": {
                "protocol_name": "CBBM",
                "site_code": "DDA-1-Test",
                "local_site_code": "",
                "advanced": "0",
                "visit_number": "158",
                "sequence_number": "1",
                "list_type": "-",
                "waterbird_conditions": "GOOD_NORMAL",
                "waterbird_coverage": "COMPLETE",
                "waterbird_optical": "TELESCOPE",
                "waterbird_countmethod": "GROUND",
                "waterbird_ice": "NO_ICE",
                "waterbird_waterlevel": "NO_SNOW",
                "waterbird_snowcover": "NO_SNOW",
                "waterbird_counttype": "NORMAL",
                "waterbird_visibility": "NORMAL",
                "waterbird_waves": "NORMAL",
                "waterbird_conditions_reason": "NORMAL",
                "waterbird_count_payed": "NORMAL",
                "waterbird_activity_persons_on_shore": "NORMAL",
                "waterbird_activity_boats_rowing": "NORMAL",
                "waterbird_activity_boats_motor": "NORMAL",
                "waterbird_activity_boats_sailing": "NORMAL",
                "waterbird_activity_boats_kayak": "NORMAL",
                "waterbird_activity_boats_fisherman": "NORMAL",
                "waterbird_activity_divers": "NORMAL",
                "waterbird_activity_surfers": "NORMAL",
                "moving_harvest": "NORMAL",
                "coverage": "NORMAL",
                "condition": "NORMAL",
                "chiro_identify": "NORMAL",
                "additional_observer": "NORMAL",
                "changes": "NORMAL",
                "drone_used": "NORMAL",
                "tmp_water_bodies": "NORMAL",
                "nest_number": "11",
                "occupied_nest_number": "12",
            },
            "sightings": [
                {
                    "date": {
                        "@notime": "1",
                        "@offset": "3600",
                        "@timestamp": "1583362800",
                    },
                    "species": {
                        "@id": "385",
                        "taxonomy": "1",
                        "rarity": "verycommon",
                        "category": "C",
                    },
                    "place": {
                        "@id": "822442",
                        "id_universal": "28_45114715",
                        "place_type": "transect",
                        "name": "DDA-Teststrecke Münster",
                        "lat": "51.99666467623097",
                        "lon": "7.6341611553058595",
                        "loc_precision": "0",
                    },
                    "observers": [
                        {
                            "@id": "3277",
                            "@uid": "40232",
                            "traid": "3277",
                            "id_sighting": "45114715",
                            "id_universal": "28_45114715",
                            "guid": "c97731f4-5ebb-41ea-805a-01c002b0655b",
                            "version": "0",
                            "timing": {
                                "@notime": "0",
                                "@offset": "3600",
                                "@timestamp": "1583396828",
                            },
                            "coord_lat": "52.532542",
                            "coord_lon": "13.257572",
                            "altitude": "32",
                            "id_form": "446171",
                            "id_form_universal": "28_446171",
                            "precision": "transect_precise",
                            "estimation_code": "EXACT_VALUE",
                            "count": "1",
                            "flight_number": "1",
                            "hidden": "1",
                            "source": "WEB",
                            "insert_date": "1583397121",
                            "atlas_code": "3",
                        }
                    ],
                },
            ],
        }
        self.form = Form.create_from_ornitho_json(self.form_json)

    def test_instance_url(self):
        self.assertEqual("observations/search", self.form.instance_url())

    @mock.patch("ornitho.model.form.APIRequester")
    def test_refresh(self, mock_requester):
        class MockRequesterClass:
            def request_raw(self, method, url, short_version, body):
                return {"data": {"forms": [{"time_start": "01:01:01"}]}}, None

        def enter_requester(requester):
            return MockRequesterClass()

        mock_requester.return_value.__enter__ = enter_requester
        form = self.form.refresh()
        self.assertEqual("01:01:01", form.time_start.strftime("%H:%M:%S"))

    @mock.patch("ornitho.model.form.APIRequester")
    def test_refresh_exception(self, mock_requester):
        class MockRequesterClass:
            def request_raw(self, method, url, short_version, body):
                return {"data": {"WRONG": [{"time_start": "NEW"}]}}, None

        def enter_requester(requester):
            return MockRequesterClass()

        mock_requester.return_value.__enter__ = enter_requester
        self.assertRaises(
            APIException,
            lambda: self.form.refresh(),
        )

    def test_id_form_universal(self):
        self.assertEqual(
            self.form_json["id_form_universal"],
            self.form.id_form_universal,
        )

    def test_day(self):
        form_json = {
            "@id": "1",
            "day": {"@timestamp": "1583396828"},
        }
        self.assertEqual(
            date.fromtimestamp(
                int(self.form_json["sightings"][0]["date"]["@timestamp"])
            ),
            Form.create_from_ornitho_json(form_json).day,
        )

        self.assertEqual(
            date.fromtimestamp(
                int(self.form_json["sightings"][0]["date"]["@timestamp"])
            ),
            self.form.day,
        )

        with mock.patch("ornitho.model.Form.refresh") as mock_refresh:
            self.assertIsNone(Form().day)
            mock_refresh.assert_called_once()

    def test_time_start(self):
        self.assertEqual(
            self.form_json["time_start"],
            self.form.time_start.strftime("%H:%M:%S"),
        )
        new_time = datetime.now().time()
        self.form.time_start = new_time
        self.assertEqual(
            new_time.replace(microsecond=0),
            self.form.time_start,
        )

    def test_time_stop(self):
        self.assertEqual(
            self.form_json["time_stop"],
            self.form.time_stop.strftime("%H:%M:%S"),
        )
        new_time = datetime.now().time()
        self.form.time_stop = new_time
        self.assertEqual(
            new_time.replace(microsecond=0),
            self.form.time_stop,
        )

    def test_full_form(self):
        self.assertEqual(
            False if self.form_json["full_form"] == "0" else True, self.form.full_form
        )
        self.form.full_form = True
        self.assertTrue(self.form.full_form)
        self.form.full_form = False
        self.assertFalse(self.form.full_form)

    def test_version(self):
        self.assertEqual(
            int(self.form_json["version"]),
            self.form.version,
        )

    def test_lat(self):
        self.assertEqual(
            float(self.form_json["lat"]),
            self.form.lat,
        )

    def test_lon(self):
        self.assertEqual(
            float(self.form_json["lon"]),
            self.form.lon,
        )

    def test_id_form_mobile(self):
        self.assertEqual(
            self.form_json["id_form_mobile"],
            self.form.id_form_mobile,
        )

    def test_comment(self):
        self.assertEqual(
            self.form_json["comment"],
            self.form.comment,
        )

    def test_protocol_name(self):
        self.assertEqual(
            self.form_json["protocol"]["protocol_name"],
            self.form.protocol_name,
        )

        self.form.protocol_name = "NEW_PROTOCOL"
        self.assertEqual("NEW_PROTOCOL", self.form.protocol_name)

        new_form = Form()
        new_form.protocol_name = "NEW_PROTOCOL_2"
        self.assertEqual("NEW_PROTOCOL_2", new_form.protocol_name)

    def test_site_code(self):
        self.assertEqual(
            self.form_json["protocol"]["site_code"],
            self.form.site_code,
        )

        self.form.site_code = "SITE_CODE"
        self.assertEqual("SITE_CODE", self.form.site_code)

        new_form = Form()
        new_form.site_code = "SITE_CODE_2"
        self.assertEqual("SITE_CODE_2", new_form.site_code)

    def test_local_site_code(self):
        self.assertEqual(
            self.form_json["protocol"]["local_site_code"],
            self.form.local_site_code,
        )

    def test_advanced(self):
        self.assertEqual(
            False if self.form_json["protocol"]["advanced"] == "0" else True,
            self.form.advanced,
        )

    def test_visit_number(self):
        self.assertEqual(
            int(self.form_json["protocol"]["visit_number"]),
            self.form.visit_number,
        )

        self.form.visit_number = 99
        self.assertEqual(99, self.form.visit_number)

        new_form = Form()
        new_form.visit_number = 999
        self.assertEqual(999, new_form.visit_number)

    def test_sequence_number(self):
        self.assertEqual(
            int(self.form_json["protocol"]["sequence_number"]),
            self.form.sequence_number,
        )

        self.form.sequence_number = 99
        self.assertEqual(99, self.form.sequence_number)

        new_form = Form()
        new_form.sequence_number = 999
        self.assertEqual(999, new_form.sequence_number)

    def test_list_type(self):
        self.assertEqual(
            self.form_json["protocol"]["list_type"],
            self.form.list_type,
        )

    def test_id_waterbird_conditions(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_conditions"],
            self.form.id_waterbird_conditions,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_conditions": {
                    "@id": "GOOD_NORMAL",
                    "#text": "günstig / normal",
                },
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_conditions"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_conditions,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_conditions
        )

    def test_id_waterbird_coverage(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_coverage"],
            self.form.id_waterbird_coverage,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_coverage": {"@id": "COMPLETE", "#text": "± vollständig"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_coverage"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_coverage,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_coverage
        )

    def test_id_waterbird_optical(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_optical"],
            self.form.id_waterbird_optical,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_optical": {"@id": "TELESCOPE", "#text": "Spektiv"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_optical"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_optical,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_waterbird_optical)

    def test_id_waterbird_countmethod(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_countmethod"],
            self.form.id_waterbird_countmethod,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_countmethod": {
                    "@id": "GROUND",
                    "#text": "Boden (Auto, Fahrrad, zu Fuß)",
                },
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_countmethod"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_countmethod,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_countmethod
        )

    def test_id_waterbird_ice(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_ice"],
            self.form.id_waterbird_ice,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_ice": {"@id": "NO_ICE", "#text": "kein Eis"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_ice"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_ice,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_waterbird_ice)

    def test_id_waterbird_snowcover(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_snowcover"],
            self.form.id_waterbird_snowcover,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_snowcover": {"@id": "NO_SNOW", "#text": "kein Schnee"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_snowcover"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_snowcover,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_snowcover
        )

    def test_id_waterbird_waterlevel(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_waterlevel"],
            self.form.id_waterbird_waterlevel,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_waterlevel": {"@id": "NO_SNOW", "#text": "kein Schnee"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_waterlevel"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_waterlevel,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_waterlevel
        )

    def test_id_waterbird_counttype(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_counttype"],
            self.form.id_waterbird_counttype,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_counttype": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_counttype"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_counttype,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_counttype
        )

    def test_id_waterbird_visibility(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_visibility"],
            self.form.id_waterbird_visibility,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_visibility": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_visibility"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_visibility,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_visibility
        )

    def test_id_waterbird_waves(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_waves"],
            self.form.id_waterbird_waves,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_waves": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_waves"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_waves,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_waterbird_waves)

    def test_id_waterbird_conditions_reason(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_conditions_reason"],
            self.form.id_waterbird_conditions_reason,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_conditions_reason": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_conditions_reason"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_conditions_reason,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_conditions_reason
        )

    def test_id_waterbird_count_payed(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_count_payed"],
            self.form.id_waterbird_count_payed,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_count_payed": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_count_payed"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_count_payed,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_count_payed
        )

    def test_id_waterbird_activity_persons_on_shore(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_persons_on_shore"],
            self.form.id_waterbird_activity_persons_on_shore,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_persons_on_shore": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_persons_on_shore"]["@id"],
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_persons_on_shore,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_persons_on_shore
        )

    def test_id_waterbird_activity_boats_rowing(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_rowing"],
            self.form.id_waterbird_activity_boats_rowing,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_rowing": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_rowing"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_rowing,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_rowing
        )

    def test_id_waterbird_activity_boats_motor(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_motor"],
            self.form.id_waterbird_activity_boats_motor,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_motor": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_motor"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_motor,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_motor
        )

    def test_id_waterbird_activity_boats_sailing(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_sailing"],
            self.form.id_waterbird_activity_boats_sailing,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_sailing": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_sailing"]["@id"],
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_boats_sailing,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_sailing
        )

    def test_id_waterbird_activity_boats_kayak(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_kayak"],
            self.form.id_waterbird_activity_boats_kayak,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_kayak": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_kayak"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_kayak,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_kayak
        )

    def test_id_waterbird_activity_boats_fisherman(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_fisherman"],
            self.form.id_waterbird_activity_boats_fisherman,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_fisherman": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_fisherman"]["@id"],
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_boats_fisherman,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_boats_fisherman
        )

    def test_id_waterbird_activity_divers(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_divers"],
            self.form.id_waterbird_activity_divers,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_divers": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_divers"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_divers,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_divers
        )

    def test_id_waterbird_activity_surfers(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_surfers"],
            self.form.id_waterbird_activity_surfers,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_surfers": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_surfers"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_surfers,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_surfers
        )

    def test_id_moving_harvest(self):
        self.assertEqual(
            self.form_json["protocol"]["moving_harvest"],
            self.form.id_moving_harvest,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "moving_harvest": {"@id": "MAINLY", "#text": "Überwiegend (>50 %) "},
            },
        }
        self.assertEqual(
            form_json["protocol"]["moving_harvest"]["@id"],
            Form.create_from_ornitho_json(form_json).id_moving_harvest,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_moving_harvest)

    def test_id_coverage(self):
        self.assertEqual(
            self.form_json["protocol"]["coverage"],
            self.form.id_coverage,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "coverage": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["coverage"]["@id"],
            Form.create_from_ornitho_json(form_json).id_coverage,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_coverage)

    def test_id_condition(self):
        self.assertEqual(
            self.form_json["protocol"]["condition"],
            self.form.id_condition,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "condition": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["condition"]["@id"],
            Form.create_from_ornitho_json(form_json).id_condition,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_condition)

    def test_id_chiro_identify(self):
        self.assertEqual(
            self.form_json["protocol"]["chiro_identify"],
            self.form.id_chiro_identify,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "chiro_identify": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["chiro_identify"]["@id"],
            Form.create_from_ornitho_json(form_json).id_chiro_identify,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_chiro_identify)

    def test_id_additional_observer(self):
        self.assertEqual(
            self.form_json["protocol"]["additional_observer"],
            self.form.id_additional_observer,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "additional_observer": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["additional_observer"]["@id"],
            Form.create_from_ornitho_json(form_json).id_additional_observer,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_additional_observer
        )

    def test_id_changes(self):
        self.assertEqual(
            self.form_json["protocol"]["changes"],
            self.form.id_changes,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "changes": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["changes"]["@id"],
            Form.create_from_ornitho_json(form_json).id_changes,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_changes)

    def test_id_drone_used(self):
        self.assertEqual(
            self.form_json["protocol"]["drone_used"],
            self.form.id_drone_used,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "drone_used": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["drone_used"]["@id"],
            Form.create_from_ornitho_json(form_json).id_drone_used,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_drone_used)

    def test_id_tmp_water_bodies(self):
        self.assertEqual(
            self.form_json["protocol"]["tmp_water_bodies"],
            self.form.id_tmp_water_bodies,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "tmp_water_bodies": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["tmp_water_bodies"]["@id"],
            Form.create_from_ornitho_json(form_json).id_tmp_water_bodies,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_tmp_water_bodies)

    def test_nest_number(self):
        self.assertEqual(
            int(self.form_json["protocol"]["nest_number"]),
            self.form.nest_number,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "nest_number": {
                    "@id": "11",
                    "#text": "DISPLAY_PAGE_TEXT_NEST_NUMBER_11",
                },
            },
        }
        self.assertEqual(
            int(form_json["protocol"]["nest_number"]["@id"]),
            Form.create_from_ornitho_json(form_json).nest_number,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).nest_number)

    def test_occupied_nest_number(self):
        self.assertEqual(
            int(self.form_json["protocol"]["occupied_nest_number"]),
            self.form.occupied_nest_number,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "occupied_nest_number": {
                    "@id": "12",
                    "#text": "DISPLAY_PAGE_TEXT_OCCUPIED_NEST_NUMBER_12",
                },
            },
        }
        self.assertEqual(
            int(form_json["protocol"]["occupied_nest_number"]["@id"]),
            Form.create_from_ornitho_json(form_json).occupied_nest_number,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).occupied_nest_number)

    def test_playbacks(self):
        self.assertIsNone(self.form.playbacks)

        form_json = {
            "@id": "1",
            "protocol": {
                "playback": {
                    "Id_species_1": "1",
                    "Id_species_2": "0",
                },
            },
        }
        self.assertEqual(
            {1: True, 2: False},
            Form.create_from_ornitho_json(form_json).playbacks,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).playbacks)

    @mock.patch("ornitho.model.observation.Observation")
    def test_observations(self, mock_observation):
        self.form.refresh = MagicMock(return_value=self.form_json)
        mock_observation.create_from_ornitho_json.return_value = "Observation"
        observations = self.form.observations
        mock_observation.create_from_ornitho_json.assert_called_with(
            self.form_json["sightings"][0]
        )
        self.assertEqual(observations, ["Observation"])

        del self.form_json["sightings"]
        self.form.refresh = MagicMock(return_value=self.form_json)
        mock_observation.create_from_ornitho_json.return_value = "Observation"
        observations = self.form.observations
        self.assertEqual(observations, ["Observation"])

        self.form.observations = [mock_observation()]
        self.form.id_place = None
        self.form.observations = [mock_observation()]

    def test_playblack_played(self):
        mock_species = mock.MagicMock(spec=ornitho.Species)
        type(mock_species).id_ = mock.PropertyMock(return_value=1)
        self.assertEqual(mock_species.id_, 1)
        self.assertIsNone(self.form.playblack_played(1))
        self.assertIsNone(self.form.playblack_played(mock_species))

        form_json = {
            "@id": "1",
            "protocol": {
                "playback": {
                    "Id_species_1": "1",
                    "Id_species_2": "0",
                },
            },
        }
        self.assertTrue(Form.create_from_ornitho_json(form_json).playblack_played(1))
        self.assertFalse(Form.create_from_ornitho_json(form_json).playblack_played(2))
        self.assertTrue(
            Form.create_from_ornitho_json(form_json).playblack_played(mock_species)
        )

    @mock.patch("ornitho.model.form.Observation")
    @mock.patch("ornitho.model.form.CreateableModel.get")
    @mock.patch("ornitho.model.form.CreateableModel.create_in_ornitho")
    def test_create(self, mock_create_in_ornitho, mock_get, mock_observation):
        mock_create_in_ornitho.return_value = 1
        id_form_mock = MagicMock()
        id_form_mock.id_form.return_value = 1
        mock_get.return_value = id_form_mock
        mock_observation.raw_data_trim_field_ids.return_value = "TRIMMED!"

        Form.create(
            time_start=datetime.now().time(),
            time_stop=datetime.now().time(),
            observations=[mock_observation],
            protocol="PROTOCOL",
            place=1,
            visit_number=250,
            sequence_number=100,
        )
        mock_create_in_ornitho.assert_called()
        mock_observation.raw_data_trim_field_ids.assert_called()

        Form.create(
            time_start=datetime.now().time(),
            time_stop=datetime.now().time(),
            observations=[],
            protocol=mock.Mock(spec=Protocol),
            place=mock.Mock(spec=Place),
            visit_number=250,
            sequence_number=100,
        )
        mock_create_in_ornitho.assert_called()
        mock_observation.raw_data_trim_field_ids.assert_called()
