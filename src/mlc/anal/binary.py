from typing import Callable


def _bin(byte: int) -> str:
    return "{:08b}".format(byte)


def average_byte(data: bytes) -> float:
    return sum(data) / len(data)


def average_byte_int(data: bytes) -> int:
    return sum(data) // len(data)


def most_common_byte(data: bytes) -> int:
    """In case of collisions, highest byte is returned"""
    counts = {(data.count(b), b) for b in range(256)}
    # Sort by count (and then byte value in case of collisions)
    # Grab last element (highest count)
    # Return byte value
    return sorted(counts)[-1][1]


def average_num_bits_on(data: bytes) -> float:
    return sum(_bin(byte).count("1") for byte in data) / len(data)


def average_num_bits_off(data: bytes) -> float:
    return sum(_bin(byte).count("0") for byte in data) / len(data)


def percent_bytes_with_bit_x_on(data: bytes, bit: int) -> float:
    assert 0 <= bit <= 7
    bit = 1 << bit
    return 100.0 * len([byte for byte in data if byte & bit]) / len(data)


def percent_bytes_with_bit_x_off(data: bytes, bit: int) -> float:
    assert 0 <= bit <= 7
    bit = 1 << bit
    return 100.0 * len([byte for byte in data if byte & bit == 0]) / len(data)


def nib1(byte: int) -> int:
    return byte & 0x0F


def nib2(byte: int) -> int:
    return (byte & 0xF0) >> 4


def percent_bytes_first_nibble_gt_second_nibble(data: bytes) -> float:
    return 100.0 * sum([1 for byte in data if nib1(byte) > nib2(byte)]) / len(data) 


def percent_bytes_first_nibble_ge_second_nibble(data: bytes) -> float:
    return 100.0 * sum([1 for byte in data if nib1(byte) >= nib2(byte)]) / len(data) 


def percent_bytes_first_nibble_lt_second_nibble(data: bytes) -> float:
    return 100.0 * sum([1 for byte in data if nib1(byte) < nib2(byte)]) / len(data) 


def percent_bytes_first_nibble_le_second_nibble(data: bytes) -> float:
    return 100.0 * sum([1 for byte in data if nib1(byte) <= nib2(byte)]) / len(data) 


def percent_bytes_first_nibble_eq_second_nibble(data: bytes) -> float:
    return 100.0 * sum([1 for byte in data if nib1(byte) == nib2(byte)]) / len(data) 


def percent_bytes_first_nibble_eq_complement_of_second_nibble(data: bytes) -> float:
    return 100.0 * sum([1 for byte in data if nib1(byte) == ~nib2(byte)]) / len(data) 


def _mirror(byte: int) -> int:
    # bit-reverse input int (range [0, 255])
    return int("{:08b}".format(byte)[::-1], 2)


def percent_bytes_first_nibble_eq_mirror_of_second_nibble(data: bytes) -> float:
    return 100.0 * sum([1 for byte in data if nib1(byte) == _mirror(nib2(byte))]) / len(data) 


percent_bytes_with_bit_0_on = lambda data: percent_bytes_with_bit_x_on(data, 0)
percent_bytes_with_bit_1_on = lambda data: percent_bytes_with_bit_x_on(data, 1)
percent_bytes_with_bit_2_on = lambda data: percent_bytes_with_bit_x_on(data, 2)
percent_bytes_with_bit_3_on = lambda data: percent_bytes_with_bit_x_on(data, 3)
percent_bytes_with_bit_4_on = lambda data: percent_bytes_with_bit_x_on(data, 4)
percent_bytes_with_bit_5_on = lambda data: percent_bytes_with_bit_x_on(data, 5)
percent_bytes_with_bit_6_on = lambda data: percent_bytes_with_bit_x_on(data, 6)
percent_bytes_with_bit_7_on = lambda data: percent_bytes_with_bit_x_on(data, 7)
percent_bytes_with_bit_0_off = lambda data: percent_bytes_with_bit_x_off(data, 0)
percent_bytes_with_bit_1_off = lambda data: percent_bytes_with_bit_x_off(data, 1)
percent_bytes_with_bit_2_off = lambda data: percent_bytes_with_bit_x_off(data, 2)
percent_bytes_with_bit_3_off = lambda data: percent_bytes_with_bit_x_off(data, 3)
percent_bytes_with_bit_4_off = lambda data: percent_bytes_with_bit_x_off(data, 4)
percent_bytes_with_bit_5_off = lambda data: percent_bytes_with_bit_x_off(data, 5)
percent_bytes_with_bit_6_off = lambda data: percent_bytes_with_bit_x_off(data, 6)
percent_bytes_with_bit_7_off = lambda data: percent_bytes_with_bit_x_off(data, 7)


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


def percent_bytes_lt_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _lt_op)


def percent_bytes_le_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _le_op)


def percent_bytes_gt_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _gt_op)


def percent_bytes_ge_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _ge_op)


def percent_bytes_eq_next_byte(data: bytes) -> float:
    return _percent_op_next_byte(data, _eq_op)


def _set_up_percent_bytes_with_bits_funcs():
    for bit_len in range(1, 9):
        for patt in range(0, 2 ** bit_len):
            patt = ("{:0" + str(bit_len) + "b}").format(patt)
            func_name = f"percent_of_bytes_with_bits_{patt}"
            globals()[func_name] = lambda data: 100.0 * sum([1 for byte in data if patt in _bin(byte)]) / len(data)


_set_up_percent_bytes_with_bits_funcs()


def _set_up_percent_bytes_gt_funcs():
    for num in range(1, 255):
        func_name = f"percent_of_bytes_gt_{num}"
        globals()[func_name] = lambda data: 100.0 * sum([1 for byte in data if
                                                         byte > num]) / len(data)


_set_up_percent_bytes_gt_funcs()


def average_max_per_block(data: bytes, block_size_bytes: 8) -> float:
    # TODO: unit test
    # TODO: same for min
    # TODO: same for max - min
    max_sums = 0
    for idx in range(0, len(data) - block_size_bytes, block_size_bytes):
        block = data[idx, idx + block_size_bytes]
        max_sums += max(block)
    return max_sums / (len(data) // block_size_bytes)


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
