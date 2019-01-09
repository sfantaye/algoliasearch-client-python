from platform import python_version
from typing import Optional

from algoliasearch.configs import Config
from algoliasearch.helpers import Items
from algoliasearch.version import VERSION


class RequestOptions(object):
    def __init__(self, headers, query_parameters, timeouts, data):
        # type: (dict, dict, dict, dict) -> None

        self.headers = headers
        self.query_parameters = query_parameters
        self.timeouts = timeouts
        self.data = data

    @staticmethod
    def create(config, options=None):
        # type: (Config, Optional[dict]) -> RequestOptions

        version = str(python_version())  # type: ignore

        headers = {
            'X-Algolia-Application-Id': config.app_id,
            'X-Algolia-API-Key': config.api_key,
            'User-Agent': 'Algolia for Python (%s); Python (%s)' % (
                VERSION, version),
            'Content-Type': 'application/json',
        }

        timeouts = {
            'readTimeout': config.read_timeout,
            'writeTimeout': config.write_timeout,
            'connectTimeout': config.connect_timeout,
        }

        request_options = RequestOptions(headers, {}, timeouts, {})

        for option, value in Items.get(options):
            if option in Params.HEADERS:
                request_options.headers[option] = value
            elif option in Params.QUERY_PARAMETERS:
                request_options.query_parameters[option] = value
            elif option in Params.TIMEOUTS:
                request_options.timeouts[option] = value
            else:
                request_options.data[option] = value

        return request_options


class Params(object):
    HEADERS = [
        'Content-type',
        'User-Agent',
    ]

    QUERY_PARAMETERS = [
        'createIfNotExists',
        'forwardToReplicas',
        'replaceExistingSynonyms',
        'clearExistingRules',
        'getVersion',
    ]

    TIMEOUTS = [
        'readTimeout',
        'writeTimeout',
        'connectTimeout',
    ]
