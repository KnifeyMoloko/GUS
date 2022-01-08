import logging

import pytest
from assertpy import assert_that, soft_assertions

import config
from common.elements.paths import GUSPath
from common.swagger_parser.swagger_parser import (
    download_swagger,
    read_swagger,
)
from config import config_path

logger = logging.getLogger(__name__)


class TestSwaggerParser:
    test_swagger_file = "test_swagger.json"
    test_swagger_path = config_path / test_swagger_file

    @pytest.fixture(scope="class")
    def download_test_swagger(self) -> None:
        if not self.test_swagger_path.exists():
            download_swagger(path=self.test_swagger_path)

    @pytest.fixture(scope="function", autouse=True)
    def delete_local_test_swagger_file(self):
        yield
        if self.test_swagger_path.exists():
            logger.info(
                "Deleting local test swagger file at location: %s",
                self.test_swagger_path,
            )
            self.test_swagger_path.unlink()

    def test_download_swagger(self, delete_local_test_swagger_file):
        # pylint: disable=unused-argument, no-self-use
        download_swagger(path=self.test_swagger_path)
        assert_that(self.test_swagger_path.is_file())

    def test_read_swagger_paths(self, download_test_swagger):
        # pylint: disable=unused-argument, no-self-use
        root_path = read_swagger(package=config, resource=self.test_swagger_file)
        with soft_assertions():
            sub_paths = root_path.sub_paths
            endpoints = root_path.endpoints
            assert_that(root_path).is_instance_of(GUSPath)
            assert_that(sub_paths).is_not_empty()
            assert_that(endpoints).is_empty()

            for sub_path in sub_paths:
                assert_that(sub_path).is_instance_of(GUSPath)

            units = [path for path in root_path.sub_paths if path.name == "units"][0]
            localities = [
                path for path in units.sub_paths if path.name == "units-localities"
            ][0]
            by_id = [
                path
                for path in localities.sub_paths
                if path.name == "units-localities-{id}"
            ][0]
            print(by_id.endpoints)
            by_id_endpoints = by_id.endpoints
            assert_that(len(by_id_endpoints)).is_equal_to(1)
            # assert_that(by_id_endpoints[0]).is_instance_of(GUSEndpoint)
