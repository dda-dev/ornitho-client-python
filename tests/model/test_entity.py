from unittest import TestCase

from ornitho import Entity


class TestEntity(TestCase):
    def setUp(self):
        self.entity_json = {
            "id": "1",
            "short_name": "Short",
            "full_name_german": "Full Nmae",
            "address": "",
            "url": "",
            "description_german": 'Description',
        }
        self.entity = Entity.create_from(self.entity_json)

    def test_short_name(self):
        self.assertEqual(self.entity_json["short_name"], self.entity.short_name)

    def test_full_name_german(self):
        self.assertEqual(
            self.entity_json["full_name_german"], self.entity.full_name_german
        )

    def test_address(self):
        self.assertEqual(self.entity_json["address"], self.entity.address)

    def test_url(self):
        self.assertEqual(self.entity_json["url"], self.entity.url)

    def test_description_german(self):
        self.assertEqual(
            self.entity_json["description_german"], self.entity.description_german
        )
