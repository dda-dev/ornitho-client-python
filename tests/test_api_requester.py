import json
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, Mock

import pytz

import ornitho
from ornitho import (
    APIException,
    APIHttpException,
    APIRequester,
    AuthenticationException,
    BadGatewayException,
    GatewayTimeoutException,
    ServiceUnavailableException,
)

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestAPIRequester(TestCase):
    def setUp(self):
        self.requester = APIRequester()

    def test_missing_config(self):
        ornitho.consumer_key = None
        self.assertRaises(RuntimeError, lambda: APIRequester())
        ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"

        ornitho.consumer_secret = None
        self.assertRaises(RuntimeError, lambda: APIRequester())
        ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"

        ornitho.user_email = None
        self.assertRaises(RuntimeError, lambda: APIRequester())
        ornitho.user_email = "ORNITHO_USER_EMAIL"

        ornitho.user_pw = None
        self.assertRaises(RuntimeError, lambda: APIRequester())
        ornitho.user_pw = "ORNITHO_USER_PW"

        ornitho.api_base = None
        self.assertRaises(RuntimeError, lambda: APIRequester())
        ornitho.api_base = "ORNITHO_API_BASE"

    def test_enter(self):
        requester = self.requester.__enter__()
        self.assertEqual(requester, self.requester)

    def test_exit(self):
        self.requester.close = Mock()
        self.requester.__exit__()
        self.requester.close.assert_called()

    def test_close(self):
        self.requester.session = Mock()
        self.requester.close()
        self.requester.session.close.assert_called()

    def test_request(self):
        # Case 1: no data key
        self.requester.request_raw = MagicMock(
            return_value=[[{"id": "1"}, {"id": "2"}], None]
        )
        response, pk = self.requester.request(method="get", url="test")
        self.assertEqual(response, [{"id": "1"}, {"id": "2"}])
        self.assertEqual(pk, None)

        # Case 2: data is list
        self.requester.request_raw = MagicMock(
            return_value=[{"data": [{"id": "1"}, {"id": "2"}]}, None]
        )
        response, pk = self.requester.request(method="get", url="test")
        self.assertEqual(response, [{"id": "1"}, {"id": "2"}])
        self.assertEqual(pk, None)

        # Case 3: data is dict
        self.requester.request_raw = MagicMock(
            return_value=[
                {
                    "data": {
                        "sightings": [],
                        "forms": [
                            {
                                "full_form": "1",
                                "sightings": [
                                    {"id": "1", "date": {"@timestamp": "1584918000"}}
                                ],
                            }
                        ],
                    }
                },
                "pagination_key",
            ]
        )
        response, pk = self.requester.request(method="post", url="test")
        self.assertEqual(
            response,
            [
                {
                    "date": {"@timestamp": "1584918000"},
                    "form": {"day": {"@timestamp": "1584918000"}, "full_form": "1"},
                    "id": "1",
                }
            ],
        )
        self.assertEqual(pk, "pagination_key")

        # Case 4: request all
        self.requester.request_raw = MagicMock(
            side_effect=[
                [{"data": [{"id": "1"}]}, "pagination_key"],
                [{"data": []}, "pagination_key"],
            ]
        )
        response, pk = self.requester.request(
            method="get", url="test", pagination_key="pagination_key", request_all=True
        )
        self.assertEqual(response, [{"id": "1"}])
        self.assertEqual(pk, "pagination_key")

        # Case 5: response is bytes
        self.requester.request_raw = MagicMock(return_value=[b"BYTES", None])
        response, pk = self.requester.request(method="get", url="test")
        self.assertEqual(response, b"BYTES")
        self.assertEqual(pk, None)

        # Case 6: response is dict and has no data-attribute
        self.requester.request_raw = MagicMock(return_value=[{"sites": "1"}, "pk"])
        response, pk = self.requester.request(method="get", url="test")
        self.assertEqual(response, [{"sites": "1"}])
        self.assertEqual(pk, "pk")

        # Case 7: first JSON, then byte response – no real world case
        self.requester.request_raw = MagicMock(
            side_effect=[
                [{"data": [{"id": "1"}]}, "pagination_key"],
                [b"BYTES", "pagination_key"],
            ]
        )
        self.assertRaises(
            APIException,
            lambda: self.requester.request(method="get", url="test", request_all=True),
        )

        # Case 8: No Data received
        self.requester.request_raw = MagicMock(return_value=[[], None])
        response, pk = self.requester.request(method="get", url="test")
        self.assertEqual(response, [])
        self.assertEqual(pk, None)

    def test_handle_error_response(self):
        self.assertRaises(
            AuthenticationException,
            lambda: self.requester.handle_error_response(
                response=Mock(status_code=401)
            ),
        )
        self.assertRaises(
            BadGatewayException,
            lambda: self.requester.handle_error_response(
                response=Mock(status_code=502)
            ),
        )
        self.assertRaises(
            GatewayTimeoutException,
            lambda: self.requester.handle_error_response(
                response=Mock(status_code=504)
            ),
        )
        self.assertRaises(
            ServiceUnavailableException,
            lambda: self.requester.handle_error_response(
                response=Mock(status_code=503)
            ),
        )
        self.assertRaises(
            APIHttpException,
            lambda: self.requester.handle_error_response(response=Mock(status_code=0)),
        )

    def test_request_headers(self):
        headers = self.requester.request_headers()
        self.assertEqual(
            headers, {"User-Agent": f"API Python Client/{ornitho.__version__}"}
        )

    def test_request_raw(self):
        # Case 1: GET Method
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                    "Transfer-Encoding": "chunked",
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            params={"test": "param"},
            body={"test": "filter"},
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")

        # Case 2: Other Method
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        response, pk = self.requester.request_raw(
            method="post", url="test", pagination_key="key", body={"test": "filter"}
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, None)

        # Case 3: Error
        self.requester.session.request = MagicMock(return_value=Mock(status_code=401))
        self.assertRaises(
            AuthenticationException,
            lambda: self.requester.request_raw(method="post", url="test"),
        )

        # Case 4: PDF
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={"Content-Type": "application/pdf", "Content-Length": 3},
                content=b"PDF",
            )
        )
        response, pk = self.requester.request_raw(
            method="post",
            url="test",
            pagination_key="key",
            body={"test": "filter"},
            short_version=True,
        )
        self.assertEqual(b"PDF", response)
        self.assertEqual(pk, None)

        # Case 5: Unhandled content type
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={"Content-Type": "application/foo", "Content-Length": 23},
                cotent=b'{"data": [{"id": "1"}]}',
            )
        )
        self.assertRaises(
            APIHttpException,
            lambda: self.requester.request_raw(method="post", url="test"),
        )

        # Case 6: No content type received
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={"Content-Length": 23},
                text=b'{"data": [{"id": "1"}]}',
            )
        )
        self.assertRaises(
            APIException,
            lambda: self.requester.request_raw(method="post", url="test"),
        )

        # Case 7: Date as parameter
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                    "Transfer-Encoding": "chunked",
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        test_date = datetime.now().date()
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            params={"test": test_date},
            short_version=True,
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")
        self.requester.session.request.assert_called_with(
            "get",
            f"ORNITHO_API_BASEtest?user_email=ORNITHO_USER_EMAIL&user_pw=ORNITHO_USER_PW&pagination_key=key&short_version=1&test={test_date.strftime('%d.%m.%Y')}",
            data=None,
            headers=APIRequester.request_headers(),
        )

        # Case 8: Unaware datetime as parameter
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                    "Transfer-Encoding": "chunked",
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        test_date = datetime.now()
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            params={"test": test_date},
            short_version=True,
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")
        self.requester.session.request.assert_called_with(
            "get",
            f"ORNITHO_API_BASEtest?user_email=ORNITHO_USER_EMAIL&user_pw=ORNITHO_USER_PW&pagination_key=key&short_version=1&test={test_date.replace(microsecond=0).strftime('%d.%m.%Y')}",
            data=None,
            headers=APIRequester.request_headers(),
        )

        # Case 10: Date as body parameter
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                    "Transfer-Encoding": "chunked",
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        test_date = datetime.now().date()
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            body={"test": test_date},
            short_version=True,
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")
        self.requester.session.request.assert_called_with(
            "get",
            f"ORNITHO_API_BASEtest?user_email=ORNITHO_USER_EMAIL&user_pw=ORNITHO_USER_PW&pagination_key=key&short_version=1",
            data=json.dumps({"test": test_date.strftime("%d.%m.%Y")}),
            headers=APIRequester.request_headers(),
        )

        # Case 11: Aware datetime as parameter
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                    "Transfer-Encoding": "chunked",
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        test_date = datetime.now(pytz.timezone("Europe/Berlin"))
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            params={"test": test_date},
            short_version=True,
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")
        self.requester.session.request.assert_called_with(
            "get",
            f"ORNITHO_API_BASEtest?user_email=ORNITHO_USER_EMAIL&user_pw=ORNITHO_USER_PW&pagination_key=key&short_version=1&test={test_date.replace(microsecond=0).astimezone(datetime.now().astimezone().tzinfo).replace(tzinfo=None).strftime('%d.%m.%Y')}",
            data=None,
            headers=APIRequester.request_headers(),
        )

        # Case 12: Unaware datetime as body parameter
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                    "Transfer-Encoding": "chunked",
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        test_date = datetime.now()
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            body={"test": test_date},
            short_version=True,
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")
        self.requester.session.request.assert_called_with(
            "get",
            f"ORNITHO_API_BASEtest?user_email=ORNITHO_USER_EMAIL&user_pw=ORNITHO_USER_PW&pagination_key=key&short_version=1",
            data=json.dumps(
                {"test": test_date.replace(microsecond=0).strftime("%d.%m.%Y")}
            ),
            headers=APIRequester.request_headers(),
        )

        # Case 13: Aware datetime as body parameter
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                    "Transfer-Encoding": "chunked",
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        test_date = datetime.now(pytz.timezone("Europe/Berlin"))
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            body={"test": test_date},
            short_version=True,
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")
        self.requester.session.request.assert_called_with(
            "get",
            f"ORNITHO_API_BASEtest?user_email=ORNITHO_USER_EMAIL&user_pw=ORNITHO_USER_PW&pagination_key=key&short_version=1",
            data=json.dumps(
                {"test": test_date.replace(microsecond=0).strftime("%d.%m.%Y")}
            ),
            headers=APIRequester.request_headers(),
        )

        # Case 14: HTML Content Type
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "Content-Type": "text/html; charset=UTF-8",
                    "Content-Length": 4,
                },
                text="HTML",
            )
        )
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            body={"test": "filter"},
            short_version=True,
        )
        self.assertEqual("HTML", response)
        self.assertEqual(pk, None)

        # Case 15: Boolean as parameter
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 23,
                    "Transfer-Encoding": "chunked",
                },
                text='{"data": [{"id": "1"}]}',
            )
        )
        test_bool = True
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            params={"test": test_bool},
            short_version=True,
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")
        self.requester.session.request.assert_called_with(
            "get",
            f"ORNITHO_API_BASEtest?user_email=ORNITHO_USER_EMAIL&user_pw=ORNITHO_USER_PW&pagination_key=key&short_version=1&test={1 if test_bool else 0}",
            data=None,
            headers=APIRequester.request_headers(),
        )

        # Case 16: First Line is not part of the JSON response (success)

        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 43,
                    "Transfer-Encoding": "chunked",
                },
                text='API message : Ihre Beobachtungsdaten wurden erfolgreich übermittelt, vielen Dank!\n{"data": [{"id": "1"}]}',
            )
        )
        response, pk = self.requester.request_raw(
            method="get",
            url="test",
            pagination_key="key",
            short_version=True,
        )
        self.assertEqual({"data": [{"id": "1"}]}, response)
        self.assertEqual(pk, "new_key")
        self.requester.session.request.assert_called_with(
            "get",
            f"ORNITHO_API_BASEtest?user_email=ORNITHO_USER_EMAIL&user_pw=ORNITHO_USER_PW&pagination_key=key&short_version=1",
            data=None,
            headers=APIRequester.request_headers(),
        )

        # Case 17: First Line is not part of the JSON response (error)
        self.requester.session.request = MagicMock(
            return_value=Mock(
                status_code=200,
                headers={
                    "pagination_key": "new_key",
                    "Content-Type": "application/json; charset=utf-8",
                    "Content-Length": 43,
                    "Transfer-Encoding": "chunked",
                },
                text='A very stupid line!\n{"data": [{"id": "1"}]}',
            )
        )
        self.assertRaises(
            APIException,
            lambda: self.requester.request_raw(
                method="get",
                url="test",
                pagination_key="key",
                short_version=True,
            ),
        )
