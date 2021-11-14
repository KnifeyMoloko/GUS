from typing import Generator

import pytest
from assertpy import assert_that, soft_assertions

from common.elements.paths import GUSPath, GUSEndpoint, RestMethods, EndpointProperties


class TestAPIPaths:
    @pytest.fixture(scope="function")
    def root_path(self) -> Generator[GUSPath, None, None]:
        # pylint: disable=no-self-use
        yield GUSPath("root", "/v1/")

    @pytest.fixture(scope="function")
    def new_endpoint(self) -> Generator[GUSEndpoint, None, None]:
        # pylint: disable=no-self-use
        properties = EndpointProperties(
            parameters=[
                {
                    "description": "Id atrybutu / " "Attribute Id",
                    "format": "int32",
                    "in": "path",
                    "name": "id",
                    "required": True,
                    "type": "integer",
                },
                {
                    "description": "Oczekiwany język "
                    "odpowiedzi - "
                    "opcjonalny "
                    "(jeśli podano "
                    "parametr, "
                    "nagłówek "
                    '"Accept-Language" '
                    "jest ignorowany) "
                    "/ Expected "
                    "response conent "
                    "language - "
                    "optional (if "
                    "parameter "
                    "specified, "
                    "request header "
                    '"Accept-Language" '
                    "is ignored)",
                    "enum": ["pl", "en"],
                    "in": "query",
                    "name": "lang",
                    "required": False,
                    "type": "enum",
                },
                {
                    "description": "Oczekiwany "
                    "format "
                    "odpowiedzi - "
                    "opcjonalny "
                    "(jeśli podano "
                    "parametr, "
                    "nagłówek "
                    '"Accept" jest '
                    "ignorowany) / "
                    "Expected "
                    "response content "
                    "type - optional "
                    "(if parameter "
                    "specified, "
                    "request header "
                    '"Accept" is '
                    "ignored)",
                    "enum": ["json", "jsonapi", "xml"],
                    "in": "query",
                    "name": "format",
                    "required": False,
                    "type": "enum",
                },
                {
                    "description": "Oczekiwany język "
                    "odpowiedzi - "
                    "opcjonalny "
                    "(jeśli podano "
                    'parametr "lang", '
                    "nagłówek "
                    '"Accept-Language" '
                    "zostanie "
                    "ignorowany) / "
                    "Expected "
                    "response conent "
                    "language - "
                    "optional (if "
                    '"lang" parameter '
                    "is specified, "
                    "the "
                    '"Accept-Language" '
                    "header will be "
                    "ignored)",
                    "enum": ["pl", "en"],
                    "in": "header",
                    "name": "Accept-Language",
                    "required": False,
                    "type": "enum",
                },
                {
                    "description": "Oczekiwany "
                    "format "
                    "odpowiedzi - "
                    "opcjonalny "
                    "(jeśli podano "
                    "parametr "
                    '"format", '
                    "nagłówek "
                    '"Accept" '
                    "zostanie "
                    "zignorowany) / "
                    "Expected "
                    "response content "
                    "type - optional "
                    '(if the "format" '
                    "parameter is "
                    "specified, the "
                    '"Accept" header '
                    "will be ignored)",
                    "enum": [
                        "application/json",
                        "application/vnd.api+json",
                        "application/xml",
                    ],
                    "in": "header",
                    "name": "Accept",
                    "required": False,
                    "type": "enum",
                },
                {
                    "description": "Nagłówek "
                    "warunkowego "
                    "żadania "
                    "If-None-Match "
                    "(entity "
                    "tag)/Conditional "
                    "Requests header "
                    "If-None-Match "
                    "(entity tag)",
                    "in": "header",
                    "name": "If-None-Match",
                    "required": False,
                    "type": "string",
                },
                {
                    "description": "Nagłówek "
                    "warunkowego "
                    "żadania "
                    "If-Modified-Since/Conditional "
                    "Requests header "
                    "If-Modified-Since",
                    "in": "header",
                    "name": "If-Modified-Since",
                    "required": False,
                    "type": "string",
                },
            ],
            produces=[
                "application/json",
                "application/vnd.api+json",
                "application/xml",
            ],
            responses={
                "200": {
                    "description": "Success",
                    "headers": {
                        "Date": {
                            "description": "Server " "date " "and " "time",
                            "type": "string",
                        },
                        "ETag": {"description": "Entity " "tag", "type": "string"},
                        "X-Rate-Limit-Limit": {
                            "description": "Rate " "limit " "limit",
                            "type": "string",
                        },
                        "X-Rate-Limit-Remaining": {
                            "description": "Rate " "limit " "remaining",
                            "type": "string",
                        },
                        "X-Rate-Limit-Reset": {
                            "description": "Rate " "limit " "reset",
                            "type": "string",
                        },
                    },
                    "schema": {"$ref": "#/definitions/Year"},
                },
                "404": {
                    "description": "Not found",
                    "schema": {"$ref": "#/definitions/ErrorResponseMessage"},
                },
                "429": {
                    "description": "limit exceeded",
                    "schema": {"$ref": "#/definitions/LimitResponseMessage"},
                },
                "500": {
                    "description": "Error",
                    "schema": {"$ref": "#/definitions/ErrorResponseMessage"},
                },
            },
            summary="Rok o wybranym Id / Year with selected Id",
            tags=["Years"],
        )

        yield GUSEndpoint(
            name="get-something",
            raw_path="get-something/{id}",
            method=RestMethods.get,
            properties=properties,
        )

    def test_path_creation(self):
        # pylint: disable=no-self-use
        new_path = GUSPath("root", "/v1/")

        with soft_assertions():
            assert_that(new_path.name).is_true()
            assert_that(new_path.raw_path).is_true()
            assert_that(new_path.is_endpoint).is_false()
            assert_that(new_path.endpoints).is_empty()
            assert_that(new_path.sub_paths).is_empty()

    def test_subpath_registration(self, root_path: GUSPath):
        # pylint: disable=no-self-use, expression-not-assigned
        subpath_count = 10
        for i in range(subpath_count):
            root_path.register_subpath(GUSPath(str(i), "/" + str(i) + "/{id}}"))

        with soft_assertions():
            assert_that(len(root_path.sub_paths)).is_equal_to(subpath_count)
            for subpath in root_path.sub_paths:
                assert_that(subpath).is_type_of(GUSPath)
                assert_that(int(subpath.name)).is_in(*range(subpath_count))
                assert_that(subpath.raw_path).matches(r"\/\d\/{id\}")

    def test_endpoint_creation(self, new_endpoint: GUSEndpoint):
        # pylint: disable=no-self-use, expression-not-assigned
        name = "get-something"
        raw_path = "get-something/{id}"
        method = RestMethods.get

        with soft_assertions():
            assert_that(new_endpoint.name).is_equal_to(name)
            assert_that(new_endpoint.raw_path).is_equal_to(raw_path)
            assert_that(new_endpoint.method).is_equal_to(method)
            assert_that(new_endpoint.is_endpoint)

    def test_endpoint_registration(self, root_path: GUSPath, new_endpoint):
        # pylint: disable=no-self-use, expression-not-assigned
        root_path.register_endpoint(new_endpoint)

        with soft_assertions():
            assert_that(len(root_path.endpoints)).is_equal_to(1)

    def test_endpoint_properties(self, new_endpoint: GUSEndpoint):
        # pylint: disable=no-self-use, expression-not-assigned
        with soft_assertions():
            assert_that(new_endpoint.parameters).is_not_empty()
            assert_that(new_endpoint.parameters).is_type_of(list)
            params = new_endpoint.parameters
            for param in params:
                assert_that(param).is_type_of(dict)
                assert_that(param).is_not_empty()

            assert_that(new_endpoint.produces).is_not_empty()
            assert_that(new_endpoint.produces).is_type_of(list)
            produces = new_endpoint.produces
            for prod in produces:
                assert_that(prod).is_type_of(str)
                assert_that(prod).is_true()

            assert_that(new_endpoint.responses).is_type_of(dict)
            assert_that(new_endpoint.responses).is_not_empty()

            assert_that(new_endpoint.summary).is_type_of(str)
            assert_that(new_endpoint.summary).is_true()

            assert_that(new_endpoint.tags).is_type_of(list)
            tags = new_endpoint.tags
            for tag in tags:
                assert_that(tag).is_type_of(str)
                assert_that(tag).is_true()
