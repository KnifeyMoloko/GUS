from typing import Generator

import pytest
from assertpy import assert_that, soft_assertions

from common.elements.paths import Path


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
        # pylint: disable=no-self-use
        pass

    def test_endpoint_registration(self):
        # pylint: disable=no-self-use
        pass
