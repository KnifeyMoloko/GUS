import json
import requests
import re
import logging
from typing import Dict, Any, List, Optional, Set, Tuple, Union, Iterable
from pathlib import Path
from config import swagger_path
from importlib.resources import read_binary, Package, Resource
from dataclasses import dataclass, field, make_dataclass
from common.swagger_parser.singature_parameter_builder \
    import SignatureParameterBuilder


logger = logging.getLogger(__name__)


def download_swagger(path: Union[str, Path] = swagger_path) \
        -> None:
    logger.info(f"Downloading swagger file to path: {swagger_path}")
    swagger_uri = "http://bdl.stat.gov.pl/api/v1/swagger/doc/swagger.json"
    with swagger_path.open(mode="w") as out_file:
        out_file.write(requests.get(swagger_uri).text)


def read_swagger(
        package: Package,
        signature_parser_builder: SignatureParameterBuilder) -> List[str]:
    swagger_json = __load_swagger_file(package=package)
    # units_keys = load_swag["paths"]["/subjects"]["get"]
    signatures = []

    paths = __extract_paths_from_swagger_json(swagger_json)
    for key in paths:
        params = __extract_params(
            paths[key],
            signature_parser_builder)
        sorts = __extract_sorts(params)
        signature = __create_signature(params)
        signatures.append((key, signature))
    # TODO: replace the return type here with a NamedTuple with
    # a template_class_name, getter_func_name, path_name_etc
    return signatures


def __load_swagger_file(package: Package, resource: Resource = "swagger.json") \
        -> Dict[str, Any]:
    logger.info("Parsing the swagger json to a Python dict...")
    loaded = json.loads(read_binary(package=package, resource=resource)
                        .decode("utf-8"))
    return loaded


def __extract_paths_from_swagger_json(swagger_json: Dict[str, Any]) \
        -> Dict[str, Any]:
    logger.info("Extracting paths from parsed swagger json...")

    output = {}

    if not swagger_json.items():
        raise ValueError("Parsed swagger object was empty.")

    paths = swagger_json["paths"]
    for key in paths.keys():
        outer_values = paths[key]
        if "get" in outer_values:
            inner_values = outer_values["get"]
            output.update({key: inner_values})
    return output


def __extract_params(
        get_dict: Dict[str, Any],
        signature_parser_builder: SignatureParameterBuilder
) -> List[str]:
    params = get_dict["parameters"]
    output = []
    for param_dict in params:
        signature_parameter = signature_parser_builder(param_dict)
        output.append(signature_parameter.build_param())
    return output


def __extract_sorts(params: List[str]) \
        -> Tuple:

    for param in params:
        if "sort" in param:
            items = param.split("Literal")[1].split(" ")
            items_cleaned = [
                item
                .strip('[]')
                .replace('"', '') for item in items]
            items_annotated = [
                item
                .replace("-", "Desc")
                .replace(",", "_")
                .replace('"', '')
                .rstrip("_")
                for item in items_cleaned]
            zipped = tuple(zip(items_annotated, items_cleaned))
            return zipped


def __create_signature(params: List[str]) -> str:
    param_string = ", ".join(params)
    return param_string

# TODO: factor this out and possibly ammend the logic
# TODO: unit test this


def divide_and_sort(signature_list: List[Tuple[str, str]]) -> Set[str]:
    literals = []
    pattern = re.compile("[a-zA-z]*: Literal\[.+?\]")
    for name, signature_string in signature_list:
        if "Literal" in signature_string:
            # TODO: factor this out into a get_class_name_method
            # TODO: watch out with the replacement of {var} variables, they are query variables
            replaced = name.replace(
                "{", "/").replace("}", "").replace("-", "/")
            parsed_path_parts = replaced.lstrip("/").split("/")
            capitalized_path_parts = [path.capitalize()
                                      for path in parsed_path_parts]
            path_class_name = "".join(capitalized_path_parts)
            print(f"NAME: {path_class_name}")
            finds = pattern.findall(signature_string)
            # print(finds)
            literals += finds

    literal_set = set(literals)

    return literal_set
