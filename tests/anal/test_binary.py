import unittest

from mlc.anal.binary import (
    average_byte,
    average_byte_int,
    most_common_byte,
    average_num_bits_on,
    average_num_bits_off,
    percent_bytes_with_bit_x_on,
    percent_bytes_with_bit_x_off,
)


class TestAverageByte(unittest.TestCase):
    def test_all_same_value(self):
        self.assertEqual(average_byte(b"\x00" * 20), 0.0)
        self.assertEqual(average_byte_int(b"\x00" * 20), 0)
        self.assertEqual(average_byte(b"\x11" * 20), 17.0)
        self.assertEqual(average_byte_int(b"\x11" * 20), 17)
        self.assertEqual(average_byte(b"\xfe" * 20), 254.0)
        self.assertEqual(average_byte_int(b"\xfe" * 20), 255)
