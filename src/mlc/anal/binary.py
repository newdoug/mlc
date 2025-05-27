from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import math
import subprocess
import tempfile
from typing import Callable


_MARK_ATTR = "is_anal"
DEFAULT_BLOCK_SIZE_BYTES: int = 8


def mark(f: Callable) -> Callable:
    setattr(f, _MARK_ATTR, True)
    return f


def set_default_block_size(block_size_bytes: int) -> int:
    global DEFAULT_BLOCK_SIZE_BYTES
    DEFAULT_BLOCK_SIZE_BYTES = block_size_bytes


def blocks(data: bytes, block_size_bytes: int) -> list[bytes]:
    for idx in range(0, len(data) - block_size_bytes, block_size_bytes):
        yield data[idx, idx + block_size_bytes]


def _bin(byte: int) -> str:
    return "{:08b}".format(byte)


def lower_nibble(byte: int) -> int:
    return byte & 0x0F


def upper_nibble(byte: int) -> int:
    return (byte & 0xF0) >> 4


def num_bits_on(byte: int) -> int:
    return _bin(byte).count("1")


def num_bits_off(byte: int) -> int:
    return _bin(byte).count("0")


@mark
def average_byte(data: bytes) -> float:
    return sum(data) / len(data)


@mark
def average_byte_int(data: bytes) -> int:
    return sum(data) // len(data)


@mark
def average_bit(data: bytes) -> float:
    return sum([num_bits_on(byte) for byte in data]) / (len(data) * 8)


@mark
def average_nibble(data: bytes) -> float:
    return sum([lower_nibble(byte) + upper_nibble(byte) for byte in data]) / (
        len(data) * 2
    )


@mark
def average_upper_nibble(data: bytes) -> float:
    return sum([upper_nibble(byte) for byte in data]) / len(data)


@mark
def average_lower_nibble(data: bytes) -> float:
    return sum([lower_nibble(byte) for byte in data]) / len(data)


@mark
def most_common_byte(data: bytes) -> int:
    """In case of collisions, highest byte is returned"""
    counts = {(data.count(b), b) for b in range(256)}
    # Sort by count (and then byte value in case of collisions)
    # Grab last element (highest count)
    # Return byte value
    return sorted(counts)[-1][1]


@mark
def average_num_bits_on(data: bytes) -> float:
    return sum([num_bits_on(byte) for byte in data]) / len(data)


@mark
def average_num_bits_off(data: bytes) -> float:
    return sum([num_bits_off(byte) for byte in data]) / len(data)


@mark
def percent_bytes_with_bit_x_on(data: bytes, bit: int) -> float:
    assert 0 <= bit <= 7
    bit = 1 << bit
    return 100.0 * len([byte for byte in data if byte & bit]) / len(data)


@mark
def percent_bytes_with_bit_x_off(data: bytes, bit: int) -> float:
    assert 0 <= bit <= 7
    bit = 1 << bit
    return 100.0 * len([byte for byte in data if byte & bit == 0]) / len(data)


@mark
def percent_bytes_first_nibble_gt_second_nibble(data: bytes) -> float:
    return (
        100.0
        * sum([1 for byte in data if lower_nibble(byte) > upper_nibble(byte)])
        / len(data)
    )


@mark
def percent_bytes_first_nibble_ge_second_nibble(data: bytes) -> float:
    return (
        100.0
        * sum([1 for byte in data if lower_nibble(byte) >= upper_nibble(byte)])
        / len(data)
    )


@mark
def percent_bytes_first_nibble_lt_second_nibble(data: bytes) -> float:
    return (
        100.0
        * sum([1 for byte in data if lower_nibble(byte) < upper_nibble(byte)])
        / len(data)
    )


@mark
def percent_bytes_first_nibble_le_second_nibble(data: bytes) -> float:
    return (
        100.0
        * sum([1 for byte in data if lower_nibble(byte) <= upper_nibble(byte)])
        / len(data)
    )


@mark
def percent_bytes_first_nibble_eq_second_nibble(data: bytes) -> float:
    return (
        100.0
        * sum([1 for byte in data if lower_nibble(byte) == upper_nibble(byte)])
        / len(data)
    )


@mark
def percent_bytes_first_nibble_eq_complement_of_second_nibble(data: bytes) -> float:
    return (
        100.0
        * sum([1 for byte in data if lower_nibble(byte) == ~upper_nibble(byte)])
        / len(data)
    )


def _mirror(byte: int) -> int:
    # bit-reverse input int (range [0, 255])
    return int("{:08b}".format(byte)[::-1], 2)


@mark
def percent_bytes_first_nibble_eq_mirror_of_second_nibble(data: bytes) -> float:
    return (
        100.0
        * sum([1 for byte in data if lower_nibble(byte) == _mirror(upper_nibble(byte))])
        / len(data)
    )


percent_bytes_with_bit_0_on = mark(lambda data: percent_bytes_with_bit_x_on(data, 0))
percent_bytes_with_bit_1_on = mark(lambda data: percent_bytes_with_bit_x_on(data, 1))
percent_bytes_with_bit_2_on = mark(lambda data: percent_bytes_with_bit_x_on(data, 2))
percent_bytes_with_bit_3_on = mark(lambda data: percent_bytes_with_bit_x_on(data, 3))
percent_bytes_with_bit_4_on = mark(lambda data: percent_bytes_with_bit_x_on(data, 4))
percent_bytes_with_bit_5_on = mark(lambda data: percent_bytes_with_bit_x_on(data, 5))
percent_bytes_with_bit_6_on = mark(lambda data: percent_bytes_with_bit_x_on(data, 6))
percent_bytes_with_bit_7_on = mark(lambda data: percent_bytes_with_bit_x_on(data, 7))
percent_bytes_with_bit_0_off = mark(lambda data: percent_bytes_with_bit_x_off(data, 0))
percent_bytes_with_bit_1_off = mark(lambda data: percent_bytes_with_bit_x_off(data, 1))
percent_bytes_with_bit_2_off = mark(lambda data: percent_bytes_with_bit_x_off(data, 2))
percent_bytes_with_bit_3_off = mark(lambda data: percent_bytes_with_bit_x_off(data, 3))
percent_bytes_with_bit_4_off = mark(lambda data: percent_bytes_with_bit_x_off(data, 4))
percent_bytes_with_bit_5_off = mark(lambda data: percent_bytes_with_bit_x_off(data, 5))
percent_bytes_with_bit_6_off = mark(lambda data: percent_bytes_with_bit_x_off(data, 6))
percent_bytes_with_bit_7_off = mark(lambda data: percent_bytes_with_bit_x_off(data, 7))


def _percent_op_next_byte(data: bytes, op: Callable) -> float:
    if len(data) < 2:
        return 0.0
    occ = 0
    for idx in range(0, len(data) - 1):
        if op(ata[idx], data[idx + 1]):
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


@mark
def percent_bytes_lt_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _lt_op)


@mark
def percent_bytes_le_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _le_op)


@mark
def percent_bytes_gt_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _gt_op)


@mark
def percent_bytes_ge_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _ge_op)


@mark
def percent_bytes_eq_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _eq_op)


def _set_up_percent_bytes_with_bits_funcs():
    for bit_len in range(1, 9):
        for patt in range(0, 2**bit_len):
            patt = ("{:0" + str(bit_len) + "b}").format(patt)
            func_name = f"percent_of_bytes_with_bits_{patt}"
            globals()[func_name] = mark(
                lambda data: 100.0
                * sum([1 for byte in data if patt in _bin(byte)])
                / len(data)
            )


_set_up_percent_bytes_with_bits_funcs()


def _set_up_percent_bytes_gt_funcs():
    for num in range(1, 255):
        func_name = f"percent_of_bytes_gt_{num}"
        globals()[func_name] = mark(
            lambda data: 100.0 * sum([1 for byte in data if byte > num]) / len(data)
        )


_set_up_percent_bytes_gt_funcs()


def _set_up_percent_freq_each_byte_funcs():
    for num in range(0, 256):
        func_name = f"percent_of_bytes_eq_{num}"
        globals()[func_name] = mark(lambda data: 100.0 * data.count(num) / len(data))


_set_up_percent_freq_each_byte_funcs()


def _set_up_percent_of_blocks_with_byte_in_pos_funcs(
    pos: int, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
):
    for num in range(0, 256):
        func_name = f"percent_of_blocks_idx_{pos}_eq_{num}"
        globals()[func_name] = mark(
            lambda data: 100.0
            * len([block for block in blocks(data) if block[pos] == num])
            / (len(data) / block_size_bytes)
        )


for pos in range(DEFAULT_BLOCK_SIZE_BYTES):
    _set_up_percent_of_blocks_with_byte_in_pos_funcs(
        pos, block_size_bytes=DEFAULT_BLOCK_SIZE_BYTES
    )


def _average_block_op(
    data: bytes, op: Callable, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    sums = sum(op(block) for block in blocks(data, block_size_bytes))
    return sums / (len(data) // block_size_bytes)


@mark
def average_block_max(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    return _average_block_op(data, max, block_size_bytes=block_size_bytes)


@mark
def average_block_min(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    return _average_block_op(data, min, block_size_bytes=block_size_bytes)


@mark
def average_block_max_minus_min(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    return _average_block_op(
        data, lambda block: max(block) - min(block), block_size_bytes=block_size_bytes
    )


@mark
def calc_entropy(data: bytes) -> float:
    freq = Counter(data)
    return -sum((c / len(data)) * math.log2(c / len(data)) for c in freq.values())


@mark
def calc_chi_square(data: bytes) -> float:
    expected = len(data) / 256  # Expected frequency for uniform distribution
    freq = Counter(data)

    chi2 = 0.0
    for byte_val in range(256):
        observed = freq.get(byte_val, 0)
        chi2 += ((observed - expected) ** 2) / expected

    return chi2


@dataclass
class EntResults:
    """Useful outputs of `ent -t <filename>`"""

    entropy: float
    chi_square: float
    mean: float
    monte_carlo_pi: float
    serial_correlation: float


# If data is only run serially through functions in this file, then 1 would be sufficient, but in cases of
# multi-threading or multi-processing, more cache entries would be needed to be useful
@lru_cache(maxsize=64)
def run_ent(data: bytes) -> EntResults:
    with tempfile.NamedTemporaryFile() as temp_file:
        filename = temp_file.name
        with open(filename, "wb") as handle:
            handle.write(data)
        result = subprocess.run(["ent", "-t", filename], stdout=subprocess.PIPE)
        lines = [line.strip() for line in result.stdout.decode().split("\n")]
        values = [value.strip() for value in lines[1].split(",")]
        return EntResults(
            entropy=float(values[2]),
            chi_square=float(values[3]),
            mean=float(values[4]),
            monte_carlo_pi=float(values[5]),
            serial_correlation=float(values[6]),
        )


@mark
def ent_entropy(data: bytes) -> float:
    return run_ent(data).entropy


@mark
def ent_chi_square(data: bytes) -> float:
    return run_ent(data).chi_square


@mark
def ent_monte_carlo_pi(data: bytes) -> float:
    return run_ent(data).monte_carlo_pi


@mark
def ent_serial_correlation(data: bytes) -> float:
    return run_ent(data).serial_correlation


@mark
def ent_entropy_block_average(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    block_vals = [
        run_ent(block).entropy
        for block in blocks(data, block_size_bytes=block_size_bytes)
    ]
    return sum(block_vals) / len(block_vals)


@mark
def ent_chi_square_block_average(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    block_vals = [
        run_ent(block).chi_square
        for block in blocks(data, block_size_bytes=block_size_bytes)
    ]
    return sum(block_vals) / len(block_vals)


@mark
def ent_monte_carlo_pi_block_average(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    block_vals = [
        run_ent(block).monte_carlo_pi
        for block in blocks(data, block_size_bytes=block_size_bytes)
    ]
    return sum(block_vals) / len(block_vals)


@mark
def ent_serial_correlation_bkock_average(
    data: bytes, block_size_bytes: int = DEFAULT_BLOCK_SIZE_BYTES
) -> float:
    block_vals = [
        run_ent(block).serial_correlation
        for block in blocks(data, block_size_bytes=block_size_bytes)
    ]
    return sum(block_vals) / len(block_vals)


def bits_on_indices(byte: int) -> list[int]:
    byte = _bin(byte)[::-1]
    return [i for i in range(len(byte)) if byte[i] == "1"]


@mark
def average_on_bit_position_8bits(data: bytes) -> float:
    # TODO: unit test
    # TODO: 4 bits, 16 bits
    total_sum = 0
    for byte in data:
        on = bits_on_indices(byte)
        total_sum += sum(on)
    return total_sum / (len(data) * 8)


# TODO: track occurrences and frequencies of all byte strings <= length 5? 4? 8?
# TODO: detect clusters of bytes that are close to each other in value? E.g.
# \xAB\x29\x63\x66\x62\x5F\x72 might trigger "bytes '\x63\x66\x62\x5F'
# adjacent bytes were close in value (like a cluster).
#   - Maybe a clustering algorithm?
# TODO: perform various transformations on the data (linear, non-linear, steps
# of AES, etc.) and then perform binary analysis on that too.
# TODO: track if any correlations between plaintext and ciphertext exist? What
# about between plaintext and transformed ciphertext? What about between
# ciphertext and transformed plaintext? What about between transformed plaintext
# and transformed ciphertext?
# TODO: use various transformations (probably pieces of AES) on blocks/plaintext/ciphertext using just
# piece of known key and compare those transformations with other values?
# Plaintext? Ciphertext? Single blocks of plaintext? Single blocks of
# ciphertext? Transformed ciphertext? Etc.
# TODO: most common bit position (4, 8, and 16 bits)
# TODO: basic frequency of each byte. Of each 16 bits?
# TODO: similar functions, but on nibbles level
# TODO: similar functions, but on 16-bit level
# TODO: similar functions, but per block and between each possible pair of bytes in an 8-byte block
#       idk what I mean by this
# TODO: percent similarity between plaintext and ciphertext
# TODO: check for recurring patterns of bits


def get_analysis_funcs() -> dict[str, Callable]:
    funcs = {}
    for name, obj in globals().items():
        if callable(obj) and hasattr(obj, _MARK_ATTR) and getattr(obj, _MARK_ATTR):
            funcs[name] = obj
    return funcs


ANAL_FUNCS = get_analysis_funcs()
print(ANAL_FUNCS)
print(len(ANAL_FUNCS))
