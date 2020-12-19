import json
import requests
import re
import logging
from typing import Dict, Any, List, Optional, Set, Tuple, Union
from pathlib import Path
from config import swagger_path
from importlib.resources import read_binary, Package, Resource
from dataclasses import dataclass, field


logger = logging.getLogger(__name__)


type_map = {
    "string": "str",
    "integer": "int",
    "enum": "Literal",
    "array": "List"
}


@dataclass
class SignatureParameter:
    params: Dict[str, Any] = field(init=True, repr=False)
    name: str = field(init=False)
    required: bool = field(init=False)
    param_type: str = field(init=False)
    param_in: str = field(init=False)
    param_format: Optional[str] = field(init=False)
    param_enum: Optional[List[str]] = field(init=False)
    param_default: Optional[Any] = field(init=False)

    def __post_init__(self):
        self.name = self.params["name"].replace("-", "_")
        self.required = self.params["required"]
        self.param_type = self.params["type"]
        self.param_in = self.params["in"]
        self.param_format = self.params["format"] if "format" in self.params.keys(
        ) else None
        self.param_enum = self.params["enum"] if "enum" in self.params.keys(
        ) else None
        self.param_default = self.params["default"] if "default" in self.params.keys(
        ) else None

    def __handle_type(self):
        if self.param_type not in type_map:
            raise ValueError(
                f"Param type not in type map. Param type: {self.param_type}")

        type_hint = type_map[self.param_type]
        if type_hint == "Literal":
            enums = list(map(lambda x: f"\"{x}\"", self.param_enum))
            options = ', '.join(enums)
            type_hint = f"{type_hint}[{options}]"
            return type_hint
        else:
            return type_hint

        return type_hint

    def __handle_default(self):
        if self.param_default:
            return f" = {self.param_default}"
        elif not self.required:
            return " = None"
        else:
            return ""

    def build_param(self, SignatureParameter: str) -> Optional[str]:
        if self.param_in == "header":
            return f"header_{self.name}: {self.__handle_type()}{self.__handle_default()}"
        elif self.param_in == "query":
            return f"{self.name}: {self.__handle_type()}{self.__handle_default()}"
        elif self.param_in == "path":
            return f"path_{self.name}: {self.__handle_type()}{self.__handle_default()}"
        return


def download_swagger(path: Union[str, Path] = swagger_path) \
    -> None:
    logger.info(f"Downloading swagger file to path: {swagger_path}")
    swagger_uri = "http://bdl.stat.gov.pl/api/v1/swagger/doc/swagger.json"
    with swagger_path.open(mode="w") as out_file:
        out_file.write(requests.get(swagger_uri).text)


def __load_swagger_file(package: Package, resource: Resource = "swagger.json") \
    -> Dict[str, Any]:
    logger.info("Parsing the swagger json to a Python dict...")
    loaded = json.loads(read_binary(package=package, resource=resource)
        .decode("utf-8"))
    return loaded


def read_swagger(package: Package) -> List[str]:
    swagger_json = __load_swagger_file(package=package)
    # units_keys = load_swag["paths"]["/subjects"]["get"]
    signatures = []

    for key in swagger_json["paths"].keys():
        if "get" in swagger_json["paths"][key].keys():
            params = __extract_params(
                swagger_json["paths"][key]["get"])
            sig = __create_signature(params)
            signatures.append((key, sig))
        else:
            print(f"Could not find 'get' key in {key}")
    # TODO: replace the return type here with a NamedTuple with
    # a template_class_name, getter_func_name, path_name_etc
    return signatures


def __extract_params(
        get_dict: Dict[str, Any]
) -> List[str]:
    params = get_dict["parameters"]
    output = []
    for param_dict in params:
        signature_parameter = SignatureParameter(param_dict)
        output.append(signature_parameter.build_param(SignatureParameter=""))
    return output


def __create_signature(params: List[str]) -> str:
    param_string = ", ".join(params)
    return param_string


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
