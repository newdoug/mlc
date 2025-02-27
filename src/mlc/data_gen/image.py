"""Image/picture data type(s)"""

from enum import auto

try:
    from .data_type_base import DataTypeBase
except (ImportError, ModuleNotFoundError):
    from data_gen.data_type_base import DataTypeBase


class ImageDataType(DataTypeBase):
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
