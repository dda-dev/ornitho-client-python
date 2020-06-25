from unittest import TestCase, mock

import ornitho
from ornitho.model.abstract import CreateableModel

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestCreateableModel(TestCase):
    class MyModel(CreateableModel):
        ENDPOINT = "my_model"

    # noinspection PyUnusedLocal
    @staticmethod
    def fake_request(**kwargs):
        return [{"id": [1]}]

    @mock.patch.object(MyModel, "request", fake_request)
    def test_create_in_ornitho(self):
        returned_id = self.MyModel.create_in_ornitho({"my_data": 123})
        self.assertEqual(1, returned_id)
