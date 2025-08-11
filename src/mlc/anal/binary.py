"""Analysis functions that may be useful on random binary data.
Only data >= 8 bytes is supported at this time as it's not worth the overhead to check every input
for correct sizes just to support unusual inputs. Most of these functions should support all
bytes-type inputs. If you feel like catching the appropriate exceptions yourself and setting
feature values to None or something, that's fine. Most exceptions are probably `ZeroDivisionError`.
"""

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import math
import subprocess
import tempfile
from typing import Callable, Iterable, Tuple, Union
import zlib

from mlc.compression import compress, CompressionType


# Indicates that the function accepts 1 bytes object and returns a float or int
_MARK_BYTE_ARRAY_ATTR = "is_anal"
# Indicates that the function accepts 2 bytes objects and returns a float or int
_MARK_BYTE_ARRAYS_ATTR = "is_anals"
DEFAULT_BLOCK_SIZE_BYTES: int = 8
# Some typedefs
FeatureType = Union[float, int]
ByteArrayCallableT = Callable[[bytes], FeatureType]
ByteArraysCallableT = Callable[[bytes, bytes], FeatureType]


def mark_byte_array_func(func: ByteArrayCallableT) -> ByteArrayCallableT:
    setattr(func, _MARK_BYTE_ARRAY_ATTR, True)
    return func


def mark_byte_arrays_func(func: ByteArraysCallableT) -> ByteArraysCallableT:
    setattr(func, _MARK_BYTE_ARRAYS_ATTR, True)
    return func


def set_default_block_size(block_size_bytes: int) -> int:
    global DEFAULT_BLOCK_SIZE_BYTES
    DEFAULT_BLOCK_SIZE_BYTES = block_size_bytes


def blocks(data: bytes, block_size_bytes: int) -> list[bytes]:
    for idx in range(0, len(data) - block_size_bytes, block_size_bytes):
        yield data[idx : idx + block_size_bytes]


def _bin(byte: int) -> str:
    return "{:08b}".format(byte)


def bytes_to_bin_str(data: bytes) -> str:
    return "".join([_bin(byte) for byte in data])


def lower_nibble(byte: int) -> int:
    return byte & 0x0F


def upper_nibble(byte: int) -> int:
    return (byte & 0xF0) >> 4


def num_bits_on(byte: int) -> int:
    return _bin(byte).count("1")


def num_bits_off(byte: int) -> int:
    return _bin(byte).count("0")


@mark_byte_array_func
def average_byte(data: bytes) -> float:
    return sum(data) / len(data)


@mark_byte_array_func
def average_byte_int(data: bytes) -> int:
    return sum(data) // len(data)


def break_bytes_iter(
    data: bytes, int_size_bytes: int, byteorder: str, signed: bool
) -> Iterable[int]:
    for i in range(0, len(data) - int_size_bytes + 1, int_size_bytes):
        yield int.from_bytes(data[i : i + int_size_bytes], byteorder=byteorder, signed=signed)


def break_bytes(data: bytes, int_size_bytes: int, byteorder: str, signed: bool) -> list[int]:
    return list(break_bytes_iter(data, int_size_bytes, byteorder, signed))


@mark_byte_array_func
def average_uint16_le(data: bytes) -> float:
    return sum(break_bytes(data, 2, "little", False)) / (len(data) // 2)


@mark_byte_array_func
def average_uint16_be(data: bytes) -> float:
    return sum(break_bytes(data, 2, "big", False)) / (len(data) // 2)


@mark_byte_array_func
def average_int16_le(data: bytes) -> float:
    return sum(break_bytes(data, 2, "little", True)) / (len(data) // 2)


@mark_byte_array_func
def average_int16_be(data: bytes) -> float:
    return sum(break_bytes(data, 2, "big", True)) / (len(data) // 2)


@mark_byte_array_func
def average_uint24_le(data: bytes) -> float:
    return sum(break_bytes(data, 3, "little", False)) / (len(data) // 3)


@mark_byte_array_func
def average_uint24_be(data: bytes) -> float:
    return sum(break_bytes(data, 3, "big", False)) / (len(data) // 3)


@mark_byte_array_func
def average_int24_le(data: bytes) -> float:
    return sum(break_bytes(data, 3, "little", True)) / (len(data) // 3)


@mark_byte_array_func
def average_int24_be(data: bytes) -> float:
    return sum(break_bytes(data, 3, "big", True)) / (len(data) // 3)


@mark_byte_array_func
def average_uint32_le(data: bytes) -> float:
    return sum(break_bytes(data, 4, "little", False)) / (len(data) // 4)


@mark_byte_array_func
def average_uint32_be(data: bytes) -> float:
    return sum(break_bytes(data, 4, "big", False)) / (len(data) // 4)


@mark_byte_array_func
def average_int32_le(data: bytes) -> float:
    return sum(break_bytes(data, 4, "little", True)) / (len(data) // 4)


@mark_byte_array_func
def average_int32_be(data: bytes) -> float:
    return sum(break_bytes(data, 4, "big", True)) / (len(data) // 4)


@mark_byte_array_func
def average_uint40_le(data: bytes) -> float:
    return sum(break_bytes(data, 5, "little", False)) / (len(data) // 5)


@mark_byte_array_func
def average_uint40_be(data: bytes) -> float:
    return sum(break_bytes(data, 5, "big", False)) / (len(data) // 5)


@mark_byte_array_func
def average_int40_le(data: bytes) -> float:
    return sum(break_bytes(data, 5, "little", True)) / (len(data) // 5)


@mark_byte_array_func
def average_int40_be(data: bytes) -> float:
    return sum(break_bytes(data, 5, "big", True)) / (len(data) // 5)


@mark_byte_array_func
def average_uint48_le(data: bytes) -> float:
    return sum(break_bytes(data, 6, "little", False)) / (len(data) // 6)


@mark_byte_array_func
def average_uint48_be(data: bytes) -> float:
    return sum(break_bytes(data, 6, "big", False)) / (len(data) // 6)


@mark_byte_array_func
def average_int48_le(data: bytes) -> float:
    return sum(break_bytes(data, 6, "little", True)) / (len(data) // 6)


@mark_byte_array_func
def average_int48_be(data: bytes) -> float:
    return sum(break_bytes(data, 6, "big", True)) / (len(data) // 6)


@mark_byte_array_func
def average_uint56_le(data: bytes) -> float:
    return sum(break_bytes(data, 7, "little", False)) / (len(data) // 7)


@mark_byte_array_func
def average_uint56_be(data: bytes) -> float:
    return sum(break_bytes(data, 7, "big", False)) / (len(data) // 7)


@mark_byte_array_func
def average_int56_le(data: bytes) -> float:
    return sum(break_bytes(data, 7, "little", True)) / (len(data) // 7)


@mark_byte_array_func
def average_int56_be(data: bytes) -> float:
    return sum(break_bytes(data, 7, "big", True)) / (len(data) // 7)


@mark_byte_array_func
def average_uint64_le(data: bytes) -> float:
    return sum(break_bytes(data, 8, "little", False)) / (len(data) // 8)


@mark_byte_array_func
def average_uint64_be(data: bytes) -> float:
    return sum(break_bytes(data, 8, "big", False)) / (len(data) // 8)


@mark_byte_array_func
def average_int64_le(data: bytes) -> float:
    return sum(break_bytes(data, 8, "little", True)) / (len(data) // 8)


@mark_byte_array_func
def average_int64_be(data: bytes) -> float:
    return sum(break_bytes(data, 8, "big", True)) / (len(data) // 8)


@mark_byte_array_func
def average_bit(data: bytes) -> float:
    return sum(num_bits_on(byte) for byte in data) / (len(data) * 8)


@mark_byte_array_func
def average_nibble(data: bytes) -> float:
    return sum(lower_nibble(byte) + upper_nibble(byte) for byte in data) / (len(data) * 2)


@mark_byte_array_func
def average_upper_nibble(data: bytes) -> float:
    return sum(upper_nibble(byte) for byte in data) / len(data)


@mark_byte_array_func
def average_lower_nibble(data: bytes) -> float:
    return sum(lower_nibble(byte) for byte in data) / len(data)


@mark_byte_array_func
def most_common_byte(data: bytes) -> int:
    """In case of collisions, highest byte is returned"""
    counts = {(data.count(b), b) for b in range(256)}
    # Sort by count (and then byte value in case of collisions)
    # Grab last element (highest count)
    # Return byte value
    return sorted(counts)[-1][1]


@mark_byte_array_func
def average_num_bits_on(data: bytes) -> float:
    return sum(num_bits_on(byte) for byte in data) / len(data)


@mark_byte_array_func
def average_num_bits_off(data: bytes) -> float:
    return sum(num_bits_off(byte) for byte in data) / len(data)


def percent_bytes_with_bit_x_on(data: bytes, bit: int) -> float:
    assert 0 <= bit <= 7
    bit = 1 << bit
    return 100.0 * len([byte for byte in data if byte & bit]) / len(data)


def percent_bytes_with_bit_x_off(data: bytes, bit: int) -> float:
    assert 0 <= bit <= 7
    bit = 1 << bit
    return 100.0 * len([byte for byte in data if byte & bit == 0]) / len(data)


@mark_byte_array_func
def percent_bytes_first_nibble_gt_second_nibble(data: bytes) -> float:
    return 100.0 * sum(1 for byte in data if lower_nibble(byte) > upper_nibble(byte)) / len(data)


@mark_byte_array_func
def percent_bytes_first_nibble_ge_second_nibble(data: bytes) -> float:
    return 100.0 * sum(1 for byte in data if lower_nibble(byte) >= upper_nibble(byte)) / len(data)


@mark_byte_array_func
def percent_bytes_first_nibble_lt_second_nibble(data: bytes) -> float:
    return 100.0 * sum(1 for byte in data if lower_nibble(byte) < upper_nibble(byte)) / len(data)


@mark_byte_array_func
def percent_bytes_first_nibble_le_second_nibble(data: bytes) -> float:
    return 100.0 * sum(1 for byte in data if lower_nibble(byte) <= upper_nibble(byte)) / len(data)


@mark_byte_array_func
def percent_bytes_first_nibble_eq_second_nibble(data: bytes) -> float:
    return 100.0 * sum(1 for byte in data if lower_nibble(byte) == upper_nibble(byte)) / len(data)


@mark_byte_array_func
def percent_bytes_first_nibble_eq_complement_of_second_nibble(data: bytes) -> float:
    return 100.0 * sum(1 for byte in data if lower_nibble(byte) == ~upper_nibble(byte)) / len(data)


def _mirror(byte: int) -> int:
    # bit-reverse input int (range [0, 255])
    return int("{:08b}".format(byte)[::-1], 2)


@mark_byte_array_func
def percent_bytes_first_nibble_eq_mirror_of_second_nibble(data: bytes) -> float:
    # TODO: is sum(1 for byte ...]) or len([byte for byte ...) faster? Memory efficiency?
    return (
        100.0
        * sum(1 for byte in data if lower_nibble(byte) == _mirror(upper_nibble(byte)))
        / len(data)
    )


percent_bytes_with_bit_0_on = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_on(data, 0)
)
percent_bytes_with_bit_1_on = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_on(data, 1)
)
percent_bytes_with_bit_2_on = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_on(data, 2)
)
percent_bytes_with_bit_3_on = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_on(data, 3)
)
percent_bytes_with_bit_4_on = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_on(data, 4)
)
percent_bytes_with_bit_5_on = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_on(data, 5)
)
percent_bytes_with_bit_6_on = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_on(data, 6)
)
percent_bytes_with_bit_7_on = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_on(data, 7)
)
percent_bytes_with_bit_0_off = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_off(data, 0)
)
percent_bytes_with_bit_1_off = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_off(data, 1)
)
percent_bytes_with_bit_2_off = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_off(data, 2)
)
percent_bytes_with_bit_3_off = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_off(data, 3)
)
percent_bytes_with_bit_4_off = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_off(data, 4)
)
percent_bytes_with_bit_5_off = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_off(data, 5)
)
percent_bytes_with_bit_6_off = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_off(data, 6)
)
percent_bytes_with_bit_7_off = mark_byte_array_func(
    lambda data: percent_bytes_with_bit_x_off(data, 7)
)


def _percent_op_next_byte(data: bytes, op: Callable) -> float:
    if len(data) < 2:
        return 0.0
    occ = 0
    for idx in range(0, len(data) - 1):
        if op(data[idx], data[idx + 1]):
            occ += 1
    return 100.0 * occ / (len(data) - 1)


def _lt_op(byte1: int, byte2: int) -> bool:
    return byte1 < byte2


def _le_op(byte1: int, byte2: int) -> bool:
    return byte1 <= byte2


def _gt_op(byte1: int, byte2: int) -> bool:
    return byte1 > byte2


def _ge_op(byte1: int, byte2: int) -> bool:
    return byte1 >= byte2


def _eq_op(byte1: int, byte2: int) -> bool:
    return byte1 == byte2


@mark_byte_array_func
def percent_bytes_lt_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _lt_op)


@mark_byte_array_func
def percent_bytes_le_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _le_op)


@mark_byte_array_func
def percent_bytes_gt_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _gt_op)


@mark_byte_array_func
def percent_bytes_ge_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _ge_op)


@mark_byte_array_func
def percent_bytes_eq_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _eq_op)


def _set_up_percent_bytes_containing_bits_funcs() -> None:
    def _get_func(patt):
        return lambda data: 100.0 * sum(1 for byte in data if patt in _bin(byte)) / len(data)

    for bit_len in range(1, 9):
        for patt in range(0, 2**bit_len):
            patt = ("{:0" + str(bit_len) + "b}").format(patt)
            func_name = f"percent_of_bytes_containing_bits_{patt}"
            globals()[func_name] = mark_byte_array_func(_get_func(patt))


_set_up_percent_bytes_containing_bits_funcs()


def _set_up_percent_bytes_gt_funcs() -> None:
    def _get_func(num):
        return lambda data: 100.0 * sum(1 for byte in data if byte > num) / len(data)

    for num in range(1, 255):
        func_name = f"percent_of_bytes_gt_{num}"
        globals()[func_name] = mark_byte_array_func(_get_func(num))


_set_up_percent_bytes_gt_funcs()


def _set_up_percent_freq_each_byte_funcs() -> None:
    def _get_func(num):
        return lambda data: 100.0 * data.count(num) / len(data)

    for num in range(0, 256):
        func_name = f"percent_of_bytes_eq_{num}"
        globals()[func_name] = mark_byte_array_func(_get_func(num))


_set_up_percent_freq_each_byte_funcs()


# TODO: not sure these are correct. Values look off. Write tests to verify.
#       Update: I think it might actually be fine. Test anyways.
def _set_up_percent_of_blocks_with_byte_in_pos_funcs(
    pos: int, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> None:
    def _get_func(pos_, num):
        return lambda data: (
            100.0
            * len([block for block in blocks(data, block_size_bytes) if block[pos_] == num])
            / (len(data) / block_size_bytes)
        )

    for num in range(0, 256):
        func_name = f"percent_of_blocks_idx_{pos}_eq_{num}"
        globals()[func_name] = mark_byte_array_func(_get_func(pos, num))


for POS in range(DEFAULT_BLOCK_SIZE_BYTES):
    _set_up_percent_of_blocks_with_byte_in_pos_funcs(POS, block_size_bytes=DEFAULT_BLOCK_SIZE_BYTES)


def _average_block_op(
    data: bytes, op: Callable, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    sums = sum(op(block) for block in blocks(data, block_size_bytes))
    return sums / (len(data) // block_size_bytes)


@mark_byte_array_func
def average_block_max(data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES) -> float:
    return _average_block_op(data, max, block_size_bytes=block_size_bytes)


@mark_byte_array_func
def average_block_min(data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES) -> float:
    return _average_block_op(data, min, block_size_bytes=block_size_bytes)


@mark_byte_array_func
def average_block_max_minus_min(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    return _average_block_op(
        data, lambda block: max(block) - min(block), block_size_bytes=block_size_bytes
    )


@mark_byte_array_func
def calc_entropy(data: bytes) -> float:
    freq = Counter(data)
    return -sum((c / len(data)) * math.log2(c / len(data)) for c in freq.values())


@mark_byte_array_func
def calc_chi_square(data: bytes) -> float:
    expected = len(data) / 256  # Expected frequency for uniform distribution
    freq = Counter(data)

    chi2 = 0.0
    for byte_val in range(256):
        observed = freq.get(byte_val, 0)
        chi2 += ((observed - expected) ** 2) / expected

    return chi2


@mark_byte_array_func
def calc_chi_square_normalized(data: bytes) -> float:
    return calc_chi_square(data) / len(data)


@dataclass
class EntResults:
    """Useful outputs of `ent -t <filename>`"""

    entropy: float
    chi_square: float
    mean: float
    monte_carlo_pi: float
    serial_correlation: float


# If data is only run serially through functions in this file, then 1 would be sufficient, but in
# cases of multi-threading or multi-processing, more cache entries would be needed to be useful
@lru_cache(maxsize=64)
def run_ent(data: bytes) -> EntResults:
    with tempfile.NamedTemporaryFile() as temp_file:
        filename = temp_file.name
        with open(filename, "wb") as handle:
            handle.write(data)
        result = subprocess.run(["ent", "-t", filename], stdout=subprocess.PIPE, check=True)
        lines = [line.strip() for line in result.stdout.decode().split("\n")]
        values = [value.strip() for value in lines[1].split(",")]
        return EntResults(
            entropy=float(values[2]),
            chi_square=float(values[3]),
            mean=float(values[4]),
            monte_carlo_pi=float(values[5]),
            serial_correlation=float(values[6]),
        )


@mark_byte_array_func
def ent_entropy(data: bytes) -> float:
    return run_ent(data).entropy


@mark_byte_array_func
def ent_chi_square(data: bytes) -> float:
    return run_ent(data).chi_square


@mark_byte_array_func
def ent_chi_square_normalized(data: bytes) -> float:
    return run_ent(data).chi_square / len(data)


@mark_byte_array_func
def ent_monte_carlo_pi(data: bytes) -> float:
    return run_ent(data).monte_carlo_pi


@mark_byte_array_func
def ent_serial_correlation(data: bytes) -> float:
    return run_ent(data).serial_correlation


@mark_byte_array_func
def ent_entropy_block_average(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    block_vals = [run_ent(block).entropy for block in blocks(data, block_size_bytes)]
    return sum(block_vals) / len(block_vals)


@mark_byte_array_func
def ent_chi_square_block_average(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    block_vals = [run_ent(block).chi_square for block in blocks(data, block_size_bytes)]
    return sum(block_vals) / len(block_vals)


@mark_byte_array_func
def ent_monte_carlo_pi_block_average(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    block_vals = [run_ent(block).monte_carlo_pi for block in blocks(data, block_size_bytes)]
    return sum(block_vals) / len(block_vals)


@mark_byte_array_func
def ent_serial_correlation_bkock_average(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    block_vals = [run_ent(block).serial_correlation for block in blocks(data, block_size_bytes)]
    return sum(block_vals) / len(block_vals)


def bits_on_indices(byte: int) -> list[int]:
    """Returns list of indices of which bits were on in given `byte` (range [0, 255])"""
    byte = _bin(byte)[::-1]
    return [i for i in range(len(byte)) if byte[i] == "1"]


@mark_byte_array_func
def average_on_bit_position_8bits(data: bytes) -> float:
    # TODO: unit test
    # TODO: 4 bits, 16 bits
    total_sum = 0
    for byte in data:
        on = bits_on_indices(byte)
        total_sum += sum(on)
    return total_sum / (len(data) * 8)


@mark_byte_array_func
def kolmogorov_complexity_estimate(data: bytes) -> float:
    return len(zlib.compress(data)) / len(data)


@mark_byte_array_func
def kolmogorov_complexity_estimate_binary(data: bytes) -> float:
    return kolmogorov_complexity_estimate(bytes_to_bin_str(data).encode())


@mark_byte_array_func
def compression_ratio_zlib(data: bytes) -> float:
    return len(compress(data, CompressionType.ZLIB)) / len(data)


@mark_byte_array_func
def compression_ratio_gzip(data: bytes) -> float:
    return len(compress(data, CompressionType.GZIP)) / len(data)


@mark_byte_array_func
def compression_ratio_lzma(data: bytes) -> float:
    return len(compress(data, CompressionType.LZMA)) / len(data)


@mark_byte_array_func
def compression_ratio_bz2(data: bytes) -> float:
    return len(compress(data, CompressionType.BZ2)) / len(data)


@mark_byte_array_func
def compression_ratio_tar(data: bytes) -> float:
    return len(compress(data, CompressionType.TAR)) / len(data)


@mark_byte_array_func
def compression_ratio_tar_gz(data: bytes) -> float:
    return len(compress(data, CompressionType.TAR_GZ)) / len(data)


@mark_byte_array_func
def compression_ratio_tar_bz2(data: bytes) -> float:
    return len(compress(data, CompressionType.TAR_BZ2)) / len(data)


@mark_byte_array_func
def compression_ratio_tar_xz(data: bytes) -> float:
    return len(compress(data, CompressionType.TAR_XZ)) / len(data)


@mark_byte_array_func
def compression_ratio_zstd(data: bytes) -> float:
    return len(compress(data, CompressionType.ZSTD)) / len(data)


@mark_byte_array_func
def percent_bytes_bit0_bit7_symmetry(data: bytes) -> float:
    return sum(1 for byte in data if (byte & 1) and (byte & 0b10000000)) / len(data)


def _set_up_percent_bit_symmetries_funcs() -> None:
    # TODO: unit test these
    def _get_func(start_1, end_1, start_2, end_2):
        return lambda data: 100.0 * _num_match(data, start_1, end_1, start_2, end_2) / len(data)

    for start_bit_idx_1 in range(0, 7):
        for start_bit_idx_2 in range(start_bit_idx_1 + 1, 8):
            for bit_len in range(1, 8 - start_bit_idx_2):
                end_bit_idx_1 = start_bit_idx_1 + bit_len
                end_bit_idx_2 = start_bit_idx_2 + bit_len

                func_name = f"percent_of_bytes_bits_{start_bit_idx_1}_to_{end_bit_idx_1}_eq_{start_bit_idx_2}_to_{end_bit_idx_2}"

                def _num_match(data, start_1, end_1, start_2, end_2):
                    s = 0
                    for byte in data:
                        bin_byte = _bin(byte)
                        if bin_byte[start_1 : end_1 + 1] == bin_byte[start_2 : end_2 + 1]:
                            s += 1
                    return s

                globals()[func_name] = mark_byte_array_func(
                    # This binds the proper idx values to the function returned
                    # TODO: make sure other functions that do this globals()[...] thing properly
                    # bind values too (should be verifiable with unit tests)
                    _get_func(start_bit_idx_1, end_bit_idx_1, start_bit_idx_2, end_bit_idx_2)
                )


_set_up_percent_bit_symmetries_funcs()


def _set_up_percent_bit_mask_match_funcs() -> None:
    def _get_func(mask):
        return lambda data: 100.0 * sum(1 for byte in data if byte & mask == mask) / len(data)

    for mask in range(1, 256):
        func_name = f"percent_of_bytes_matching_mask_{mask}"
        globals()[func_name] = mark_byte_array_func(
            # This binds the proper mask value to the function returned
            _get_func(mask)
        )


_set_up_percent_bit_mask_match_funcs()


@mark_byte_array_func
def xor_all_bytes_8bit(data: bytes) -> int:
    val = 0
    for byte in data:
        val ^= byte
    return val


def xor_all_bytes_16bit(data: bytes, byteorder: str) -> int:
    val = 0
    for idx in range(0, len(data), 2):
        val ^= int.from_bytes(data[idx : idx + 2], byteorder=byteorder)
    return val


@mark_byte_array_func
def xor_all_bytes_16bit_le(data: bytes) -> int:
    return xor_all_bytes_16bit(data, "little")


@mark_byte_array_func
def xor_all_bytes_16bit_be(data: bytes) -> int:
    return xor_all_bytes_16bit(data, "big")


@mark_byte_array_func
def average_xor_per_block_8bit(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    sums = 0
    num_blocks = 0
    for block in blocks(data, block_size_bytes):
        sums += xor_all_bytes_8bit(block)
        num_blocks += 1
    return sums / num_blocks


@mark_byte_array_func
def average_block_average(data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES) -> float:
    sums = 0
    num_blocks = 0
    for block in blocks(data, block_size_bytes):
        sums += sum(block) / block_size_bytes
        num_blocks += 1
    return sums / num_blocks


@mark_byte_array_func
def variance(data: bytes) -> float:
    data_len = len(data)
    average = sum(data) / data_len
    return sum((byte - average) ** 2 for byte in data) / data_len


@mark_byte_array_func
def standard_deviation(data: bytes) -> float:
    return variance(data) ** 0.5


@mark_byte_array_func
def average_block_variance(data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES) -> float:
    variances = 0
    num_blocks = 0
    for block in blocks(data, block_size_bytes):
        variances += variance(block)
        num_blocks += 1
    return variances / num_blocks


@mark_byte_array_func
def average_block_standard_deviation(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    deviations = 0
    num_blocks = 0
    for block in blocks(data, block_size_bytes):
        deviations += standard_deviation(block)
        num_blocks += 1
    return deviations / num_blocks


def num_equal(data1: Iterable, data2: Iterable) -> Tuple[int, int]:
    total = num = 0
    for val1, val2 in zip(data1, data2):
        total += 1
        if val1 == val2:
            num += 1
    return num, total


def percent_iterables_equal(data1: Iterable, data2: Iterable) -> float:
    num, total = num_equal(data1, data2)
    return 100.0 * (num / total)


@mark_byte_arrays_func
def percent_bytes_equal(data1: bytes, data2: bytes) -> float:
    return percent_iterables_equal(data1, data2)


@mark_byte_arrays_func
def percent_bits_equal(data1: bytes, data2: bytes) -> float:
    nums = [num_equal(_bin(b1), _bin(b2))[0] for b1, b2 in zip(data1, data2)]
    return 100.0 * sum(nums) / (len(nums) * 8)


@mark_byte_array_func
def average_abs_difference_between_bytes(data: bytes) -> float:
    data_len_min_1 = len(data) - 1
    # Special cases
    if data_len_min_1 < 1:
        return 0
    diff_sum = 0
    for idx in range(0, data_len_min_1):
        diff_sum += abs(data[idx] - data[idx + 1])
    return diff_sum / data_len_min_1


@mark_byte_arrays_func
def average_abs_difference_between_byte_arrays(data1: bytes, data2: bytes) -> float:
    data1_len_min_1 = len(data1) - 1
    data2_len_min_1 = len(data2) - 1
    # Special cases
    if data1_len_min_1 < 0 or data2_len_min_1 < 0:
        return 0
    diff_sum = 0
    for byte1, byte2 in zip(data1, data2):
        diff_sum += abs(byte1 - byte2)
    return diff_sum / (min(data1_len_min_1, data2_len_min_1) + 1)


def get_byte_array_analysis_funcs() -> dict[str, ByteArrayCallableT]:
    funcs = {}
    for name, obj in globals().items():
        if (
            callable(obj)
            and hasattr(obj, _MARK_BYTE_ARRAY_ATTR)
            and getattr(obj, _MARK_BYTE_ARRAY_ATTR)
        ):
            funcs[name] = obj
    return funcs


def get_byte_arrays_analysis_funcs() -> dict[str, ByteArraysCallableT]:
    funcs = {}
    for name, obj in globals().items():
        if (
            callable(obj)
            and hasattr(obj, _MARK_BYTE_ARRAYS_ATTR)
            and getattr(obj, _MARK_BYTE_ARRAYS_ATTR)
        ):
            funcs[name] = obj
    return funcs


BYTE_ARRAY_ANAL_FUNCS = get_byte_array_analysis_funcs()
BYTE_ARRAYS_ANAL_FUNCS = get_byte_arrays_analysis_funcs()


if __name__ == "__main__":
    print(BYTE_ARRAY_ANAL_FUNCS)
    print(len(BYTE_ARRAY_ANAL_FUNCS))
    print(len(BYTE_ARRAYS_ANAL_FUNCS))
    # TODO: turn these into unit tests
    # print(percent_of_bytes_bits_0_to_1_eq_6_to_7(b"\xc3\xc4\xc5\x82\x00"))
    # print(percent_of_bytes_bits_0_to_1_eq_6_to_7(b"\xc3"))
    # print(percent_of_bytes_bits_0_to_1_eq_6_to_7(b"\xc3\x01"))
    # print(percent_of_bytes_bits_0_to_1_eq_6_to_7(b"\xc3\xc4\xc5"))
