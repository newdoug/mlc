"""Audio data type(s)"""

from enum import auto

from mlc.data_gen.data_type_base import DataTypeBase


class AudioDataType(DataTypeBase):
    """Audio data types/formats"""

    # Advanced Audio Coding
    AAC = auto()
    FLAC = auto()
    MP3 = auto()
    # RealAudio
    RA = auto()
    # Sound
    SND = auto()
    WAV = auto()
    # Windows Media Audio
    WMA = auto()
    # TODO: more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Audio data types not yet supported")
