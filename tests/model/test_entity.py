from unittest import TestCase

from ornitho import Entity


class TestEntity(TestCase):
    def setUp(self):
        self.entity_json = {
            "id": "5",
            "short_name": "MhB-DE",
            "full_name_german": "MhB Default-Profil",
            "address": "",
            "url": "",
            "description_german": '<p>\r\n\tBitte wenden Sie sich an die für Ihre Bundesland / Ihre Region zuständige Koordinationsstelle. Diese finden Sie auf der DDA-Webseite unter <a href="https://www.dda-web.de/mhb" target="_blank">www.dda-web.de/mhb</a>.<br />\r\n\tIst dort keine Koordinatorin / kein Koordinator angegeben, wenden Sie sich bei Fragen bitte an die bundesweite Koordinationsstelle. Vielen Dank!</p>\r\n',
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
