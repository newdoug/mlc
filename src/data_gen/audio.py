"""Audio data type(s)"""

from enum import auto

try:
    from .data_type_base import DataTypeBase
except (ImportError, ModuleNotFoundError):
    from data_gen.data_type_base import DataTypeBase


class AudioDataType(DataTypeBase):
    """Audio data types/formats"""
    MP3 = auto()
    FLAC = auto()
    WAV = auto()
    # TODO: more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Audio data types not yet supported")
