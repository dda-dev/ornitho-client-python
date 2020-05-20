from unittest import TestCase

import ornitho
from ornitho.model.territorial_unit import TerritorialUnit

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestTerritorialUnit(TestCase):
    def setUp(self):
        self.territorial_unit_json = {
            "id": "256",
            "id_country": "200",
            "name": "Dithmarschen",
            "short_name": "HEI",
        }
        self.territorial_unit = TerritorialUnit.create_from(self.territorial_unit_json)

    def test_id_country(self):
        self.assertEqual(
            int(self.territorial_unit_json["id_country"]),
            self.territorial_unit.id_country,
        )

    def test_name(self):
        self.assertEqual(self.territorial_unit_json["name"], self.territorial_unit.name)

    def test_short_name(self):
        self.assertEqual(
            self.territorial_unit_json["short_name"], self.territorial_unit.short_name
        )
