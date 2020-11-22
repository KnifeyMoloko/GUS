"""
Helper function code for GUS.
Author: Maciej Cisowski
"""
import logging
from os import environ
from ruamel.yaml import YAML
from common import GUS_CONFIG_DIR
from ruamel.yaml.comments import CommentedMap


logger = logging.getLogger(__name__)


def get_env_vars() -> dict:
    return dict(environ)


def get_api_key() -> str:
    env_vars = get_env_vars()
    logger.info("Getting GUS_KEY from environment variables...")
    if "GUS_KEY" in env_vars.keys():
        return env_vars["GUS_KEY"]
    else:
        print(env_vars)
        raise ValueError("Did not find GUS_KEY in environment variables!")


def get_env_type() -> str:
    logger.info("Getting environment type from environment variables...")
    env_vars = get_env_vars()
    if "GUS_ENV" in env_vars.keys():
        logger.info(f"Using environment: {env_vars['GUS_ENV']}")
        return env_vars["GUS_ENV"]
    else:
        raise ValueError("Did not find GUS_ENV in environment variables!")


def get_config() -> CommentedMap:
    env_type = get_env_type()
    config_file = GUS_CONFIG_DIR / f"{env_type}.yml"
    if config_file.is_file():
        yaml = YAML()
        return yaml.load(config_file)
    else:
        raise FileNotFoundError(f"Did not find file at: {str(config_file)}")
