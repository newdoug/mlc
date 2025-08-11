"""Random data"""

from enum import auto
import os
import struct
from typing import Any

from mlc.data_gen.data_type_base import DataTypeBase, DataTypeSettingKey
from mlc.utils.rand import rand_bytes


# Range (low inclusive, high exclusive) of integers that are valid ASCII
# (standard ASCII)
ASCII_RANGE = (0x20, 0x7F)


class RandomDataType(DataTypeBase):
    """Types of random data to generate"""

    ASCII = auto()
    BINARY = auto()
    SPARSE_ASCII = auto()
    SPARSE_BINARY = auto()

    def generate(self, settings: dict) -> bytes:
        length = settings[DataTypeSettingKey.LENGTH.name]

        if self == RandomDataType.ASCII:
            return rand_ascii_bytes(length)
        if self == RandomDataType.BINARY:
            return rand_bytes(length)

        sparse_percent = settings.get(DataTypeSettingKey.SPARSE_PERCENT.name, 60.0)
        sparse_byte = settings.get(DataTypeSettingKey.SPARSE_BYTE.name, 0)

        if self == RandomDataType.SPARSE_ASCII:
            return rand_sparse_ascii_bytes(
                length, sparse_percent=sparse_percent, sparse_byte=sparse_byte
            )
        if self == RandomDataType.SPARSE_BINARY:
            return rand_sparse_bytes(length, sparse_percent=sparse_percent, sparse_byte=sparse_byte)
        raise ValueError(f"Invalid data type '{self.value}'")


def rand_int_in_range(low: int, high: int) -> int:
    """Generates a random integer that is in range [low, high) (`low` is
    inclusive, `high` is exclusive).
    """
    return (int.from_bytes(os.urandom(4), byteorder="little") % (high - low)) + low


def _rand_val_from_struct_fmt(struct_fmt: str):
    return struct.unpack(struct_fmt, os.urandom(struct.calcsize(struct_fmt)))[0]


def rand_uint64() -> int:
    """Random uint64"""
    return _rand_val_from_struct_fmt("<Q")


def rand_int64() -> int:
    """Random int64"""
    return _rand_val_from_struct_fmt("<q")


def rand_uint32() -> int:
    """Random uint32"""
    return _rand_val_from_struct_fmt("<I")


def rand_int32() -> int:
    """Random int32"""
    return _rand_val_from_struct_fmt("<i")


def rand_uint16() -> int:
    """Random uint16"""
    return _rand_val_from_struct_fmt("<H")


def rand_int16() -> int:
    """Random int16"""
    return _rand_val_from_struct_fmt("<h")


def rand_uint8() -> int:
    """Random uint8"""
    return _rand_val_from_struct_fmt("<B")


def rand_int8() -> int:
    """Random int8"""
    return _rand_val_from_struct_fmt("<b")


def rand_double() -> float:
    """Random 8-byte double"""
    return _rand_val_from_struct_fmt("<d")


def rand_float() -> float:
    """Random 4-byte float"""
    return _rand_val_from_struct_fmt("<f")


def rand_bytes_in_range(length: int, low: int, high: int) -> bytes:
    """Generate random bytes of length `length` where each value is in range
    [low, high).
    """
    data = bytearray(length)
    for i in range(length):
        data[i] = rand_int_in_range(low, high)
    return bytes(data)


def rand_ascii_bytes(length: int) -> bytes:
    """Random ASCII bytes of length `length`"""
    return rand_bytes_in_range(length, ASCII_RANGE[0], ASCII_RANGE[1])


def rand_ascii_str(length: int) -> str:
    """Random ASCII bytes of length `length`"""
    return rand_ascii_bytes(length).decode("ASCII")


def rand_sparse_bytes(length: int, percent_sparse: float = 60.0, sparse_byte: int = 0) -> bytes:
    """Generate random bytes of length `length` that is roughly
    `percent_sparse` percent sparse where "sparse" just means `sparse_byte`.
    """
    data = bytearray(rand_bytes(length))
    for i in range(length):
        # Roughly `percent_sparse` of bytes will be turned into `sparse_byte`
        if rand_int_in_range(0, 101) <= percent_sparse:
            data[i] = sparse_byte
    return bytes(data)


def rand_sparse_ascii_bytes(
    length: int, percent_sparse: float = 60.0, sparse_byte: int = 0
) -> bytes:
    """Generate random bytes of length `length` that is roughly
    `percent_sparse` percent sparse where "sparse" just means `sparse_byte`.
    The data is standard ASCII except for the `sparse_byte` values.
    """
    data = bytearray(rand_ascii_bytes(length))
    for i in range(length):
        # Roughly `percent_sparse` of bytes will be turned into 0
        if rand_int_in_range(0, 101) <= percent_sparse:
            data[i] = sparse_byte
    return bytes(data)


def rand_sparse_ascii_str(length: int, percent_sparse: float = 60.0, sparse_byte: int = 0) -> str:
    """Generate random string of length `length` that is roughly
    `percent_sparse` percent sparse where "sparse" just means `sparse_byte`.
    The data is standard ASCII except for the `sparse_byte` values.
    """
    return rand_sparse_ascii_bytes(
        length, percent_sparse=percent_sparse, sparse_byte=sparse_byte
    ).decode("ASCII")


def rand_element_in_list(lst: list) -> Any:
    """Returns a random element in list `lst`"""
    return lst[rand_int_in_range(0, len(lst))]
