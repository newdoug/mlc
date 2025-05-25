"""Video data type(s)"""

from enum import auto

from mlc.data_gen.data_type_base import DataTypeBase


class VideoDataType(DataTypeBase):
    """Video data types/formats"""
    MP4 = auto()
    MKV = auto()
    MPEG = auto()
    FLV = auto()
    # TODO: more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Video data types not yet supported")

