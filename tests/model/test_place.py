from datetime import datetime, timedelta
from unittest import TestCase, mock
from unittest.mock import MagicMock

import pytz

import ornitho
from ornitho import ModificationType
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
            "created_by": "30",
            "created_date": {
                "@timestamp": "1285902090",
                "@notime": "0",
                "@offset": "7200",
                "@ISO8601": "2010-10-01T05:01:30+02:00",
                "#text": "Freitag, 1. Oktober 2010, 05:01:30",
            },
            "last_updated_by": "30",
            "last_updated_date": {
                "@timestamp": "1530066871",
                "@notime": "0",
                "@offset": "7200",
                "@ISO8601": "2018-06-27T04:34:31+02:00",
                "#text": "Mittwoch, 27. Juni 2018, 04:34:31",
            },
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

    def test_created_by(self):
        self.assertEqual(int(self.place_json["created_by"]), self.place.created_by.id_)

    def test_created_date(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.place_json["created_date"]["@timestamp"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.place.created_date,
        )

    def test_last_updated_by(self):
        self.assertEqual(
            int(self.place_json["last_updated_by"]), self.place.last_updated_by.id_
        )

    def test_last_updated_date(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.place_json["last_updated_date"]["@timestamp"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.place.last_updated_date,
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

    def test_centroid(self):
        self.assertIsNone(self.place.centroid)

    def test_order(self):
        self.assertIsNone(self.place.order)

    def test_wkt(self):
        self.assertIsNone(self.place.wkt)

    @mock.patch("ornitho.model.place.ListableModel.list_all")
    def test_find_closest_place(self, mock_list_all):
        mock_list_all.return_value = ["Place"]

        place = Place.find_closest_place(1.1, 2.2)
        self.assertEqual(place, "Place")

    def test_create_from_site(self):
        place = Place.create_from_site(
            {
                "id": "1",
                "id_universal": "1_1",
                "name": "ETST (1)",
                "altitude": "1",
                "order": "1",
                "wkt": "POINT(1.1 2.2)",
            }
        )
        self.assertEqual(1, place.id_)

    def test_diff(self):
        Place.request = MagicMock(
            return_value=[
                {
                    "id_place": "1",
                    "id_universal": "1",
                    "modification_type": "updated",
                },
                {
                    "id_place": "2",
                    "id_universal": "2",
                    "modification_type": "deleted",
                },
            ]
        )

        # Case 1: without retrieving
        date = datetime.now() - timedelta(hours=1)
        observations = Place.diff(
            date,
            modification_type=ModificationType.ALL,
            only_protocol="CBBM",
        )
        self.assertEqual(len(observations), 2)
        Place.request.assert_called_with(
            method="get",
            url="places/diff",
            params={
                "date": date.replace(microsecond=0).isoformat(),
                "modification_type": ModificationType.ALL.value,
                "only_protocol": "CBBM",
            },
        )

        # Case 2: with retrieving

        mock_protocol = MagicMock(spec=ornitho.Protocol)
        type(mock_protocol).name = mock.PropertyMock(return_value="CBBM-Mock")
        Place.get = MagicMock(return_value=self.place)
        date = datetime.now().astimezone(pytz.timezone("Asia/Tokyo")) - timedelta(
            hours=1
        )
        places = Place.diff(date, only_protocol=mock_protocol, retrieve_places=True)
        self.assertEqual(len(places), 2)
        self.assertEqual(places[0], self.place)
        Place.request.assert_called_with(
            method="get",
            url="places/diff",
            params={
                "date": date.replace(microsecond=0)
                .astimezone(datetime.now().astimezone().tzinfo)
                .replace(tzinfo=None)
                .isoformat(),
                "only_protocol": "CBBM-Mock",
            },
        )
