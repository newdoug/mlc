"""`compression` module tests"""

import os
import struct
from typing import Optional

from mlc.compression import compress, CompressionType, decompress
from mlc.data_gen.random_data import rand_bytes, rand_uint16

import zstd


def _rand_data(length: Optional[int] = None) -> bytes:
    """This has a default case unlike `rand_bytes` in `utils.rand`"""
    if not length:
        length = rand_uint16() or 1
    return rand_bytes(length)


# TODO: these test basic functionality. More unit tests are possible


def _run_comp_decomp_test(
    compression_type: CompressionType,
    length: Optional[int] = None,
    num_iters: int = 20,
):
    for iteration in range(num_iters):
        # Generate random data
        orig_data = _rand_data(length=length)
        # Verify compress function doesn't raise an exception on any data
        comp_data = compress(orig_data, compression_type)
        # Verify decompress function doesn't raise an exception on any data
        decomp_data = decompress(comp_data, compression_type)
        # Verifies decompress(compress(data)) == data, as it usually generally should
        assert orig_data == decomp_data, (
            f"Failed with data '{orig_data.hex()}', iteration '{iteration}', "
            f"compression_type '{compression_type}'"
        )


def test_gzip_random_binary_data_random_length():
    """gzip compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.GZIP)


def test_lzma_random_binary_data_random_length():
    """lzma compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.LZMA)


def test_bz2_random_binary_data_random_length():
    """bz2 compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.BZ2)


def test_zlib_random_binary_data_random_length():
    """zlib compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.ZLIB)


def test_tar_random_binary_data_random_length():
    """tar compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.TAR)


def test_tar_gz_random_binary_data_random_length():
    """tar_gz compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.TAR_GZ)


def test_tar_bz2_random_binary_data_random_length():
    """tar_bz2 compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.TAR_BZ2)


def test_tar_xz_random_binary_data_random_length():
    """tar_xz compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.TAR_XZ)


def test_zstd_random_binary_data_random_length():
    """zstd compress & decompress random binary data of random length"""
    _run_comp_decomp_test(CompressionType.ZSTD)
