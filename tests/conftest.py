from typing import List, Dict, Any

import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def mock_path() -> Dict[str, Any]:
    mock_path = {
        r"mockAggregate/mockSubpath/mockSubSubpath/{var}":
            {'tags': ['Aggregates'],
             'summary': 'Metadane / Metadata',
             'operationId': 'GetAggregatesMetadata',
             'consumes': [],
             'produces': ['application/json', 'application/xml'],
             'parameters': [
                 {
                     'name': 'lang',
                     'in': 'query',
                     'description': 'Oczekiwany język odpowiedzi - opcjonalny (jeśli podano parametr, nagłówek "Accept-Language" jest ignorowany) / Expected response conent language - optional (if parameter specified, request header "Accept-Language" is ignored)',
                     'required': False,
                     'type': 'enum', 'enum': ['pl', 'en']
                 },
                 {
                     'name': 'format',
                     'in': 'query',
                     'description': 'Oczekiwany format odpowiedzi - opcjonalny (jeśli podano parametr, nagłówek "Accept" jest ignorowany) / Expected response content type - optional (if parameter specified, request header "Accept" is ignored)',
                     'required': False,
                     'type': 'enum',
                     'enum': ['json', 'xml']
                 },
                 {
                     'name': 'Accept-Language',
                     'in': 'header',
                     'description': 'Oczekiwany język odpowiedzi - opcjonalny (jeśli podano parametr "lang", nagłówek "Accept-Language" zostanie ignorowany) / Expected response conent language - optional (if "lang" parameter is specified, the "Accept-Language" header will be ignored)',
                     'required': False,
                     'type': 'enum',
                     'enum': ['pl', 'en']
                 },
                 {
                     'name': 'Accept',
                     'in': 'header',
                     'description': 'Oczekiwany format odpowiedzi - opcjonalny (jeśli podano parametr "format", nagłówek "Accept" zostanie zignorowany) / Expected response content type - optional (if the "format" parameter is specified, the "Accept" header will be ignored)',
                     'required': False,
                     'type':
                         'enum',
                     'enum': ['application/json', 'application/xml']
                 },
                 {
                     'name':
                         'If-None-Match',
                     'in': 'header',
                     'description': 'Nagłówek warunkowego żadania If-None-Match (entity tag)/Conditional Requests header If-None-Match (entity tag)',
                     'required': False,
                     'type': 'string'
                 },
                 {
                     'name': 'If-Modified-Since',
                     'in': 'header',
                     'description': 'Nagłówek warunkowego żadania If-Modified-Since/Conditional Requests header If-Modified-Since',
                     'required': False,
                     'type': 'string'
                 }
             ],
             'responses': {'200': {'description': 'Success', 'schema': {'$ref': '#/definitions/Metadata'},
                                   'headers': {'ETag': {'description': 'Entity tag', 'type': 'string'},
                                               'Date': {'description': 'Server date and time', 'type': 'string'},
                                               'X-Rate-Limit-Limit': {'description': 'Rate limit limit',
                                                                      'type': 'string'},
                                               'X-Rate-Limit-Remaining': {'description': 'Rate limit remaining',
                                                                          'type': 'string'},
                                               'X-Rate-Limit-Reset': {'description': 'Rate limit reset',
                                                                      'type': 'string'}}},
                           '429': {'description': 'limit exceeded',
                                   'schema': {'$ref': '#/definitions/LimitResponseMessage'}}}
             }
    }
    return mock_path


@pytest.fixture(scope="session")
def mock_params(mock_path: Dict[str, Any]) \
        -> List[Dict[str, Any]]:
    mock_key = list(mock_path.keys())[0]
    mock_params = mock_path[mock_key]["parameters"]
    return mock_params
