import pytest
import logging
from typing import List, Any, Dict
from assertpy import assert_that, soft_assertions
from common.swagger_parser.singature_parameter_builder import \
    SignatureParameterBuilder


logger = logging.getLogger(__name__)


class TestSignatureParametersBuilder:
    def test_ingest_path_dict(
            self,
            mock_params: List[Dict[str, Any]]):
        for param in mock_params:
            spb = SignatureParameterBuilder(params=param)

            with soft_assertions():
                members = [spb.name, spb.required,
                           spb.param_in, spb.param_type]
                for member in members:
                    assert_that(member).is_not_none()
                    assert_that(spb.param_format).is_none()
                    assert_that(spb.name).does_not_contain("-")

    def test_build(self, mock_params: List[Dict[str, Any]]):
        for param in mock_params:
            spb = SignatureParameterBuilder(params=param)
            spb_string = spb.build_param()
            logger.info(spb_string)

            with soft_assertions():
                assert_that(spb_string).is_not_empty()
                assert_that(spb_string).is_type_of(str)
