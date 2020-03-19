from datetime import datetime
from unittest import TestCase

import ornitho
from ornitho.model.media import Media

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestMedia(TestCase):
    def setUp(self):
        self.media_json = {
            "obid": "2222",
            "obs_hidden": "0",
            "surname": "Test",
            "name": "Name",
            "advanced_observer": "1",
            "traid": "2222",
            "tra_hidden": "0",
            "tra_surname": "Test",
            "tra_name": "Name",
            "obs_power_user": "0",
            "tra_power_user": "0",
            "id": "123123",
            "media": "PHOTO",
            "has_large": "1",
            "insert_date": {
                "@notime": "0",
                "@offset": "3600",
                "@timestamp": "1584206291",
            },
            "photo": "https://test.media/www.ornitho.de/1970-01/xsmall/1111-22222222-3333.jpg",
        }
        self.media = Media.create_from(self.media_json)

    def test_obid(self):
        self.assertEqual(int(self.media_json["obid"]), self.media.obid)

    def test_obs_hidden(self):
        self.assertEqual(
            False if self.media_json["obs_hidden"] == "0" else True,
            self.media.obs_hidden,
        )

    def test_surname(self):
        self.assertEqual(self.media_json["surname"], self.media.surname)

    def test_name(self):
        self.assertEqual(self.media_json["name"], self.media.name)

    def test_advanced_observer(self):
        self.assertEqual(
            False if self.media_json["advanced_observer"] == "0" else True,
            self.media.advanced_observer,
        )

    def test_traid(self):
        self.assertEqual(int(self.media_json["traid"]), self.media.traid)

    def test_tra_hidden(self):
        self.assertEqual(
            False if self.media_json["tra_hidden"] == "0" else True,
            self.media.tra_hidden,
        )

    def test_tra_surname(self):
        self.assertEqual(self.media_json["tra_surname"], self.media.tra_surname)

    def test_tra_name(self):
        self.assertEqual(self.media_json["tra_name"], self.media.tra_name)

    def test_obs_power_user(self):
        self.assertEqual(
            False if self.media_json["obs_power_user"] == "0" else True,
            self.media.obs_power_user,
        )

    def test_tra_power_user(self):
        self.assertEqual(
            False if self.media_json["tra_power_user"] == "0" else True,
            self.media.tra_power_user,
        )

    def test_media(self):
        self.assertEqual(self.media_json["media"], self.media.media)

    def test_has_large(self):
        self.assertEqual(
            False if self.media_json["has_large"] == "0" else True, self.media.has_large
        )

    def test_insert_date(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.media_json["insert_date"]["@timestamp"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.media.insert_date,
        )

    def test_photo(self):
        self.assertEqual(
            self.media_json["photo"].replace("xsmall", "large"), self.media.photo
        )

        media_json = {
            "obid": "2222",
            "obs_hidden": "0",
            "surname": "Test",
            "name": "Name",
            "advanced_observer": "1",
            "traid": "2222",
            "tra_hidden": "0",
            "tra_surname": "Test",
            "tra_name": "Name",
            "obs_power_user": "0",
            "tra_power_user": "0",
            "id": "123123",
            "media": "PHOTO",
            "has_large": "0",
            "insert_date": {
                "@notime": "0",
                "@offset": "3600",
                "@timestamp": "1584206291",
            },
            "photo": "https://test.media/www.ornitho.de/1970-01/xsmall/1111-22222222-3333.jpg",
        }

        self.assertEqual(
            media_json["photo"].replace("xsmall/", ""),
            Media.create_from(media_json).photo,
        )

        sound_json = {
            "obid": "2222",
            "obs_hidden": "0",
            "surname": "Test",
            "name": "Name",
            "advanced_observer": "1",
            "traid": "2222",
            "tra_hidden": "0",
            "tra_surname": "Test",
            "tra_name": "Name",
            "obs_power_user": "0",
            "tra_power_user": "0",
            "id": "123123",
            "media": "SOUND",
            "has_large": "0",
            "insert_date": {
                "@notime": "0",
                "@offset": "3600",
                "@timestamp": "1584206291",
            },
            "photo": "https://test.media/www.ornitho.de/1970-01/1111-22222222-3333.mp3",
        }

        self.assertEqual(sound_json["photo"], Media.create_from(sound_json).photo)

    def test_photo_small(self):
        self.assertEqual(self.media_json["photo"], self.media.photo_small)
