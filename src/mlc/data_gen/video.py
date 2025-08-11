"""Video data type(s)"""

from enum import auto

from mlc.data_gen.data_type_base import DataTypeBase


class VideoDataType(DataTypeBase):
    """Video data types/formats"""

    AVI = auto()
    FLV = auto()
    MKV = auto()
    MOV = auto()
    MP4 = auto()
    # .mpg or .mpeg
    MPEG = auto()
    # 3gp
    THREEGP = auto()
    WMV = auto()
    # TODO: more

    def generate(self, settings: dict) -> bytes:
        raise NotImplementedError("Video data types not yet supported")
