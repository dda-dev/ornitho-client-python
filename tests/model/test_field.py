from unittest import TestCase, mock
from unittest.mock import MagicMock

from ornitho import Field
from ornitho.api_exception import APIException


class TestField(TestCase):
    def setUp(self):
        self.field_json = {
            "id": "1",
            "group": "OBS",
            "name": "RESTING_HABITAT",
            "text": "(Rast)Habitat",
            "default": "0",
            "mandatory": "0",
            "empty_choice": "1",
        }
        self.field = Field.create_from_ornitho_json(self.field_json)

    def test_get(self):
        Field.list_all = MagicMock(
            return_value=[
                Field.create_from_ornitho_json(
                    {
                        "id": "1",
                        "group": "OBS",
                        "name": "RESTING_HABITAT",
                        "text": "(Rast)Habitat",
                        "default": "0",
                        "mandatory": "0",
                        "empty_choice": "1",
                    }
                ),
                Field.create_from_ornitho_json(
                    {
                        "id": "2",
                        "group": "OBS",
                        "name": "ACCURACY_OF_LOCATION",
                        "text": "Genauigkeit der Ortsangabe",
                        "default": "0",
                        "mandatory": "0",
                        "empty_choice": "1",
                    }
                ),
            ]
        )
        field = Field.get(1)
        self.assertEqual(1, field.id_)

        # Test Exception
        self.assertRaises(
            APIException,
            lambda: Field.get(4),
        )

    def test_refresh(self):
        self.assertRaises(
            NotImplementedError,
            lambda: self.field.refresh(),
        )

    def test_group(self):
        self.assertEqual(self.field_json["group"], self.field.group)

    def test_name(self):
        self.assertEqual(self.field_json["name"], self.field.name)

    def test_text(self):
        self.assertEqual(self.field_json["text"], self.field.text)

    def test_default(self):
        self.assertEqual(int(self.field_json["default"]), self.field.default)

    def test_mandatory(self):
        self.assertEqual(
            False if self.field_json["mandatory"] == "0" else True, self.field.mandatory
        )

    def test_empty_choice(self):
        self.assertEqual(
            False if self.field_json["empty_choice"] == "0" else True,
            self.field.empty_choice,
        )

    @mock.patch("ornitho.model.field.APIRequester")
    @mock.patch("ornitho.model.field.FieldOption")
    def test_options(self, mock_field_option, mock_requester):
        class MockRequesterClass:
            def request(self, method, url):
                return ["option1", "option2"], "pk"

        def enter_requester(requester):
            return MockRequesterClass()

        mock_requester.return_value.__enter__ = enter_requester

        mock_field_option.create_from_ornitho_json.return_value = ["Created!"]

        self.assertEqual(
            [
                mock_field_option.create_from_ornitho_json.return_value,
                mock_field_option.create_from_ornitho_json.return_value,
            ],
            self.field.options,
        )
