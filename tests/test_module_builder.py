import os

import pytest
from assertpy import assert_that

from common.elements.paths import GUSEndpoint, GUSPath
from common.module_builder.builder import GUSModuleBuilder
from common.swagger_parser.swagger_parser import read_swagger
from tests import test_data


class TestModuleBuilder:
    TEST_SWAGGER = "test_swagger.json"

    @pytest.fixture(scope="class")
    def parsed_swagger(self) -> GUSPath:
        root_path = read_swagger(package=test_data, resource=self.TEST_SWAGGER)
        print("Root path: %s", root_path.name)
        return root_path

    def test_build_endpoint_modules(self, parsed_swagger):
        endpoint: GUSEndpoint = None
        module_builder = GUSModuleBuilder(parsed_swagger)
        module_builder.buld_modules()
        expected_module_names = []
        # TODO: filter out module names (ending with .py)
        actual_module_names = os.walk("./root", topdown=True)

        assert_that(expected_module_names).is_equal_to(actual_module_names)

    def test_build_dir_hierarchy(self, parsed_swagger):
        assert_that(False).is_true()

    def test_construct_endpoint_constructs_correct_api_method(self, parsed_swagger):
        assert_that(False).is_true()

    def test_construct_api_path_registeres_all_endpoints(self, parsed_swagger):
        assert_that(False).is_true()

    def test_construct_api_path_registeres_subpaths(self, parsed_swagger):
        assert_that(False).is_true()
