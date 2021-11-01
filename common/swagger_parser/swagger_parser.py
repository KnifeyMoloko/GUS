import json
import logging
import re
from importlib.resources import read_binary, Package, Resource
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple, Union, NamedTuple, Optional

import requests  # type: ignore

from common.swagger_parser.singature_parameter_builder import SignatureParameterBuilder
from config import swagger_path

logger = logging.getLogger(__name__)


class ParsedSwagger(NamedTuple):
    path: str
    sort: tuple
    signature: str


def download_swagger(path: Union[str, Path] = swagger_path) -> None:
    logger.info("Downloading swagger file to path: %s", path)
    swagger_uri = "http://bdl.stat.gov.pl/api/v1/swagger/doc/swagger.json"
    with swagger_path.open(mode="w") as out_file:
        out_file.write(requests.get(swagger_uri).text)


def read_swagger(package: Package) -> List[ParsedSwagger]:
    # pylint: disable=unused-variable
    swagger_json = __load_swagger_file(package=package)
    parsed_swaggers: list[Any] = []

    paths = __extract_paths_from_swagger_json(swagger_json)

    return parsed_swaggers


def __load_swagger_file(
    package: Package, resource: Resource = "swagger.json"
) -> Dict[str, Any]:
    logger.info("Parsing the swagger json to a Python dict...")
    loaded = json.loads(read_binary(package=package, resource=resource).decode("utf-8"))
    return loaded


def __extract_paths_from_swagger_json(swagger_json: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Extracting paths from parsed swagger json...")

    output: dict[str, Any] = {}

    if not swagger_json.items():
        raise ValueError("Parsed swagger object was empty.")

    paths = swagger_json["paths"]
    keys = []
    for key in paths.keys():
        # logger.info(f"\nKey: {key}\n")
        # logger.info(f"How many methods: {len(paths[key]['get'].keys())}")
        # logger.info(f"Path: {paths[key]}")
        keys.append(key)

    for key in keys:
        print(key)
    return output


def __extract_params(
    get_dict: Dict[str, Any], signature_parser_builder: SignatureParameterBuilder
) -> list[Optional[str]]:
    # pylint: disable=unused-variable
    params = get_dict["parameters"]
    output = []
    signature_parameter = signature_parser_builder
    output.append(signature_parameter.build_param())

    return output


def __extract_sorts(params: List[str]) -> Tuple:
    for param in params:
        if "sort" in param:
            items = param.split("Literal")[1].split(" ")
            items_cleaned = [item.strip("[]").replace('"', "") for item in items]
            items_annotated = [
                item.replace("-", "Desc").replace(",", "_").replace('"', "").rstrip("_")
                for item in items_cleaned
            ]
            zipped = tuple(zip(items_annotated, items_cleaned))
    return zipped


def __create_signature(params: List[str]) -> str:
    param_string = ", ".join(params)
    return param_string


def divide_and_sort(signature_list: List[Tuple[str, str]]) -> Set[str]:
    literals = []
    pattern = re.compile(r"[a-zA-z]*: Literal\[.+?\]")
    for name, signature_string in signature_list:
        if "Literal" in signature_string:
            replaced = name.replace("{", "/").replace("}", "").replace("-", "/")
            parsed_path_parts = replaced.lstrip("/").split("/")
            capitalized_path_parts = [path.capitalize() for path in parsed_path_parts]
            path_class_name = "".join(capitalized_path_parts)
            print(f"NAME: {path_class_name}")
            finds = pattern.findall(signature_string)
            # print(finds)
            literals += finds

    literal_set = set(literals)

    return literal_set
