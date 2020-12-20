from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Union
import logging


logger = logging.getLogger(__name__)


type_map = {
    "string": "str",
    "integer": "int",
    "enum": "Literal",
    "array": "List"
}


@dataclass
class SignatureParameterBuilder:
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
        self.param_format = self.params["format"] \
            if "format" in self.params.keys(
        ) else None
        self.param_enum = self.params["enum"] \
            if "enum" in self.params.keys(
        ) else None
        self.param_default = self.params["default"] \
            if "default" in self.params.keys(
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

    def __build_header_param(self) -> str:
        return f"header_{self.name}: {self.__handle_type()}"
        f"{self.__handle_default()}"

    def __build_query_param(self) -> str:
        return f"{self.name}: {self.__handle_type()}"
        f"{self.__handle_default()}"

    def __build_path_param(self) -> str:
        return f"path_{self.name}: {self.__handle_type()}"
        f"{self.__handle_default()}"

    def build_param(self) -> Optional[str]:
        if self.param_in == "header":
            return self.__build_header_param()
        elif self.param_in == "query":
            return self.__build_query_param()
        elif self.param_in == "path":
            return self.__build_path_param()
        return
