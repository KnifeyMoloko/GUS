"""
Test for the common package of GUS.
Author: Maciej Cisowski (KnifeyMoloko)
"""
from assertpy import assert_that, soft_assertions
from common.helpers import get_env_vars, get_api_key, \
    get_env_type, get_config
from ruamel.yaml.comments import CommentedMap
from rest.gus_rest_client import GUSClient


def test_env_vars_are_not_empty():
    assert_that(get_env_vars()).is_not_empty()


def test_get_api_key():
    acutal = get_api_key()
    with soft_assertions():
        assert_that(acutal).is_not_none()
        assert_that(acutal).is_type_of(str)
        assert_that(len(acutal)).is_greater_than(1)


def test_get_env_type():
    assert_that(get_env_type()).is_equal_to("test")


def test_get_config():
    config = get_config()
    with soft_assertions():
        assert_that(config).is_not_empty()
        assert_that(config).is_type_of(CommentedMap)
        assert_that(config['version']).is_equal_to(1)
