"""Miscellaneous data types"""

from base64 import b64encode
from enum import auto

from mlc.data_gen.data_type_base import DataTypeBase, DataTypeSettingKey
from mlc.data_gen.misc.json_generator import rand_json_str


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
        length = settings[DataTypeSettingKey.LENGTH.name]
        # TODO: validate length? Maybe settings will be assumed validated
        #       before here via a jsonschema or something. At some point at
        #       least. Length seems like it could/should have different meanings
        #       depending on data type though, which implies specific validation
        if self == MiscFileDataType.BASE64:
            return b64encode(rand_bytes(length))
        if self == MiscFileDataType.JSON:
            max_depth = settings.get(DataTypeSettingKey.JSON_DEPTH.name, 5)
            return rand_json_str(max_depth).encode("UTF-8")
        if self == MiscFileDataType.CSV:
            num_cols = settings.get(DataTypeSettingKey.CSV_NUM_COLS, DEFAULT_CSV_NUM_COLS)
            csv_header = settings.get(
                DataTypeSettingKey.CSV_HEADER, generate_random_csv_header(num_cols)
            )
        raise NotImplementedError("That data type is not yet supported")
