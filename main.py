""" main file for the app orchestration """
# imports
import logging
from ruamel.yaml import YAML


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.info("Working.")


if __name__ == "__main__":
    main()
