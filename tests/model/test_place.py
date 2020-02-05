from unittest import TestCase

from ornitho.model.place import Place


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
        }
        self.place = Place.create_from(self.place_json)

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
