"""Types of data we can generate"""
from enum import auto

try:
    from .utils import BetterEnum
except (ImportError, ModuleNotFoundError):
    from utils import BetterEnum


# TODO: `DataType` base class if useful? E.g. provide a `generate()` method

class RandomDataType(BetterEnum):
    """Types of random data to generate"""
    ASCII = auto()
    BINARY = auto()
    SPARSE_ASCII = auto()
    SPARSE_BIN = auto()


class MiscFileDataTypes(BetterEnum):
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


class AudioDataType(BetterEnum):
    """Audio data types/formats"""
    MP3 = auto()
    FLAC = auto()
    WAV = auto()
    # TODO: more


class VideoDataType(BetterEnum):
    """Video data types/formats"""
    MP4 = auto()
    MKV = auto()
    MPEG = auto()
    FLV = auto()
    # TODO: more


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


class DocumentDataType(BetterEnum):
    """Document (mostly plaintext) data type/format"""
    ASCIIDOC = auto()
    EPUB = auto()
    # HOCON is a superset of .properties and .json, so leaving that off
    MARKDOWN = auto()
    MOBI = auto()
    MS_DOC = auto()
    MS_DOCX = auto()
    MOBI = auto()
    PDF = auto()
    PLIST = auto()
    PROPERTIES = auto()
    RTF = auto()
    # TODO: much more
