from unittest import TestCase, mock

import ornitho
from ornitho.model.place import Place

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestPlace(TestCase):
    def setUp(self):
        self.place_json = {
            "id": "767",
            "id_commune": "8192",
            "name": "Aasbüttel (SH, IZ) - Gemeindemittelpunkt",
            "coord_lon": "9.43977095617034",
            "coord_lat": "54.0686078708784",
            "altitude": "52",
            "id_region": "5",
            "visible": "0",
            "is_private": "0",
            "place_type": "municipality",
            "loc_precision": "750",
            "municipality": "municipality",
        }
        self.place = Place.create_from_ornitho_json(self.place_json)

    def test_id_commune(self):
        self.assertEqual(int(self.place_json["id_commune"]), self.place.id_commune)

    def test_name(self):
        self.assertEqual(self.place_json["name"], self.place.name)

    def test_coord_lon(self):
        self.assertEqual(float(self.place_json["coord_lon"]), self.place.coord_lon)

    def test_coord_lat(self):
        self.assertEqual(float(self.place_json["coord_lat"]), self.place.coord_lat)

    def test_altitude(self):
        self.assertEqual(int(self.place_json["altitude"]), self.place.altitude)

    def test_id_region(self):
        self.assertEqual(int(self.place_json["id_region"]), self.place.id_region)

    def test_visible(self):
        self.assertEqual(
            False if self.place_json["visible"] == "0" else True, self.place.visible
        )

    def test_is_private(self):
        self.assertEqual(
            False if self.place_json["is_private"] == "0" else True,
            self.place.is_private,
        )

    def test_place_type(self):
        self.assertEqual(self.place_json["place_type"], self.place.place_type)

    def test_loc_precision(self):
        self.assertEqual(
            int(self.place_json["loc_precision"]), self.place.loc_precision
        )

    @mock.patch("ornitho.model.place.LocalAdminUnit")
    def test_local_admin_unit(self, mock_local_admin_unit):
        mock_local_admin_unit.get.return_value = "Local Admin Unit retrieved"
        local_admin_unit = self.place.local_admin_unit
        mock_local_admin_unit.get.assert_called_with(self.place.id_commune)
        self.assertEqual(local_admin_unit, "Local Admin Unit retrieved")

    @mock.patch("ornitho.model.place.LocalAdminUnit")
    def test_commune(self, mock_local_admin_unit):
        mock_local_admin_unit.get.return_value = "Local Admin Unit retrieved"
        local_admin_unit = self.place.commune
        mock_local_admin_unit.get.assert_called_with(self.place.id_commune)
        self.assertEqual(local_admin_unit, "Local Admin Unit retrieved")

    def test_municipality(self):
        self.assertEqual(self.place_json["municipality"], self.place.municipality)

    def test_county(self):
        self.assertIsNone(self.place.county)

    def test_country(self):
        self.assertIsNone(self.place.country)
