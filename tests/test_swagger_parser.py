import pytest
import logging
from assertpy import assert_that, soft_assertions
import config
from config import config_path
from common.swagger_parser.swagger_parser import download_swagger,\
    read_swagger
from common.swagger_parser.singature_parameter_builder import \
    SignatureParameterBuilder


logger = logging.getLogger(__name__)


class TestSwaggerParser:
    test_swagger_dl_path = config_path / "test_swagger_dl.json"
    test_swagger_path = config_path / "test_swagger.json"

    @pytest.fixture(scope="class")
    def download_test_swagger(self) -> None:
        if self.test_swagger_path.exists():
            return None
        else:
            download_swagger(path=self.test_swagger_path)

    @pytest.fixture(scope="function")
    def delete_local_test_swagger_file(self) -> None:
        logger.info(f"Deleting local test swagger file at location:"
                    f"{self.test_swagger_path}")
        if self.test_swagger_dl_path.exists():
            self.test_swagger_dl_path.unlink()

    def test_download_swagger(self, delete_local_test_swagger_file):
        download_swagger(path=self.test_swagger_dl_path)
        assert_that(self.test_swagger_dl_path.is_file())

    def test_read_swagger(self,
                          download_test_swagger):
        parsed_swagger = read_swagger(
            package=config,
            signature_parser_builder=SignatureParameterBuilder)
        assert_that(parsed_swagger).is_not_empty()
