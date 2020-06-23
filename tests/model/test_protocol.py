from unittest import TestCase, mock
from unittest.mock import MagicMock

import ornitho
from ornitho import Protocol

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestProtocol(TestCase):
    def setUp(self):
        self.protocol_json = {
            "id": "1",
            "name": "TEST",
            "nbre_points_min": "0",
            "nbre_points_max": "0",
            "time_point": "",
            "taxo_point": "1",
            "additional_taxo_point": "",
            "nbre_transects_min": "1",
            "nbre_transects_max": "1",
            "time_transect": "",
            "taxo_transect": "1",
            "additional_taxo_transect": "",
            "nbre_polygones_min": "0",
            "nbre_polygones_max": "0",
            "time_polygone": "",
            "taxo_poly": "1",
            "additional_taxo_poly": "",
            "project_id": "",
            "id_entity": "5",
            "nbre_bounding_box_max": "2",
            "nbre_passage": "",
            "auto_hidden": "0",
            "only_admin_create": "1",
            "start_month": "1",
            "default_atlas_code": "",
            "default_count": "",
        }
        self.protocol = Protocol.create_from(self.protocol_json)

    def test_name(self):
        self.assertEqual(self.protocol_json["name"], self.protocol.name)

    def test_nbre_points_min(self):
        self.assertEqual(
            int(self.protocol_json["nbre_points_min"]), self.protocol.nbre_points_min
        )

    def test_nbre_points_max(self):
        self.assertEqual(
            int(self.protocol_json["nbre_points_max"]), self.protocol.nbre_points_max
        )

    def test_time_point(self):
        self.assertIsNone(self.protocol.time_point)

    def test_taxo_point(self):
        self.assertEqual(
            int(self.protocol_json["taxo_point"]), self.protocol.taxo_point
        )

    def test_additional_taxo_point(self):
        self.assertIsNone(self.protocol.additional_taxo_point)

    def test_nbre_transects_min(self):
        self.assertEqual(
            int(self.protocol_json["nbre_transects_min"]),
            self.protocol.nbre_transects_min,
        )

    def test_nbre_transects_max(self):
        self.assertEqual(
            int(self.protocol_json["nbre_transects_max"]),
            self.protocol.nbre_transects_max,
        )

    def test_time_transect(self):
        self.assertIsNone(self.protocol.time_transect)

    def test_taxo_transect(self):
        self.assertEqual(
            int(self.protocol_json["taxo_transect"]), self.protocol.taxo_transect
        )

    def test_additional_taxo_transect(self):
        self.assertIsNone(self.protocol.additional_taxo_transect)

    def test_nbre_polygones_min(self):
        self.assertEqual(
            int(self.protocol_json["nbre_polygones_min"]),
            self.protocol.nbre_polygones_min,
        )

    def test_nbre_polygones_max(self):
        self.assertEqual(
            int(self.protocol_json["nbre_polygones_max"]),
            self.protocol.nbre_polygones_max,
        )

    def test_time_polygone(self):
        self.assertIsNone(self.protocol.time_polygone)

    def test_taxo_poly(self):
        self.assertEqual(int(self.protocol_json["taxo_poly"]), self.protocol.taxo_poly)

    def test_additional_taxo_poly(self):
        self.assertIsNone(self.protocol.additional_taxo_poly)

    def test_project_id(self):
        self.assertIsNone(self.protocol.project_id)

    def test_id_entity(self):
        self.assertEqual(int(self.protocol_json["id_entity"]), self.protocol.id_entity)

    def test_nbre_bounding_box_max(self):
        self.assertEqual(
            int(self.protocol_json["nbre_bounding_box_max"]),
            self.protocol.nbre_bounding_box_max,
        )

    def test_nbre_passage(self):
        self.assertIsNone(self.protocol.nbre_passage)

    def test_auto_hidden(self):
        self.assertFalse(self.protocol.auto_hidden)

    def test_only_admin_create(self):
        self.assertTrue(self.protocol.only_admin_create)

    def test_start_month(self):
        self.assertEqual(
            int(self.protocol_json["start_month"]), self.protocol.start_month
        )

    def test_default_atlas_code(self):
        self.assertIsNone(self.protocol.default_atlas_code)

    def test_default_count(self):
        self.assertIsNone(self.protocol.default_count)

    @mock.patch("ornitho.model.protocol.Entity")
    def test_entity(self, mock_entity):
        mock_entity.get.return_value = "Entity retrieved"
        entity = self.protocol.entity
        mock_entity.get.assert_called_with(self.protocol.id_entity)
        self.assertEqual(entity, "Entity retrieved")

    def test_sites(self):
        Protocol.request = MagicMock(
            return_value=[
                {
                    "sites": {
                        "5253": {
                            "id": "5253",
                            "id_universal": "28_5253",
                            "custom_name": "test CBBM",
                            "reference_locality": "Staufenberg [4623_4_39s]",
                        },
                        "7043": {
                            "id": "7043",
                            "id_universal": "28_7043",
                            "custom_name": "dda3",
                            "reference_locality": "DDA-Teststrecke-Uder",
                        },
                    }
                }
            ]
        )

        sites = self.protocol.sites
        self.assertEqual(len(sites), 2)
        Protocol.request.assert_called_with(
            method="get",
            url=f"{self.protocol.ENDPOINT}/list_sites",
            params={"id": self.protocol.id_},
        )

    @mock.patch("ornitho.model.protocol.Observation")
    def test_get_observations(self, mock_observation):
        mock_observation.search = MagicMock(
            return_value=[["observation1", "observation2"], None]
        )

        observations = self.protocol.get_observations()
        self.assertEqual(2, len(observations[0]))
        self.assertIsNone(observations[1])
        mock_observation.search.assert_called_with(
            request_all=False,
            pagination_key=None,
            short_version=False,
            only_protocol=self.protocol.name,
            period_choice="all",
        )

    @mock.patch("ornitho.model.protocol.Observation")
    def test_get_all_observations(self, mock_observation):
        mock_observation.search = MagicMock(
            return_value=[["observation1", "observation2"], None]
        )

        observations = self.protocol.get_all_observations(period_choice="range")
        self.assertEqual(2, len(observations))
        mock_observation.search.assert_called_with(
            request_all=True,
            pagination_key=None,
            short_version=False,
            only_protocol=self.protocol.name,
            period_choice="range",
        )
