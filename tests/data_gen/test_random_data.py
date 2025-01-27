"""`utils` module tests"""
import os
import unittest

from data_gen.random_data import ASCII_RANGE, rand_int_in_range


class TestRandIntInRange(unittest.TestCase):
    """`rand_int_in_range` function"""
    # TODO: more tests: negative numbers?

    def _run_range_test(self, int_range, iterations: int = 1000):
        for iteration in range(iterations):
            with self.subTest(iteration=iteration, iterations=iterations,
                              int_range=int_range):
                value = rand_int_in_range(int_range[0], int_range[1])
                self.assertTrue(value in range(int_range[0], int_range[1]))

    def test_small_range_subset(self):
        """small range that's a proper subset of possible values"""
        self._run_range_test((5, 10))

    def test_large_range_subset(self):
        """larger range that's a proper subset of possible values"""
        self._run_range_test((5, 2**30))

    def test_all_possible_values_as_range(self):
        """All possible 4-byte unsigned integers"""
        self._run_range_test((0, 2**32))

    def test_low_equals_high(self):
        """low equals high"""
        low = 0
        while low < 2**32:
            skip_len = 2 if low % 2 else 3
            low += int.from_bytes(os.urandom(skip_len),
                                  byteorder="little") or 2
            self._run_range_test((low, low + 1), 100)

    def test_gen_ascii(self):
        """`rand_int_in_range` using the `ASCII_RANGE` in the utils module"""
        for iteration in range(1000):
            with self.subTest(iteration=iteration):
                value = rand_int_in_range(ASCII_RANGE[0], ASCII_RANGE[1])
                # Try to decode as ASCII. It'll raise an exception if it fails
                int.to_bytes(value, length=1,
                             byteorder="little").decode("ASCII")
