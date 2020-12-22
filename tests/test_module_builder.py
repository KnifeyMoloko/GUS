from typing import Dict, List, Any

import pytest
from assertpy import soft_assertions, assert_that

from common.swagger_parser.swagger_parser import ParsedSwagger


class TestModuleBuilder:
    @pytest.fixture(scope="class")
    def parsed_swagger(self, mock_params: List[Dict[str, Any]]):
        path = "/test_path/test_module/"
        sorts = (("Id", "Id"), ("DescId", "-Id"))
        signature = "mock_param: str = None, " \
                    "sort: Literal['Id', '-Id'], " \
                    "mock_param_two: bool = False"
        return ParsedSwagger(path=path, sort=sorts, signature=signature)

    def test_module_builder(self):
        pass
