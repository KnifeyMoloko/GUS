""" main file for the app orchestration """
# imports
import config
from pprint import pprint
import logging
from common.swagger_parser.swagger_parser import read_swagger, \
    download_swagger, divide_and_sort
from common.swagger_parser.singature_parameter_builder import \
    SignatureParameterBuilder


logger = logging.getLogger(__name__)


def main():
    download_swagger()
    signature_list = read_swagger(
        package=config,
        signature_parser_builder=SignatureParameterBuilder)
    # pprint(signature_list)
    # print(len(divide_and_sort(signature_list)))
    # pprint(divide_and_sort(signature_list))


if __name__ == "__main__":
    main()
