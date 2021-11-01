import logging

import pytest
from assertpy import assert_that, soft_assertions

import config
from common.swagger_parser.swagger_parser import (
    download_swagger,
    read_swagger,
    ParsedSwagger,
)
from config import config_path

logger = logging.getLogger(__name__)


class TestSwaggerParser:
    test_swagger_dl_path = config_path / "test_swagger_dl.json"
    test_swagger_path = config_path / "test_swagger.json"

    @pytest.fixture(scope="class")
    def download_test_swagger(self) -> None:
        if not self.test_swagger_path.exists():
            download_swagger(path=self.test_swagger_path)

    @pytest.fixture(scope="function")
    def delete_local_test_swagger_file(self) -> None:
        logger.info(
            "Deleting local test swagger file at location: %s", self.test_swagger_path
        )
        if self.test_swagger_dl_path.exists():
            self.test_swagger_dl_path.unlink()

    def test_download_swagger(self, delete_local_test_swagger_file):
        # pylint: disable=unused-argument, no-self-use
        download_swagger(path=self.test_swagger_dl_path)
        assert_that(self.test_swagger_dl_path.is_file())

    def test_read_swagger(self, download_test_swagger):
        # pylint: disable=unused-argument, no-self-use
        parsed_swagger = read_swagger(package=config)

        logger.info("Parsed swagger is: %s", parsed_swagger)

        with soft_assertions():
            for signature_parser in parsed_swagger:
                assert_that(signature_parser).is_not_empty()
                assert_that(signature_parser).is_type_of(ParsedSwagger)
                assert_that(signature_parser.path).is_not_none()
                assert_that(signature_parser.signature).is_type_of(str)
                assert_that(signature_parser.signature).is_not_none()

                if signature_parser.sort:
                    assert_that(signature_parser.sort).is_type_of(tuple)
                    assert_that(signature_parser.sort).is_not_empty()

    def test_read_swagger_paths(self):
        # pylint: disable=no-self-use
        read_swagger(package=config)
