from unittest import TestCase

import ornitho
from ornitho.model.local_admin_unit import LocalAdminUnit

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestLocalAdminUnit(TestCase):
    def setUp(self):
        self.local_admin_unit_json = {
            "id": "8192",
            "id_canton": "269",
            "name": "Aasbüttel (SH, IZ)",
            "insee": "",
            "coord_lon": "9.43977095617034",
            "coord_lat": "54.0686078708784",
        }
        self.local_admin_unit = LocalAdminUnit.create_from_ornitho_json(
            self.local_admin_unit_json
        )

    def test_id_canton(self):
        self.assertEqual(
            int(self.local_admin_unit_json["id_canton"]),
            self.local_admin_unit.id_canton,
        )

    def test_name(self):
        self.assertEqual(self.local_admin_unit_json["name"], self.local_admin_unit.name)

    def test_insee(self):
        self.assertEqual(
            self.local_admin_unit_json["insee"], self.local_admin_unit.insee
        )

    def test_coord_lon(self):
        self.assertEqual(
            float(self.local_admin_unit_json["coord_lon"]),
            self.local_admin_unit.coord_lon,
        )

    def test_coord_lat(self):
        self.assertEqual(
            float(self.local_admin_unit_json["coord_lat"]),
            self.local_admin_unit.coord_lat,
        )

    def test_territorial_unit(
        self,
    ):
        territorial_unit = self.local_admin_unit.territorial_unit
        self.assertEqual(
            int(self.local_admin_unit_json["id_canton"]), territorial_unit.id_
        )

    def test_canton(
        self,
    ):
        territorial_unit = self.local_admin_unit.canton
        self.assertEqual(
            int(self.local_admin_unit_json["id_canton"]), territorial_unit.id_
        )
