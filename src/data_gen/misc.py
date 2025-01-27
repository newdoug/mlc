"""Miscellaneous data types"""

from base64 import b64encode
from enum import auto

try:
    from .data_type_base import DataTypeBase, DataTypeSettingKey
    from .random_data import rand_json_str
except (ImportError, ModuleNotFoundError):
    from data_gen.data_type_base import DataTypeBase, DataTypeSettingKey
    from data_gen.random_data import rand_json_str


class MiscFileDataType(DataTypeBase):
    """Miscellaneous/Config (sometimes) and other file formats (e.g., YAML,
    JSON, base64, etc.)
    """
    # Generic data storage formats
    BASE64 = auto()
    CSV = auto()
    INI = auto()
    JSON = auto()
    SAML = auto()
    TOML = auto()
    XML = auto()
    YAML = auto()
    YANG = auto()

    # Very specific
    NGINX_CONF = auto()

    def generate(self, settings: dict) -> bytes:
        length = settings.get(DataTypeSettingKey.LENGTH.name)
        if self == MiscFileDataType.BASE64:
            return b64encode(rand_bytes(length))
        if self == MiscFileDataType.JSON:
            max_depth = settings.get(DataTypeSettingKey.JSON_DEPTH.name, 5)
            return rand_json_str(max_depth).encode("UTF-8")
        raise NotImplementedError("That data type is not yet supported")
