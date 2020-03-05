from unittest import TestCase, mock

import ornitho
from ornitho import Form

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
            "protocol": {
                "protocol_name": "CBBM",
                "site_code": "DDA-1-Test",
                "local_site_code": "",
                "advanced": "0",
                "visit_number": "158",
                "sequence_number": "1",
                "list_type": "-",
                "waterbird_conditions": "GOOD_NORMAL",
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
        self.form = Form.create_from(self.form_json)

    def test_instance_url(self):
        self.assertEqual("observations/search", self.form.instance_url())

    @mock.patch("ornitho.model.form.APIRequester")
    def test_refresh(self, mock_requester):
        class MockRequesterClass:
            def request_raw(self, method, url, body):
                return {"data": {"forms": [{"time_start": "NEW"}]}}, None

        def enter_requester(requester):
            return MockRequesterClass()

        mock_requester.return_value.__enter__ = enter_requester
        form = self.form.refresh()
        self.assertEqual("NEW", form.time_start)

    def test_id_form_universal(self):
        self.assertEqual(
            self.form_json["id_form_universal"], self.form.id_form_universal,
        )

    def test_time_start(self):
        self.assertEqual(
            self.form_json["time_start"], self.form.time_start,
        )

    def test_time_stop(self):
        self.assertEqual(
            self.form_json["time_stop"], self.form.time_stop,
        )

    def test_full_form(self):
        self.assertEqual(
            False if self.form_json["full_form"] == "0" else True, self.form.full_form
        )

    def test_version(self):
        self.assertEqual(
            int(self.form_json["version"]), self.form.version,
        )

    def test_lat(self):
        self.assertEqual(
            float(self.form_json["lat"]), self.form.lat,
        )

    def test_lon(self):
        self.assertEqual(
            float(self.form_json["lon"]), self.form.lon,
        )

    def test_id_form_mobile(self):
        self.assertEqual(
            self.form_json["id_form_mobile"], self.form.id_form_mobile,
        )

    def test_protocol_name(self):
        self.assertEqual(
            self.form_json["protocol"]["protocol_name"], self.form.protocol_name,
        )

    def test_site_code(self):
        self.assertEqual(
            self.form_json["protocol"]["site_code"], self.form.site_code,
        )

    def test_local_site_code(self):
        self.assertEqual(
            self.form_json["protocol"]["local_site_code"], self.form.local_site_code,
        )

    def test_advanced(self):
        self.assertEqual(
            False if self.form_json["protocol"]["advanced"] == "0" else True,
            self.form.advanced,
        )

    def test_visit_number(self):
        self.assertEqual(
            int(self.form_json["protocol"]["visit_number"]), self.form.visit_number,
        )

    def test_sequence_number(self):
        self.assertEqual(
            int(self.form_json["protocol"]["sequence_number"]),
            self.form.sequence_number,
        )

    def test_list_type(self):
        self.assertEqual(
            self.form_json["protocol"]["list_type"], self.form.list_type,
        )

    def test_waterbird_conditions(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_conditions"],
            self.form.waterbird_conditions,
        )

    @mock.patch("ornitho.model.form.Observation")
    def test_observations(self, mock_observation):
        mock_observation.create_from.return_value = "Observation"
        observations = self.form.observations
        mock_observation.create_from.assert_called_with(self.form_json["sightings"][0])
        self.assertEqual(observations, ["Observation"])
