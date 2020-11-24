from unittest import TestCase, mock

import ornitho
from ornitho.model.right import Right

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestDetail(TestCase):
    # noinspection PyUnusedLocal
    @staticmethod
    def fake_request(**kwargs):
        return {
            "data": {
                "rights": [
                    {"id": "2", "name": "ADMIN", "comment": "Administratorenrechte"},
                    {
                        "id": "8",
                        "name": "ADMIN_OBS",
                        "comment": "Recht, Beobachtungen zu bearbeiten",
                    },
                ]
            }
        }, None

    @mock.patch.object(ornitho.model.right.APIRequester, "request_raw", fake_request)
    def test_retrieve_for_observer(self):
        rights = Right.retrieve_for_observer(1)
        self.assertEqual(2, len(rights))
        self.assertEqual(rights[0].id_, 2)
        self.assertEqual(rights[1].id_, 8)

    def test_str(self):
        right = Right(2, "ADMIN", "Administratorenrechte")
        self.assertEqual("2-ADMIN-Administratorenrechte", right.__str__())
