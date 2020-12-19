from string import Template

module_header_template = Template(
    "from dataclasses import dataclass\n"
)

field_template = Template(
    "    $field_name: str = $field_value"
)

class_signature_template = Template(
    "@dataclass\nclass $class_name:"
)
