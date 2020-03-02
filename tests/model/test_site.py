from unittest import TestCase, mock

from ornitho.model.site import MapLayer, Site


class TestSite(TestCase):
    def setUp(self):
        self.site_json = {
            "id": "1",
            "id_universal": "1_1",
            "custom_name": "TEST",
            "reference_locality": "TEST-Site",
        }
        self.site = Site.create_from(self.site_json)

    def test_request(self):
        self.assertRaises(
            NotImplementedError, lambda: Site.request(method="GET", url="/test")
        )

    def test_id_universal(self):
        self.assertEqual(self.site_json["id_universal"], self.site.id_universal)

    def test_custom_name(self):
        self.assertEqual(self.site_json["custom_name"], self.site.custom_name)

    def test_reference_locality(self):
        self.assertEqual(
            self.site_json["reference_locality"], self.site.reference_locality
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
