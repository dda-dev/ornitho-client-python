# flake8: noqa
"""
    Ornitho
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    An ornitho API client
    :copyright: (c) 2019 by Patrick Lindel
    :license: MIT, see LICENSE for more details.
"""
import logging
import os

from ornitho.api_exception import (
    APIConnectionException,
    APIException,
    AuthenticationException,
    GatewayTimeoutException,
)
from ornitho.api_requester import APIRequester
from ornitho.model import (
    ModificationType,
    Observation,
    Observer,
    Place,
    Species,
    TaxonomicGroup,
)

__version__ = "0.0.1"
__license__ = "MIT"


# Configuration variables

consumer_key = None
consumer_secret = None
user_email = None
user_pw = None
api_base = "https://www.ornitho.de/api/"

app_info = None


log_level = os.environ.get("ORNITHO_LOG_LEVEL") or logging.WARNING
logging.basicConfig(
    level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
