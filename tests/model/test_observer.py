from datetime import datetime
from unittest import TestCase, mock
from unittest.mock import MagicMock

import ornitho
from ornitho.model.observer import Observer

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestObserver(TestCase):
    def setUp(self):
        self.observer_json = {
            "id": "9446",
            "external_id": "0",
            "name": "Datenbank",
            "surname": "Dbird",
            "street": "An den Speichern",
            "number": "6",
            "postcode": "48157",
            "municipality": "Münster",
            "lat": "51.9543773534501",
            "lon": "7.62357910479833",
            "email": "dbird@dda-web.de",
            "private_phone": "",
            "work_phone": "",
            "mobile_phone": "",
            "birth_year": "1970",
            "atlas_list": "19",
            "id_universal": "37382",
            "display_order": "DATE_PLACE_SPECIES",
            "registration_date": {
                "@timestamp": "1381071044",
                "@notime": "1",
                "@offset": "7200",
                "@ISO8601": "2013-10-06T16:50:44+02:00",
                "#text": "Sonntag, 6. Oktober 2013",
            },
            "last_inserted_data": {
                "@timestamp": "32400",
                "@notime": "0",
                "@offset": "3600",
                "@ISO8601": "1970-01-01T10:00:00+01:00",
                "#text": "Donnerstag, 1. Januar 1970, 10:00:00",
            },
            "last_login": {
                "@timestamp": "1578663858",
                "@notime": "0",
                "@offset": "3600",
                "@ISO8601": "2020-01-10T14:44:18+01:00",
                "#text": "Freitag, 10. Januar 2020, 14:44:18",
            },
            "anonymous": "1",
            "hide_email": "1",
            "photo": "",
            "species_order": "ALPHA",
            "langu": "de",
            "item_per_page_obs": "20",
            "item_per_page_gallery": "12",
            "archive_account": "0",
            "collectif": "0",
            "use_latin_search": "N",
            "private_website": "",
            "presentation": "",
            "has_search_access": "0",
            "default_hidden": "0",
            "debug_file_upload": "0",
            "mobile_use_form": "0",
            "mobile_use_mortality": "0",
            "show_precise": "0",
            "bypass_purchase": "0",
            "mobile_use_protocol": "0",
            "mobile_use_trace": "0",
        }
        self.observer = Observer.create_from_ornitho_json(self.observer_json)

    def test_current(self):
        Observer.request = MagicMock(
            return_value=[
                {
                    "id": "42",
                    "external_id": "0",
                    "name": "TEST_NAME",
                    "surname": "TEST_SURNAME",
                }
            ]
        )
        observer = Observer.current()
        self.assertEqual(observer.id_, 42)
        self.assertEqual(observer.external_id, 0)
        self.assertEqual(observer.name, "TEST_NAME")
        self.assertEqual(observer.surname, "TEST_SURNAME")
        Observer.request.assert_called_with(
            method="GET", url="observers/current",
        )

    def test_external_id(self):
        self.assertEqual(
            int(self.observer_json["external_id"]), self.observer.external_id
        )

    def test_name(self):
        self.assertEqual(self.observer_json["name"], self.observer.name)

    def test_surname(self):
        self.assertEqual(self.observer_json["surname"], self.observer.surname)

    def test_street(self):
        self.assertEqual(self.observer_json["street"], self.observer.street)

    def test_number(self):
        self.assertEqual(self.observer_json["number"], self.observer.number)

    def test_postcode(self):
        self.assertEqual(self.observer_json["postcode"], self.observer.postcode)

    def test_municipality(self):
        self.assertEqual(self.observer_json["municipality"], self.observer.municipality)

    def test_lat(self):
        self.assertEqual(float(self.observer_json["lat"]), self.observer.lat)

    def test_lon(self):
        self.assertEqual(float(self.observer_json["lon"]), self.observer.lon)

    def test_email(self):
        self.assertEqual(self.observer_json["email"], self.observer.email)

    def test_private_phone(self):
        self.assertEqual(
            self.observer_json["private_phone"], self.observer.private_phone
        )

    def test_work_phone(self):
        self.assertEqual(self.observer_json["work_phone"], self.observer.work_phone)

    def test_mobile_phone(self):
        self.assertEqual(self.observer_json["mobile_phone"], self.observer.mobile_phone)

    def test_birth_year(self):
        self.assertEqual(
            int(self.observer_json["birth_year"]), self.observer.birth_year
        )

    def test_atlas_list(self):
        self.assertEqual(
            int(self.observer_json["atlas_list"]), self.observer.atlas_list
        )

    def test_id_universal(self):
        self.assertEqual(
            int(self.observer_json["id_universal"]), self.observer.id_universal
        )

    def test_display_order(self):
        self.assertEqual(
            self.observer_json["display_order"], self.observer.display_order
        )

    def test_registration_date(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.observer_json["registration_date"]["@timestamp"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.observer.registration_date,
        )

    def test_last_inserted_data(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.observer_json["last_inserted_data"]["@timestamp"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.observer.last_inserted_data,
        )

    def test_last_login(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.observer_json["last_login"]["@timestamp"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.observer.last_login,
        )

    def test_anonymous(self):
        self.assertEqual(
            False if self.observer_json["anonymous"] == "0" else True,
            self.observer.anonymous,
        )

    def test_hide_email(self):
        self.assertEqual(
            False if self.observer_json["hide_email"] == "0" else True,
            self.observer.hide_email,
        )

    def test_photo(self):
        self.assertEqual(self.observer_json["photo"], self.observer.photo)

    def test_species_order(self):
        self.assertEqual(
            self.observer_json["species_order"], self.observer.species_order
        )

    def test_langu(self):
        self.assertEqual(self.observer_json["langu"], self.observer.langu)

    def test_item_per_page_obs(self):
        self.assertEqual(
            int(self.observer_json["item_per_page_obs"]),
            self.observer.item_per_page_obs,
        )

    def test_item_per_page_gallery(self):
        self.assertEqual(
            int(self.observer_json["item_per_page_gallery"]),
            self.observer.item_per_page_gallery,
        )

    def test_archive_account(self):
        self.assertEqual(
            False if self.observer_json["archive_account"] == "0" else True,
            self.observer.archive_account,
        )

    def test_collectif(self):
        self.assertEqual(
            False if self.observer_json["collectif"] == "0" else True,
            self.observer.collectif,
        )

    def test_use_latin_search(self):
        self.assertEqual(
            False if self.observer_json["use_latin_search"] == "N" else True,
            self.observer.use_latin_search,
        )

    def test_private_website(self):
        self.assertEqual(
            self.observer_json["private_website"], self.observer.private_website
        )

    def test_presentation(self):
        self.assertEqual(self.observer_json["presentation"], self.observer.presentation)

    def test_has_search_access(self):
        self.assertEqual(
            False if self.observer_json["has_search_access"] == "0" else True,
            self.observer.has_search_access,
        )

    def test_default_hidden(self):
        self.assertEqual(
            False if self.observer_json["default_hidden"] == "0" else True,
            self.observer.default_hidden,
        )

    def test_debug_file_upload(self):
        self.assertEqual(
            False if self.observer_json["debug_file_upload"] == "0" else True,
            self.observer.debug_file_upload,
        )

    def test_mobile_use_form(self):
        self.assertEqual(
            False if self.observer_json["mobile_use_form"] == "0" else True,
            self.observer.mobile_use_form,
        )

    def test_mobile_use_mortality(self):
        self.assertEqual(
            False if self.observer_json["mobile_use_mortality"] == "0" else True,
            self.observer.mobile_use_mortality,
        )

    def test_show_precise(self):
        self.assertEqual(
            False if self.observer_json["show_precise"] == "0" else True,
            self.observer.show_precise,
        )

    def test_bypass_purchase(self):
        self.assertEqual(
            False if self.observer_json["bypass_purchase"] == "0" else True,
            self.observer.bypass_purchase,
        )

    def test_mobile_use_protocol(self):
        self.assertEqual(
            False if self.observer_json["mobile_use_protocol"] == "0" else True,
            self.observer.mobile_use_protocol,
        )

    def test_mobile_use_trace(self):
        self.assertEqual(
            False if self.observer_json["mobile_use_trace"] == "0" else True,
            self.observer.mobile_use_trace,
        )

    def test_rights(self):
        with mock.patch("ornitho.model.observer.Right") as mock_right:
            mock_right.retrieve_for_observer.return_value = "RIGHTS"
            self.assertEqual(
                "RIGHTS", self.observer.rights,
            )
