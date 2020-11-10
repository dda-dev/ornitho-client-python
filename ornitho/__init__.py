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
from typing import Optional

from ornitho.api_exception import (
    APIConnectionException,
    APIException,
    APIHttpException,
    AuthenticationException,
    ContentTypeException,
    GatewayTimeoutException,
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
    Site,
    Source,
    Species,
    TaxonomicGroup,
    TerritorialUnit,
)

__version__ = "0.1.0"
__license__ = "MIT"


# Configuration variables

consumer_key: Optional[str] = None
consumer_secret: Optional[str] = None
user_email: Optional[str] = None
user_pw: Optional[str] = None
api_base: Optional[str] = None

app_info = None


log_level = os.environ.get("ORNITHO_LOG_LEVEL") or logging.WARNING
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
