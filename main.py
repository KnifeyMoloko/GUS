""" main file for the app orchestration """
# imports
import logging
from ruamel.yaml import YAML
import config
from common.swagger_parser import read_swagger


def main():
    read_swagger(config)


if __name__ == "__main__":
    main()
