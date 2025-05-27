"""Loading configs and other file formats"""

import json
from typing import Union

import yaml


def load_yaml_file(filename: str) -> Union[dict, list]:
    """Load and parse a YAML config file"""
    with open(filename, "r", encoding="UTF-8") as handle:
        return yaml.load(handle, Loader=yaml.SafeLoader)


def load_json_file(filename: str) -> Union[dict, list]:
    """Load and parse a JSON config file"""
    with open(filename, "r", encoding="UTF-8") as handle:
        return json.load(handle)
