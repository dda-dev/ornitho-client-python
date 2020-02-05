from unittest import TestCase
from unittest.mock import Mock

from ornitho import AuthenticationException


class TestAPIException(TestCase):
    """
    Error tests
    """

    def setUp(self):
        self.mock_response = Mock()
        self.mock_response.status_code = 401
        self.mock_response.reason = "Unauthorized"
        self.mock_response.text = (
            "Can't verify request, missing oauth_consumer_key or oauth_token (3Leg)The "
            'consumer_key "KEY" token "" combination does not exist or is not enabled.'
        )
        self.exception = AuthenticationException(self.mock_response)

    def test_str(self):
        self.assertEqual(self.mock_response.reason, self.exception.__str__())

    def test_repr(self):
        self.assertEqual(
            f"{self.exception.__class__.__name__}(http_status={self.mock_response.status_code}, "
            f"reason='{self.mock_response.reason}', body='{self.mock_response.text}')",
            self.exception.__repr__(),
        )

    def test_http_status(self):
        self.assertEqual(self.mock_response.status_code, self.exception.http_status)

    def test_reason(self):
        self.assertEqual(self.mock_response.reason, self.exception.reason)

    def test_body(self):
        self.assertEqual(self.mock_response.text, self.exception.body)
