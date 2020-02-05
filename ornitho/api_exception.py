from requests import Response


class APIException(Exception):
    """Base API exception class"""

    def __init__(self, response: Response,) -> None:
        """API Exception constructor"""
        super(APIException, self).__init__(response)

        self.response: Response = response

    def __str__(self) -> str:
        """Readable string representation"""
        return self.reason or "<empty message>"

    def __repr__(self) -> str:
        """Unambiguous string representation"""
        return f"{self.__class__.__name__}(http_status={self.http_status}, reason='{self.reason}', body='{self.body}')"

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


class APIConnectionException(APIException):
    """Exception class indicating an connection error"""


class AuthenticationException(APIException):
    """Exception class indicating failed authentication"""


class GatewayTimeoutException(APIException):
    """Exception class indicating a gateway timeout error"""
