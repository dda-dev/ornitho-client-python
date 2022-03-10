# flake8: noqa
"""
    Ornitho
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    An ornitho API client
    :copyright: (c) 2019 by DDA
    :license: MIT, see LICENSE for more details.
"""
import logging
import os
from typing import Callable, Optional

import requests

from ornitho.api_exception import (
    APIConnectionException,
    APIException,
    APIHttpException,
    AuthenticationException,
    BadGatewayException,
    ContentTypeException,
    GatewayTimeoutException,
    ObjectNotFoundException,
    ServiceUnavailableException,
)
from ornitho.api_requester import APIRequester
from ornitho.model import (
    Detail,
    Entity,
    EstimationCode,
    Family,
    Field,
    FieldOption,
    Form,
    LocalAdminUnit,
    MapLayer,
    Media,
    ModificationType,
    Observation,
    Observer,
    Place,
    Precision,
    Protocol,
    Relation,
    RelationType,
    Right,
    Site,
    Source,
    Species,
    TaxonomicGroup,
    TerritorialUnit,
)

__version__ = "0.3.0"
__license__ = "MIT"


# Configuration variables

consumer_key: Optional[str] = None
consumer_secret: Optional[str] = None
user_email: Optional[str] = None
user_pw: Optional[str] = None
api_base: Optional[str] = None

app_info = None

cache_enabled: bool = False
cache_name: str = "ornitho_cache"
cache_backend: str = "sqlite"
cache_expire_after: int = 600
cache_filter_fn: Callable[[requests.Response], bool] = (
    lambda r: "pagination_key" not in r.headers.keys()
)
cache_redis_host: str = "localhost"
cache_redis_port: int = 6379
cache_redis_db: int = 0

log_level = os.environ.get("ORNITHO_LOG_LEVEL") or logging.WARNING
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
