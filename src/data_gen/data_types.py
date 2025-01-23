"""Types of data we can generate"""
from base64 import b64encode
from enum import auto
from typing import Optional, Union

try:
    from .utils import (
        BetterEnum,
        rand_bytes,
        rand_ascii_bytes,
        rand_ascii_str,
        rand_element_in_list,
        rand_sparse_bytes,
        rand_sparse_ascii_bytes,
    )
except (ImportError, ModuleNotFoundError):
    from utils import (
        BetterEnum,
        rand_bytes,
        rand_ascii_bytes,
        rand_ascii_str,
        rand_element_in_list,
        rand_sparse_bytes,
        rand_sparse_ascii_bytes,
    )


# TODO: put each into relevant other source file


class DataTypeBase(BetterEnum):
    """Base data type class"""
    def generate(self, settings: Optional[dict] = None) -> bytes:
        raise NotImplementedError("No specific data type to generate")


class DataTypeSettingKey(BetterEnum):
    """Common settings for data type generation.
    Values are keys in a dict.
    """
    LENGTH = "length"
    SPARSE_PERCENT = "sparse_percent"
    SPARSE_BYTE = "SPARSE_BYTE"


class RandomDataType(BetterEnum):
    """Types of random data to generate"""
    ASCII = auto()
    BINARY = auto()
    SPARSE_ASCII = auto()
    SPARSE_BIN = auto()

    def generate(self, settings: dict) -> bytes:
        length = settings.get(DataTypeSettingKey.LENGTH)
        sparse_percent = settings.get(DataTypeSettingKey.SPARSE_PERCENT, 60.0)
        sparse_byte = settings.get(DataTypeSettingKey.SPARSE_BYTE, 0)

        if self == RandomDataType.ASCII:
            return rand_ascii_bytes(length)
        if self == RandomDataType.BINARY:
            return rand_bytes(length)
        if self == RandomDataType.SPARSE_ASCII:
            return rand_sparse_ascii_bytes(
                length, sparse_percent=sparse_percent,
                sparse_byte=sparse_byte)
        if self == RandomDataType.SPARSE_BYTES:
            return rand_sparse_bytes(
                length, sparse_percent=sparse_percent,
                sparse_byte=sparse_byte)
        raise ValueError(f"Invalid data type '{self.value}'")


class AudioDataType(BetterEnum):
    """Audio data types/formats"""
    MP3 = auto()
    FLAC = auto()
    WAV = auto()
    # TODO: more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Audio data types not yet supported")


class VideoDataType(BetterEnum):
    """Video data types/formats"""
    MP4 = auto()
    MKV = auto()
    MPEG = auto()
    FLV = auto()
    # TODO: more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Video data types not yet supported")


class ImageDataType(BetterEnum):
    """Image data types/formats"""
    AVIF = auto()
    BMP = auto()
    CR2 = auto()
    DNG = auto()
    GIF = auto()
    HDR = auto()
    HEIF = auto()
    JPEG = auto()
    JPEG2000 = auto()
    JPEGXL = auto()
    PBM = auto()
    PGM = auto()
    PNG = auto()
    PNM = auto()
    PPM = auto()
    # Plaintext...
    SVG = auto()
    TIFF = auto()
    WEBP = auto()

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Image data types not yet supported")


class ExecutableDataType(BetterEnum):
    """Executable data types/formats"""
    NIX_ELF = auto()
    NIX_LIB_A = auto()
    NIX_LIB_SO = auto()
    NIX_OBJ = auto()
    WINDOWS_DLL = auto()
    # Doubt DLL vs EXE will be distinguishable
    WINDOWS_EXE = auto()
    WINDOWS_LIB = auto()
    WINDOWS_OBJ = auto()

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Executable data types not yet supported")


class SourceCodeDataType(BetterEnum):
    """Source code (plaintext) data type/format"""
    # TODO: how to handle encodings for interpreted plaintext data types?
    BATCH = auto()
    # Unsure if we'll be able to distringuish between header and source
    # (unlikely, but maybe if certain patterns that show up in headers rather
    # than source files (or vice versa) are enough to impact the ciphertext
    # or compressed text enough for the model to understand).
    C_HEADER = auto()
    C_SOURCE = auto()
    CPP_HEADER = auto()
    CPP_SOURCE = auto()
    GO = auto()
    JAVA = auto()
    JAVASCRIPT = auto()
    PERL = auto()
    PY = auto()
    RUBY = auto()
    RUST = auto()
    # Not distinguishing between various *nix shells (yet?)
    UNIX_SHELL = auto()
    # TODO: much much more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Source code data types not yet supported")


class DocumentDataType(BetterEnum):
    """Document (mostly plaintext) data type/format"""
    ASCIIDOC = auto()
    EPUB = auto()
    # HOCON is a superset of .properties and .json, so leaving that off
    MARKDOWN = auto()
    MS_DOC = auto()
    MS_DOCX = auto()
    # TODO: there are more book formats (at least one I can't remember right
    #       now)
    MOBI = auto()
    PDF = auto()
    PLIST = auto()
    PROPERTIES = auto()
    RTF = auto()
    # TODO: much more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Document data types not yet supported")


class MiscFileDataType(BetterEnum):
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
        length = settings.get(DataTypeSettingKey.LENGTH)
        if self == MiscFileDataType.BASE64:
            return b64encode(rand_bytes(length))
        raise NotImplementedError("Document data types not yet supported")


class JsonGenerator:
    LIST_DATA_TYPES = [
        int,
        float,
        str,
        dict,
        list,
    ]
    DICT_DATA_TYPES = [
        int,
        float,
        str,
        dict,
        list,
    ]
    OUTER_TYPES = [
        dict,
        list,
    ]

    def __init__(max_depth: int = 10, max_num_keys: int = 100,
                 max_list_length: int = 100) -> Union[dict, list]:
        self.max_depth = max_depth
        self.max_num_keys = max_num_keys
        self.max_list_length = max_list_length

    def _gen_dict(self, depth: int) -> dict:
        if depth > self.max_depth:
            return {}
        return {
            self._gen_key(): self._gen_element(depth + 1,
                rand_element_in_list(JsonGenerator.DICT_DATA_TYPES))
                        for _ in range(self.max_num_keys)
        }

    def _gen_list(self, depth: int) -> list:
        return [
            self._gen_element(depth + 1, rand_element_in_list(
                JsonGenerator.LIST_DATA_TYPES))
            for _ in range(self.max_list_length)
        ]

    def _gen_key(self) -> str:
        # range arbitrarily chosen
        return rand_ascii_str(rand_int_in_range(2, 13))

    def _gen_element(self, depth: int, type_):
        if type_ is int:
            return rand_int64()
        if type_ is float:
            return rand_float()
        if type_ is str:
            return rand_ascii_str(rand_int_in_range(2, 13))
        if type_ is dict:
            return self._gen_dict(depth)
        if type_ is list:
            return self._gen_list(depth)

    def gen_data(self) -> Union[dict, list]:
        """Returns randon JSON data"""
        outer_type = rand_element_in_list(JsonGenerator.OUTER_TYPES)
        return self._gen_element(0, outer_type)


def rand_json(max_depth: int) -> Union[dict, list]:
    """Generate random JSON data"""
    return JsonGenerator(max_depth).gen_data()


print("1")
print(json.dumps(rand_json(3), indent=2))
print("2")
print(json.dumps(rand_json(3), indent=2))
print("3")
print(json.dumps(rand_json(3), indent=2))
