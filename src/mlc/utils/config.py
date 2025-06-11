from pathlib import Path
from typing import Union

import yaml


SCRIPT_DIR = Path(__file__).parent.absolute()
CONFIG_FILE = SCRIPT_DIR.parent / "config.yaml"

# TODO: more config work? Make a jsonschema, validate, turn into an object with fields instead of just a dict, etc.
# There is probably a library for that.


def load_config(config_file: Union[str, Path] = CONFIG_FILE) -> dict:
    with open(config_file, "r", encoding="UTF-8") as handle:
        return yaml.load(handle, Loader=yaml.SafeLoader)
