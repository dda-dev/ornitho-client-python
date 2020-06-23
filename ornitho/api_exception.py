from urllib.parse import parse_qs, urlsplit

from requests import Response


class APIException(Exception):
    """Base API exception class"""


class APIHttpException(APIException):
    """HTTP exception class"""

    def __init__(self, response: Response) -> None:
        """API Exception constructor"""
        super().__init__(response)
        self.response: Response = response

    def __str__(self) -> str:
        """Readable string representation"""
        return f"{self.path} with query {self.query} and body {self.request_body} responses with {self.http_status}: {self.reason}"

    def __repr__(self) -> str:
        """Unambiguous string representation"""
        return (
            f"{self.__class__.__name__}(http_status={self.http_status}, reason='{self.reason}', "
            f"body='{self.body}', path='{self.path}', query='{self.query}', request_body='{self.request_body}')"
        )

    @property
    def http_status(self) -> int:
        """HTTP return code"""
        return self.response.status_code

    @property
    def reason(self) -> str:
        """Textual HTTP code"""
        return self.response.reason

    @property
    def body(self) -> str:
        """Response body as string"""
        return self.response.text

    @property
    def path(self) -> str:
        """Path of the failed request"""
        return str(urlsplit(self.response.request.url).path)

    @property
    def query(self) -> dict:
        """Path of the failed request"""
        query = parse_qs(str(urlsplit(self.response.request.url).query))
        # Remove sensible data
        if "user_email" in query.keys():
            query["user_email"] = ["***"]
        if "user_pw" in query.keys():
            query["user_pw"] = ["***"]
        return query

    @property
    def request_body(self) -> str:
        """Path of the failed request"""
        return str(self.response.request.body)


class APIConnectionException(APIHttpException):
    """Exception class indicating an connection error"""


class AuthenticationException(APIHttpException):
    """Exception class indicating failed authentication"""


class GatewayTimeoutException(APIHttpException):
    """Exception class indicating a gateway timeout error"""


class ContentTypeException(APIHttpException):
    """Content Type exception"""

    def __str__(self) -> str:
        """Readable string representation"""
        return f"Unhandled Content-Typ '{self.content_type}' received! Received body: {self.body}"

    def __repr__(self) -> str:
        """Unambiguous string representation"""
        return f"{super().__repr__()}, content_type={self.content_type}"

    @property
    def content_type(self) -> str:
        """Path of the failed request"""
        return self.response.headers["Content-Type"]
