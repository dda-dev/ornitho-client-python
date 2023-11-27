import json
from copy import deepcopy
from datetime import date, datetime
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from urllib.parse import urlencode

from requests import Response
from requests_oauthlib import OAuth1Session

import ornitho
from ornitho import api_exception

try:
    import requests_cache

    class CachedOAuthSession(
        requests_cache.CacheMixin, OAuth1Session
    ):  # pragma: no cover
        """Session with features from both CachedSession and OAuth1Session"""

except ImportError:  # pragma: no cover
    requests_cache = cast(Any, None)


class APIRequester(object):
    """Class for making API requests"""

    def __init__(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        user_email: Optional[str] = None,
        user_pw: Optional[str] = None,
        api_base: Optional[str] = None,
    ) -> None:
        """API requester constructor
        :param consumer_key: Optional Consumer Key, overrides field from ornitho module (ornitho.consumer_key)
        :param consumer_secret: Optional Consumer Secret, overrides field from ornitho module (ornitho.consumer_secret)
        :param user_email: Optional User Mail, overrides field from ornitho module (ornitho.user_email)
        :param user_pw: Optional User Password, overrides field from ornitho module (ornitho.user_pw)
        :param api_base: Optional API base url, overrides field from ornitho module (ornitho.api_base)
        :type consumer_key: Optional[str]
        :type consumer_secret: Optional[str]
        :type user_email: Optional[str]
        :type user_pw: Optional[str]
        :type api_base: Optional[str]
        """
        self.consumer_key: Optional[str] = consumer_key or ornitho.consumer_key
        self.consumer_secret: Optional[str] = consumer_secret or ornitho.consumer_secret
        self.user_email: Optional[str] = user_email or ornitho.user_email
        self.user_pw: Optional[str] = user_pw or ornitho.user_pw
        self.api_base: Optional[str] = api_base or ornitho.api_base
        if not self.consumer_key:
            raise RuntimeError("consumer_key missing!")
        if not self.consumer_secret:
            raise RuntimeError("consumer_secret missing!")
        if not self.user_email:
            raise RuntimeError("user_email missing!")
        if not self.user_pw:
            raise RuntimeError("user_pw missing!")
        if not self.api_base:
            raise RuntimeError("api_base missing!")

        if ornitho.cache_enabled and requests_cache:  # pragma: no cover
            if ornitho.cache_backend == "redis":
                import redis

                r = redis.StrictRedis(
                    host=ornitho.cache_redis_host,
                    port=ornitho.cache_redis_port,
                    db=ornitho.cache_redis_db,
                )
                self.session: OAuth1Session = CachedOAuthSession(
                    client_key=self.consumer_key,
                    client_secret=self.consumer_secret,
                    cache_name=ornitho.cache_name,
                    backend=ornitho.cache_backend,
                    expire_after=ornitho.cache_expire_after,
                    filter_fn=ornitho.cache_filter_fn,
                    connection=r,
                )
            else:
                self.session = CachedOAuthSession(
                    client_key=self.consumer_key,
                    client_secret=self.consumer_secret,
                    cache_name=ornitho.cache_name,
                    backend=ornitho.cache_backend,
                    expire_after=ornitho.cache_expire_after,
                    filter_fn=ornitho.cache_filter_fn,
                )
        else:
            if ornitho.cache_enabled:  # pragma: no cover
                ornitho.logger.warning(
                    "Cache was enabled but caching dependency is not install. Please install 'requests_cache'"
                )
            self.session = OAuth1Session(
                client_key=self.consumer_key, client_secret=self.consumer_secret
            )

    def __enter__(self):
        """Used by a with-statement"""
        return self

    def __exit__(self, *args):
        """Used by a with-statement"""
        self.close()

    def close(self):
        """Close an OAuth1 Session"""
        self.session.close()

    def request(
        self,
        method: str,
        url: str,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        request_all: bool = False,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        retries: int = 0,
    ) -> Tuple[Union[bytes, List[Dict[str, str]]], Optional[str]]:
        """Make requests to the API
        If request_all ist set, several requests calls to the API can be made, until all data is retrieved. Else a
        pagination key will be returned, which can be used to get the next data set.
        :param method: HTTP Method e.g. 'GET'
        :param url: API URL to call
        :param pagination_key: Additional pagination key, to get the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
            Default: 'False'
        :param request_all:  Indicates, if all pages should be returned. May result in many API calls. Default: 'False'
        :param params: Additional URL parameters.
        :param body: Request body
        :param retries: Indicates how many retries should be performed
        :type method: str
        :type url: str
        :type pagination_key: str
        :type short_version: bool
        :type request_all: bool
        :type params: Dict[str, Any]
        :type body: Dict[str, Any]
        :type retries: int
        :return: Tuple of raw data list and pagination key
        :rtype: Tuple[List[Dict[str, str]], Optional[str]]
        """
        data: List[Dict[str, str]] = []
        responds, pk = self.request_raw(
            method=method.lower(),
            url=url,
            pagination_key=pagination_key,
            short_version=short_version,
            params=params,
            body=body,
            retries=retries,
        )
        if isinstance(responds, bytes):
            return responds, pk
        elif isinstance(responds, list):
            data += responds
        elif isinstance(responds, dict) and "data" in responds.keys():
            if isinstance(responds["data"], dict):
                if "sightings" in responds["data"]:
                    data += responds["data"]["sightings"]
                if "forms" in responds["data"]:
                    for form in responds["data"]["forms"]:
                        day = deepcopy(form["sightings"][0]["date"])
                        form_copy_wihtout_sightings = deepcopy(form)
                        form_copy_wihtout_sightings["day"] = day
                        del form_copy_wihtout_sightings["sightings"]
                        for sighting in form["sightings"]:
                            sighting["form"] = form_copy_wihtout_sightings
                            data.append(sighting)
            else:
                data += responds["data"]
        else:
            data.append(responds)

        ornitho.logger.info("Received %s data objects" % (len(data)))

        if pk and request_all and len(data) > 0:
            next_response = self.request(
                method=method,
                url=url,
                pagination_key=pk,
                short_version=short_version,
                request_all=request_all,
                params=params,
                body=body,
                retries=retries,
            )[0]
            if isinstance(next_response, bytes):
                raise api_exception.APIException(
                    "Received bytes content, where json was expected"
                )
            data = data + next_response
        if not pagination_key and len(data) <= 0:
            ornitho.logger.debug(
                "No data received! This can be caused by wrong parameter or an error in ornitho."
            )

        return data, pk

    @staticmethod
    def handle_error_response(response: Response) -> None:
        """Check the error response and raises a proper exception
        :param response: Erroneous response, received from the API
        :type response: Response
        :raise APIHttpException: Response contains unhandled HTTP Code
        :raise AuthenticationException: Authentication failed, wrong credentials?
        :raise BadGatewayException: Unknown Server error, in most cases a retry is successful
        :raise GatewayTimeoutException: Request took to long, reduce possible response by adding filters
        :raise ServiceUnavailableException: Service unavailable, in most cases a retry is successful
        """
        if response.status_code == 401:
            raise api_exception.AuthenticationException(response)
        elif response.status_code == 502:
            raise api_exception.BadGatewayException(response)
        elif response.status_code == 503:
            raise api_exception.ServiceUnavailableException(response)
        elif response.status_code == 504:
            raise api_exception.GatewayTimeoutException(response)
        else:
            raise api_exception.APIHttpException(response)

    @staticmethod
    def request_headers() -> Dict[str, str]:
        """Generate header information, like 'User-Agent'
        :return: Header information
        :rtype: Dict[str, str]
        """
        user_agent = f"API Python Client/{ornitho.__version__}"
        headers = {"User-Agent": user_agent}
        return headers

    def request_raw(
        self,
        method: str,
        url: str,
        pagination_key: Optional[str] = None,
        short_version: bool = False,
        params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
        retries: int = 0,
    ) -> Tuple[Any, Any]:
        """Make direct request to the API
        :param method: HTTP Method e.g. 'GET'
        :param url: API URL to call
        :param pagination_key: Additional pagination key, to get the next page
        :param short_version: Indicates, if a short version with foreign keys should be returned by the API.
            Default: 'False'
        :param params: Additional URL parameters.
        :param body: Request body
        :param retries: Indicates how many retries should be performed
        :type method: str
        :type url: str
        :type pagination_key: str
        :type short_version: bool
        :type params: Dict[str, Any]
        :type body: Dict[str, Any]
        :type retries: int
        :return: Tuple of raw response data and pagination key
        :rtype: Tuple[Any, Any]
        :raise APIConnectionError: Unspecified error while connecting to Biolovision
        :raise APIException: Response contains unhandled HTTP Code
        :raise AuthenticationException: Authentication failed, wrong credentials?
        :raise GatewayTimeoutException: Request took to long, reduce possible response by adding filters
        :raise BadGatewayException: Unknown Server error, in most cases a retry is successful
        :raise ServiceUnavailableException: Service unavailable, in most cases a retry is successful
        :raise ContentTypeException: Unhandled Content Type received or no information about content typ found
        """

        params_dict: Dict[str, Any] = {
            "user_email": self.user_email,
            "user_pw": self.user_pw,
        }

        if pagination_key:
            params_dict["pagination_key"] = pagination_key

        if short_version:
            params_dict["short_version"] = 1

        if params:
            for key, value in params.items():
                if isinstance(value, bool):
                    value = 1 if value else 0
                    params[key] = value
                elif isinstance(value, datetime):
                    value = value.replace(microsecond=0)
                    if value.tzinfo:
                        value = value.astimezone(
                            datetime.now().astimezone().tzinfo
                        ).replace(tzinfo=None)
                    # ISO Format (especially time) is accepted but mostly ignored – only known exception is /observations/diff
                    # body[key] = value.replace(microsecond=0).isoformat()
                    # value = value.isoformat()
                    value = value.strftime("%d.%m.%Y")
                    params[key] = value
                elif isinstance(value, date):
                    value = value.strftime("%d.%m.%Y")
                    params[key] = value
                params_dict[key] = value

        abs_url = f"{self.api_base}{url}?{urlencode(params_dict)}"

        if body:
            for key, value in body.items():
                if isinstance(value, datetime):
                    # ISO Format (especially time) is accepted but mostly ignored
                    # body[key] = value.replace(microsecond=0).isoformat()
                    value = value.replace(microsecond=0)
                    if value.tzinfo:
                        value = value.astimezone(
                            datetime.now().astimezone().tzinfo
                        ).replace(tzinfo=None)
                    body[key] = value.strftime("%d.%m.%Y")
                elif isinstance(value, date):
                    body[key] = value.strftime("%d.%m.%Y")

        data = json.dumps(body) if body else None

        headers = self.request_headers()
        ornitho.logger.info(
            f"Request to Ornitho api. method={method}, url=/{url}, params={params}, short_version={short_version}, body={body}"
        )
        raw_response = self.session.request(method, abs_url, data=data, headers=headers)

        if not 200 <= raw_response.status_code < 300:
            if retries > 0:
                ornitho.logger.warning(
                    f"Response {raw_response.status_code}. {retries} left! Retry..."
                )
                return self.request_raw(
                    method=method,
                    url=url,
                    pagination_key=pagination_key,
                    short_version=short_version,
                    params=params,
                    body=body,
                    retries=retries - 1,
                )
            self.handle_error_response(raw_response)

        if (
            "pagination_key" in raw_response.headers.keys()
            and "Transfer-Encoding" in raw_response.headers.keys()
            and raw_response.headers["Transfer-Encoding"] == "chunked"
        ):
            pagination_key = raw_response.headers["pagination_key"] or None
        else:
            pagination_key = None

        if method == "delete":
            return raw_response.text, pagination_key
        elif "Content-Type" in raw_response.headers.keys():
            if raw_response.headers["Content-Type"].startswith("application/json"):
                raw_response_text = raw_response.text
                # Remove the first JSON Line, which breaks the JSON format
                # Hopefully there aren't any more success messages
                # A real WTF moment...
                # TODO Add other language checks
                if (
                    raw_response_text.split("\n")[0]
                    == "API message : Ihre Beobachtungsdaten wurden erfolgreich übermittelt, vielen Dank!"
                ):
                    raw_response_text = "\n".join(raw_response_text.split("\n")[1:])
                try:
                    decoded_json_response = json.loads(raw_response_text or "{}")
                except JSONDecodeError:
                    raise api_exception.APIException(
                        f"Cant decode the response as JSON:\n{raw_response_text}"
                    )
                return decoded_json_response, pagination_key
            elif raw_response.headers["Content-Type"] == "application/pdf":
                return raw_response.content, pagination_key
            elif raw_response.headers["Content-Type"] == "text/html; charset=UTF-8":
                return raw_response.text, pagination_key
            else:
                raise api_exception.ContentTypeException(raw_response)
        else:
            raise api_exception.ContentTypeException(raw_response)
