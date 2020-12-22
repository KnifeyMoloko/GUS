""" main file for the app orchestration """
import logging
from pprint import pprint

import config
from common.swagger_parser.singature_parameter_builder import \
    SignatureParameterBuilder
from common.swagger_parser.swagger_parser import read_swagger, \
    download_swagger
from common.builders.module_builder.module_builder import build_package_paths

logger = logging.getLogger(__name__)


def main():
    download_swagger()
    parsed_swaggers = read_swagger(
        package=config,
        signature_parser_builder=SignatureParameterBuilder)

    for ps in parsed_swaggers:
        build_package_paths(ps)
    # pprint(signature_list)
    # print(len(divide_and_sort(signature_list)))
    # pprint(divide_and_sort(signature_list))


if __name__ == "__main__":
    main()
