"""`compression` module tests"""
import os
import struct
from typing import Optional
import unittest

# TODO: proper way to handle unittest files for pylint?
from compression import compress, CompressionType, decompress


def _rand_data(length: Optional[int] = None) -> bytes:
    if not length:
        length = struct.unpack("<H", os.urandom(2))[0] or 1
    return os.urandom(length)


class TestCompressDecompress(unittest.TestCase):
    """Tests for the `compress` and `decompress` functions"""
    # TODO: these test basic functionality. More unit tests are possible

    def _run_comp_decomp_test(self,
                              compression_type: CompressionType,
                              length: Optional[int] = None,
                              num_iters: int = 20):
        for iteration in range(num_iters):
            orig_data = _rand_data(length=length)
            with self.subTest(data=orig_data,
                              iteration=iteration,
                              compression_type=compression_type):
                comp_data = compress(orig_data, compression_type)
                decomp_data = decompress(comp_data, compression_type)
                self.assertEqual(orig_data, decomp_data)

    def test_gzip_random_binary_data_random_length(self):
        """gzip compress & decompress random binary data or random length"""
        self._run_comp_decomp_test(CompressionType.GZIP)

    def test_lzma_random_binary_data_random_length(self):
        """lzma compress & decompress random binary data or random length"""
        self._run_comp_decomp_test(CompressionType.LZMA)

    def test_bz2_random_binary_data_random_length(self):
        """bz2 compress & decompress random binary data or random length"""
        self._run_comp_decomp_test(CompressionType.BZ2)

    def test_zlib_random_binary_data_random_length(self):
        """zlib compress & decompress random binary data or random length"""
        self._run_comp_decomp_test(CompressionType.ZLIB)

    def test_tar_random_binary_data_random_length(self):
        """tar compress & decompress random binary data or random length"""
        self._run_comp_decomp_test(CompressionType.TAR)

    def test_tar_gz_random_binary_data_random_length(self):
        """tar_gz compress & decompress random binary data or random length"""
        self._run_comp_decomp_test(CompressionType.TAR_GZ)

    def test_tar_bz2_random_binary_data_random_length(self):
        """tar_bz2 compress & decompress random binary data or random length"""
        self._run_comp_decomp_test(CompressionType.TAR_BZ2)

    def test_tar_xz_random_binary_data_random_length(self):
        """tar_xz compress & decompress random binary data or random length"""
        self._run_comp_decomp_test(CompressionType.TAR_XZ)
