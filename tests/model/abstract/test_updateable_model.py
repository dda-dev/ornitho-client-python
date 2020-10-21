from unittest import TestCase, mock

import ornitho
from ornitho.model.abstract import UpdateableModel

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestUpdateableModel(TestCase):
    class MyModel(UpdateableModel):
        ENDPOINT = "my_model"

    # noinspection PyUnusedLocal
    @staticmethod
    def fake_request(**kwargs):
        return "SUCCESS"

    @mock.patch.object(MyModel, "request", fake_request)
    def test_update(self):
        my_model = self.MyModel()
        response = my_model.update()
        self.assertEqual("SUCCESS", response)
