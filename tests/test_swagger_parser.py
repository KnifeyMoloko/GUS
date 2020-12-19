import pytest
import logging
import config
from assertpy import assert_that, soft_assertions
from config import config_path
from common.swagger_parser.swagger_parser import download_swagger, \
    __load_swagger_file


logger = logging.getLogger(__name__)


class TestSwaggerParser:
    test_swagger_path = config_path / "test_swagger.json"

    @pytest.fixture(scope="function")
    def delete_local_test_swagger_file(self) -> None:
        logger.info(f"Deleting local test swagger file at location:"
            f"{self.test_swagger_path}")
        if self.test_swagger_path.exists():
            self.test_swagger_path.unlink()
        yield
        if self.test_swagger_path.exists():
            self.test_swagger_path.unlink()

    def test_download_swagger(self, delete_local_test_swagger_file):
        download_swagger(path=self.test_swagger_path)
        assert_that(self.test_swagger_path.is_file())
