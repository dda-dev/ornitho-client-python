from unittest import TestCase

import ornitho
from ornitho.model.taxo_group import TaxonomicGroup

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestTaxonomicGroup(TestCase):
    def setUp(self):
        self.taxo_group_json = {
            "id": "1",
            "name": "Vögel",
            "latin_name": "Aves",
            "name_constant": "TAXO_GROUP_BIRD",
            "access_mode": "full",
        }
        self.taxo_group = TaxonomicGroup.create_from(self.taxo_group_json)

    def test_name(self):
        self.assertEqual(self.taxo_group_json["name"], self.taxo_group.name)

    def test_latin_name(self):
        self.assertEqual(self.taxo_group_json["latin_name"], self.taxo_group.latin_name)

    def test_name_constant(self):
        self.assertEqual(
            self.taxo_group_json["name_constant"], self.taxo_group.name_constant
        )

    def test_access_mode(self):
        self.assertEqual(
            self.taxo_group_json["access_mode"], self.taxo_group.access_mode
        )
