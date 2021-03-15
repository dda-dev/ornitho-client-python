from unittest import TestCase, mock

from ornitho import FieldOption
from ornitho.api_exception import APIException


class TestFieldOption(TestCase):
    def setUp(self):
        self.field_option_json = {
            "id": "1_1",
            "name": "SET_ASIDE",
            "text": "Brache (keine Ackerbrache)",
            "value": "1",
            "order_id": "10",
        }
        self.field_option = FieldOption.create_from_ornitho_json(self.field_option_json)

    @mock.patch("ornitho.model.field_option.APIRequester")
    def test_get(self, mock_requester):
        class MockRequesterClass:
            def request(self, method, url, short_version=False, params=None):
                return (
                    [
                        {
                            "id": "1_1",
                            "name": "SET_ASIDE",
                            "text": "Brache (keine Ackerbrache)",
                            "value": "1",
                            "order_id": "10",
                        },
                        {
                            "id": "1_2",
                            "name": "GROYNE_FIELD",
                            "text": "Buhnenfeld",
                            "value": "2",
                            "order_id": "20",
                        },
                    ],
                    None,
                )

        def enter_requester(requester):
            return MockRequesterClass()

        mock_requester.return_value.__enter__ = enter_requester

        field_option = FieldOption.get("1_1")
        self.assertEqual("1_1", field_option.id_)

        # Test Exception
        self.assertRaises(
            APIException,
            lambda: FieldOption.get("123_123"),
        )
        self.assertRaises(
            APIException,
            lambda: FieldOption.get("abc"),
        )

    def test_refresh(self):
        self.assertRaises(
            NotImplementedError,
            lambda: self.field_option.refresh(),
        )

    def test_name(self):
        self.assertEqual(self.field_option_json["name"], self.field_option.name)

    def test_text(self):
        self.assertEqual(self.field_option_json["text"], self.field_option.text)

    def test_value(self):
        self.assertEqual(int(self.field_option_json["value"]), self.field_option.value)

    def test_order_id(self):
        self.assertEqual(
            int(self.field_option_json["order_id"]), self.field_option.order_id
        )
