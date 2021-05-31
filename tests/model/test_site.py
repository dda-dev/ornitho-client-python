from unittest import TestCase, mock

from ornitho.model.site import MapLayer, Site


class TestSite(TestCase):
    def setUp(self):
        self.site_json = {
            "id": "1",
            "id_universal": "1_1",
            "custom_name": "TEST",
            "local_name": "TEST_LOCAL",
            "id_reference_locality": "1",
            "reference_locality": "TEST-Site",
            "id_protocol": "1",
            "points": [
                {
                    "id": "2",
                    "id_universal": "2_2",
                    "name": "POINT 2",
                    "altitude": "2",
                    "order": "2",
                    "wkt": "POINT(2.2 2.2)",
                },
            ],
            "polygons": [
                {
                    "id": "3",
                    "id_universal": "3_3",
                    "name": "POLYGON 3",
                    "altitude": "3",
                    "order": "4",
                    "wkt": "POLYGON((3.3 3.3,1.1 1.1,3.3 3.3,))",
                }
            ],
            "transects": [
                {
                    "id": "4",
                    "id_universal": "4_4",
                    "name": "TRANSECT 4",
                    "centroid": "POINT(4.4 4.4)",
                    "altitude": "4",
                    "order": "4",
                    "wkt": "LINESTRING(4.4 4.4,5.5 5.5)",
                }
            ],
            "boundary_wkt": "GEOMETRYCOLLECTION(POLYGON((6.6 6.6,7.7 7.7,6.6 6.6)))",
            "observers": ["123456"],
        }
        self.site = Site.create_from_ornitho_json(self.site_json)

    def test_id_universal(self):
        self.assertEqual(self.site_json["id_universal"], self.site.id_universal)

    def test_custom_name(self):
        self.assertEqual(self.site_json["custom_name"], self.site.custom_name)

    def test_local_name(self):
        self.assertEqual(self.site_json["local_name"], self.site.local_name)

    def test_id_reference_locality(self):
        self.assertEqual(
            int(self.site_json["id_reference_locality"]),
            self.site.id_reference_locality,
        )

    def test_reference_locality(self):
        self.assertEqual(
            self.site_json["reference_locality"], self.site.reference_locality
        )

    def test_place(
        self,
    ):
        self.assertEqual(
            int(self.site_json["id_reference_locality"]), self.site.place.id_
        )

    def test_id_protocol(self):
        self.assertEqual(int(self.site_json["id_protocol"]), self.site.id_protocol)

    def test_transect_places(self):
        self.assertEqual(
            int(self.site_json["transects"][0]["id"]), self.site.transect_places[0].id_
        )

    def test_point_places(self):
        self.assertEqual(
            int(self.site_json["points"][0]["id"]), self.site.point_places[0].id_
        )

    def test_polygon_places(self):
        self.assertEqual(
            int(self.site_json["polygons"][0]["id"]), self.site.polygon_places[0].id_
        )

    def test_boundary_wkt(self):
        self.assertEqual(self.site_json["boundary_wkt"], self.site.boundary_wkt)

    def test_observers(self):
        self.assertEqual(
            int(self.site_json["observers"][0]), self.site.observers[0].id_
        )

    @mock.patch("ornitho.model.site.APIRequester")
    def test_pdf(self, mock_requester):
        class MockRequesterClass:
            def request(self, method, url, params):
                return b"PDF", "pk"

        def enter_requester(requester):
            return MockRequesterClass()

        mock_requester.return_value.__enter__ = enter_requester

        pdf = self.site.pdf(
            map_layer=MapLayer.BKG,
            greyscale=True,
            greyline=True,
            alpha=True,
            boundary=True,
        )
        self.assertEqual(b"PDF", pdf)
