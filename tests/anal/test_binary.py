from mlc.anal.binary import (
    average_abs_difference_between_byte_arrays,
    average_abs_difference_between_bytes,
    average_byte,
    average_byte_int,
    average_num_bits_off,
    average_num_bits_on,
    most_common_byte,
    percent_bits_equal,
    percent_bytes_with_bit_x_on,
    percent_bytes_with_bit_x_off,
)


def test_all_same_value():
    assert average_byte(b"\x00" * 20) == 0.0
    assert average_byte_int(b"\x00" * 20) == 0
    assert average_byte(b"\x11" * 20) == 17.0
    assert average_byte_int(b"\x11" * 20) == 17
    assert average_byte(b"\xfe" * 20) == 254.0
    assert average_byte_int(b"\xfe" * 20) == 254
    assert average_byte(b"\xff" * 20) == 255.0
    assert average_byte_int(b"\xff" * 20) == 255


def test_percent_bits_equal():
    assert percent_bits_equal(b"abc", b"abc") == 100.0
    assert round(percent_bits_equal(b"ab" + b"\xa0", b"ab" + b"\xa1"), 2) == round(
        100.0 * (23 / 24), 2
    )
    assert round(percent_bits_equal(b"a\x00c", b"a\xffc"), 2) == round(100.0 * 2 / 3, 2)
    assert percent_bits_equal(b"\xff" * 3, b"\x00" * 3) == 0.0
    assert round(percent_bits_equal(b"\xff" * 3, b"\x00" * 2 + b"\xff"), 2) == round(
        100.0 * 1 / 3, 2
    )


def test_average_abs_difference_between_bytes():
    # TODO: could use more cases
    assert average_abs_difference_between_bytes(b"abcdef") == 1
    assert average_abs_difference_between_bytes(b"ace") == 2
    assert average_abs_difference_between_bytes(b"aaaa") == 0
    assert average_abs_difference_between_bytes(b"aaa") == 0
    assert average_abs_difference_between_bytes(b"aa") == 0
    assert average_abs_difference_between_bytes(b"a") == 0
    assert average_abs_difference_between_bytes(b"") == 0


def test_average_abs_difference_between_byte_arrays():
    # TODO: could use more cases
    assert average_abs_difference_between_byte_arrays(b"abcdef", b"abcdef") == 0
    assert average_abs_difference_between_byte_arrays(b"ace", b"cag") == 2
    assert round(average_abs_difference_between_byte_arrays(b"ace", b"caf"), 2) == round(5 / 3, 2)
    assert average_abs_difference_between_byte_arrays(b"aaaa", b"aaaa") == 0
    assert average_abs_difference_between_byte_arrays(b"aaa", b"aaa") == 0
    assert average_abs_difference_between_byte_arrays(b"aa", b"aa") == 0
    assert average_abs_difference_between_byte_arrays(b"a", b"a") == 0
    assert average_abs_difference_between_byte_arrays(b"", b"") == 0
