"""Audio data type(s)"""

from enum import auto

from mlc.data_gen.data_type_base import DataTypeBase


class AudioDataType(DataTypeBase):
    """Audio data types/formats"""

    MP3 = auto()
    FLAC = auto()
    WAV = auto()
    # TODO: more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Audio data types not yet supported")
