"""General utilities, will probably organize/split up better later"""

import enum
import os
import struct
from typing import List


__all__ = [
    "BetterEnum",
    "rand_ascii_bytes",
    "rand_ascii_str",
    "rand_bytes",
    "rand_bytes_in_range",
    "rand_double",
    "rand_element_in_list",
    "rand_float",
    "rand_int_in_range",
    "rand_int8",
    "rand_int16",
    "rand_int32",
    "rand_int64",
    "rand_sparse_ascii_bytes",
    "rand_sparse_ascii_str",
    "rand_sparse_bytes",
    "rand_uint8",
    "rand_uint16",
    "rand_uint32",
    "rand_uint64",
]


# Range (low inclusive, high exclusive) of integers that are valid ASCII
# (standard ASCII)
ASCII_RANGE = (0x20, 0x7F)


class BetterEnum(enum.Enum):
    """Slightly improved enum class. Just adds a couple conveniences"""

    @classmethod
    def names(cls) -> List[str]:
        """Returns names of the members of the enum"""
        return list(el.name for el in cls)

    @classmethod
    def values(cls) -> List:
        """Returns values of the members of the enum"""
        return list(el.value for el in cls)

    @classmethod
    def to_dict(cls) -> dict:
        """Names to values dictionary"""
        return dict(zip(cls.names, cls.values))


def rand_int_in_range(low: int, high: int) -> int:
    """Generates a random integer that is in range [low, high) (`low` is
    inclusive, `high` is exclusive).
    """
    return (int.from_bytes(os.urandom(4),
                           byteorder="little") % (high - low)) +  low


def rand_uint64() -> int:
    """Random uint64"""
    return struct.unpack("<Q", os.urandom(8))[0]


def rand_int64() -> int:
    """Random int64"""
    return struct.unpack("<q", os.urandom(8))[0]


def rand_uint32() -> int:
    """Random uint32"""
    return struct.unpack("<I", os.urandom(4))[0]


def rand_int32() -> int:
    """Random int32"""
    return struct.unpack("<i", os.urandom(4))[0]


def rand_uint16() -> int:
    """Random uint16"""
    return struct.unpack("<H", os.urandom(2))[0]


def rand_int16() -> int:
    """Random int16"""
    return struct.unpack("<h", os.urandom(2))[0]


def rand_uint8() -> int:
    """Random uint8"""
    return struct.unpack("<B", os.urandom(1))[0]


def rand_int8() -> int:
    """Random int8"""
    return struct.unpack("<b", os.urandom(1))[0]


def rand_double() -> float:
    """Random 8-byte double"""
    return struct.unpack("<d", os.urandom(8))[0]


def rand_float() -> float:
    """Random 4-byte float"""
    return struct.unpack("<f", os.urandom(4))[0]


def rand_bytes_in_range(length: int, low: int, high: int) -> bytes:
    """Generate random bytes of length `length` where each value is in range
    [low, high).
    """
    data = bytearray(length)
    for i in range(length):
        data[i] = rand_int_in_range(low, high)
    return bytes(data)


def rand_bytes(length: int) -> bytes:
    """Random bytes of length `length`"""
    return os.urandom(length)


def rand_ascii_bytes(length: int) -> bytes:
    """Random ASCII bytes of length `length`"""
    return rand_bytes_in_range(ASCII_RANGE[0], ASCII_RANGE[1])


def rand_ascii_str(length: int) -> str:
    """Random ASCII bytes of length `length`"""
    return rand_ascii_bytes(length).decode("ASCII")


def rand_sparse_bytes(length: int, percent_sparse: float = 60.0,
                      sparse_byte: int = 0) -> bytes:
    """Generate random bytes of length `length` that is roughly
    `percent_sparse` percent sparse where "sparse" just means `sparse_byte`.
    """
    data = bytearray(rand_bytes(length))
    for i in range(length):
        # Roughly `percent_sparse` of bytes will be turned into 0
        if rand_int_in_range(0, 101) <= percent_sparse:
            data[i] = sparse_byte
    return bytes(data)


def rand_sparse_ascii_bytes(length: int, percent_sparse: float = 60.0,
                            sparse_byte: int = 0) -> bytes:
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


def rand_sparse_ascii_str(length: int, percent_sparse: float = 60.0,
                          sparse_byte: int = 0) -> str:
    """Generate random string of length `length` that is roughly
    `percent_sparse` percent sparse where "sparse" just means `sparse_byte`.
    The data is standard ASCII except for the `sparse_byte` values.
    """
    return rand_sparse_ascii_bytes(
        length, percent_sparse=percent_sparse,
        sparse_byte=sparse_byte).decode("ASCII")


def rand_element_in_list(lst: list) -> Any:
    """Returns a random element in list `lst`"""
    return lst[rand_int_in_range(0, len(lst))]
