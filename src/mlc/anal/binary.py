

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
    return sum(bin(byte)[2:].count("1") for byte in data) / len(data)


def average_num_bits_off(data: bytes) -> float:
    return sum(bin(byte)[2:].count("0") for byte in data) / len(data)


def percent_bytes_with_bit_x_on(data: bytes, bit: int) -> float:
    assert 0 <= bit <= 7
    bit = 1 << bit
    return 100.0 * len([byte for byte in data if byte & bit]) / len(data)


def percent_bytes_with_bit_x_off(data: bytes, bit: int) -> float:
    assert 0 <= bit <= 7
    bit = 1 << bit
    return 100.0 * len([byte for byte in data if byte & bit == 0]) / len(data)


print(most_common_byte(b"aaaaaaac"))
print(average_num_bits_on(b"\x00\x00\x01"))
for bit in range(0, 8):
    print(percent_bytes_with_bit_x_on(b"\xFF\xFF\xFF", bit))
    print(percent_bytes_with_bit_x_off(b"\xFF\xFF\xFF", bit))
print(percent_bytes_with_bit_x_on(b"\xFF\xF0\xF1", 0))
# print(average_num_bits_on(b"\x00\x00\x00"))
