import json
import logging
import re
from importlib.resources import read_binary, Package, Resource
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple, Union, NamedTuple, Optional

import requests  # type: ignore

from common.elements.paths import GUSPath, GUSEndpoint, RestMethods, EndpointProperties
from common.swagger_parser.singature_parameter_builder import SignatureParameterBuilder
from config import swagger_path

logger = logging.getLogger(__name__)


class ParsedSwagger(NamedTuple):
    path: str
    sort: tuple
    signature: str


def download_swagger(path: Path = swagger_path) -> None:

    logger.info("Downloading swagger file to path: %s", path)
    swagger_uri = "http://bdl.stat.gov.pl/api/v1/swagger/doc/swagger.json"
    with path.open(mode="w") as out_file:
        out_file.write(requests.get(swagger_uri).text)


def read_swagger(package: Package, resource: Resource) -> GUSPath:
    # pylint: disable=unused-variable
    swagger_json = __load_swagger_file(package=package, resource=resource)

    # create root GUSPath
    root = GUSPath(name="root", raw_path="/api/v1/")

    # register top-level paths as sub-paths to root
    __walk_path_tree(swagger_json, root)

    return root


def __walk_path_tree(swagger_json: dict[str, Any], root: GUSPath) -> GUSPath:
    paths = swagger_json["paths"]

    for path in paths:
        parent_path = root
        split_path = path.split("/")
        temp_path = ""

        for item in split_path:
            if len(item) == 0:
                continue

            temp_path = (
                f"{temp_path}/{item}" if temp_path != "/" else f"{temp_path}{item}"
            )
            new_path = GUSPath(
                name=temp_path.replace("-", "_").replace("/", "-").lstrip("-"),
                raw_path=temp_path,
            )

            if new_path.name in [path.name for path in parent_path.sub_paths]:
                new_path = [
                    path for path in parent_path.sub_paths if path.name == new_path.name
                ][0]

            if temp_path in paths.keys():
                try:
                    if "get" in paths[temp_path].keys():
                        endpoint_properties = EndpointProperties(
                            parameters=paths[temp_path]["get"].get("parameters", None),
                            produces=paths[temp_path]["get"].get("produces", None),
                            responses=paths[temp_path]["get"].get("responses", None),
                            summary=paths[temp_path]["get"].get("summary", None),
                            tags=paths[temp_path]["get"].get("tags", None),
                        )
                        new_path.register_endpoint(
                            GUSEndpoint(
                                name=new_path.name.split("-")[-1],
                                raw_path=temp_path,
                                method=RestMethods.get,
                                properties=endpoint_properties,
                            )
                        )
                except KeyError as key_exc:
                    logger.warning("Exception in constructing GUSEndpoint\n%s", key_exc)

                result = parent_path.register_subpath(new_path)
                if not result or parent_path.name == "root":
                    parent_path = new_path

            else:
                result = parent_path.register_subpath(new_path)
                if result:
                    parent_path = new_path
                else:
                    parent_path = [
                        path
                        for path in parent_path.sub_paths
                        if path.name == new_path.name
                    ][0]

    _walk_root_tree(root)
    # logger.info(root.sub_paths[0].sub_paths)
    return root


def _walk_root_tree(node: Union[GUSPath, GUSEndpoint], indent: int = 0):
    indentation = " " * indent
    name = (
        f"{indentation}get:{node.name}"
        if node.is_endpoint
        else f"{indentation}{node.name}"
    )
    logger.info(name)

    if not node.is_endpoint and node.endpoints:  # type: ignore
        temp_indent = indent + 2
        for endpoint in node.endpoints:  # type: ignore
            _walk_root_tree(endpoint, temp_indent)

    if not node.is_endpoint and node.sub_paths:  # type: ignore
        temp_indent = indent + 2
        for subpath in node.sub_paths:  # type: ignore
            _walk_root_tree(subpath, temp_indent)


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
