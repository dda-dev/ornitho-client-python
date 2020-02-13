from unittest import TestCase

import ornitho
from ornitho.model.species import Species

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestSpecies(TestCase):
    def setUp(self):
        self.species_json = {
            "id": "1",
            "id_taxo_group": "1",
            "sys_order": "3320",
            "sempach_id_family": "1",
            "category_1": "A",
            "rarity": "unusual",
            "atlas_start": "0",
            "atlas_end": "0",
            "latin_name": "Gavia stellata",
            "french_name": "Plongeon catmarin",
            "french_name_plur": "Plongeons catmarins",
            "german_name": "Stern|taucher",
            "german_name_plur": "Sterntaucher",
            "english_name": "Red-throated Diver",
            "english_name_plur": "Red-throated Divers",
            "is_used": "1",
        }
        self.species = Species.create_from(self.species_json)

    def test_id_taxo_group(self):
        self.assertEqual(
            int(self.species_json["id_taxo_group"]), self.species.id_taxo_group
        )

    def test_sys_order(self):
        self.assertEqual(int(self.species_json["sys_order"]), self.species.sys_order)

    def test_sempach_id_family(self):
        self.assertEqual(
            int(self.species_json["sempach_id_family"]), self.species.sempach_id_family
        )

    def test_category_1(self):
        self.assertEqual(self.species_json["category_1"], self.species.category_1)

    def test_rarity(self):
        self.assertEqual(self.species_json["rarity"], self.species.rarity)

    def test_atlas_start(self):
        self.assertEqual(
            int(self.species_json["atlas_start"]), self.species.atlas_start
        )

    def test_atlas_end(self):
        self.assertEqual(int(self.species_json["atlas_end"]), self.species.atlas_end)

    def test_latin_name(self):
        self.assertEqual(self.species_json["latin_name"], self.species.latin_name)

    def test_french_name(self):
        self.assertEqual(self.species_json["french_name"], self.species.french_name)

    def test_french_name_plur(self):
        self.assertEqual(
            self.species_json["french_name_plur"], self.species.french_name_plur
        )

    def test_german_name(self):
        self.assertEqual(self.species_json["german_name"], self.species.german_name)

    def test_german_name_plur(self):
        self.assertEqual(
            self.species_json["german_name_plur"], self.species.german_name_plur
        )

    def test_english_name(self):
        self.assertEqual(self.species_json["english_name"], self.species.english_name)

    def test_english_name_plur(self):
        self.assertEqual(
            self.species_json["english_name_plur"], self.species.english_name_plur
        )

    def test_is_used(self):
        self.assertEqual(
            False if self.species_json["is_used"] == "0" else True, self.species.is_used
        )
