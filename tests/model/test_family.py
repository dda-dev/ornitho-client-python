from unittest import TestCase, mock

import ornitho
from ornitho.model.family import Family

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestFamily(TestCase):
    def setUp(self):
        self.family_json = {
            "id": "1",
            "id_taxo_group": "1",
            "name": "BIRD_FAMILY_GAVIIDAE",
            "latin_name": "Gaviidae",
            "generic": "0",
        }
        self.family = Family.create_from(self.family_json)

    def test_id_taxo_group(self):
        self.assertEqual(
            int(self.family_json["id_taxo_group"]), self.family.id_taxo_group
        )

    def test_name(self):
        self.assertEqual(self.family_json["name"], self.family.name)

    def test_latin_name(self):
        self.assertEqual(self.family_json["latin_name"], self.family.latin_name)

    def test_generic(self):
        self.assertEqual(
            False if self.family_json["generic"] == "0" else True, self.family.generic
        )

    @mock.patch("ornitho.model.family.TaxonomicGroup")
    def test_taxo_group(self, mock_taxo_group):
        mock_taxo_group.get.return_value = "Taxonomic Group retrieved"
        taxo_group = self.family.taxo_group
        mock_taxo_group.get.assert_called_with(self.family.id_taxo_group)
        self.assertEqual(taxo_group, "Taxonomic Group retrieved")
