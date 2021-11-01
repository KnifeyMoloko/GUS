from typing import Generator

import pytest
from assertpy import assert_that, soft_assertions

from common.elements.paths import Path, Endpoint, RestMethods


class TestAPIPaths:
    @pytest.fixture(scope="function")
    def root_path(self) -> Generator[Path, None, None]:
        # pylint: disable=no-self-use
        yield Path("root", "/v1/")

    def test_path_creation(self):
        # pylint: disable=no-self-use
        new_path = Path("root", "/v1/")

        with soft_assertions():
            assert_that(new_path.name).is_true()
            assert_that(new_path.raw_path).is_true()
            assert_that(new_path.is_endpoint).is_false()
            assert_that(new_path.endpoints).is_empty()
            assert_that(new_path.sub_paths).is_empty()

    def test_subpath_registration(self, root_path: Path):
        # pylint: disable=no-self-use, expression-not-assigned
        subpath_count = 10
        for i in range(subpath_count):
            root_path.register_subpath(Path(str(i), "/" + str(i) + "/{id}}"))

        with soft_assertions():
            assert_that(len(root_path.sub_paths)).is_equal_to(subpath_count)
            for subpath in root_path.sub_paths:
                assert_that(subpath).is_type_of(Path)
                assert_that(int(subpath.name)).is_in(*range(subpath_count))
                assert_that(subpath.raw_path).matches(r"\/\d\/{id\}")

    def test_endpoint_creation(self):
        # pylint: disable=no-self-use, expression-not-assigned
        name = "get-something"
        raw_path = "get-something/{id}"
        method = RestMethods.get
        new_endpoint = Endpoint(name=name, raw_path=raw_path, method=method)

        with soft_assertions():
            assert_that(new_endpoint.name).is_equal_to(name)
            assert_that(new_endpoint.raw_path).is_equal_to(raw_path)
            assert_that(new_endpoint.method).is_equal_to(method)
            assert_that(new_endpoint.is_endpoint)

    def test_endpoint_registration(self, root_path: Path):
        # pylint: disable=no-self-use, expression-not-assigned
        new_endpoint = Endpoint(
            name="get-something", raw_path="get-something/{id}", method=RestMethods.get
        )
        root_path.register_endpoint(new_endpoint)

        with soft_assertions():
            assert_that(len(root_path.endpoints)).is_equal_to(1)
