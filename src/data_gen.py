#!/usr/bin/env python3
"""Data (plaintext and ciphertext) generation script.
Written in Python because the overhead of doing this in C/C++ may not be
worth it. If it is worth it, then we can do it later.
"""

import argparse
import enum
# TODO: multiprocessing
# TODO: pass work jobs to distributed processing stuff. Especially large
#       jobs and especially since data will go into a DB.
import multiprocessing
import os
import sys
from typing import List

from .compression import CompressionType
from .crypto.types import CipherType
from .utils import BetterEnum


class DataType(BetterEnum):
    """Types of random data to generate"""
    ASCII = "ASCII"
    BINARY = "BIN"
    SPARSE_ASCII = "SPARSE_ASCII"
    SPARSE_BIN = "SPARSE_BIN"


def main(args: List[str]) -> int:
    """main returns exit code"""
    parser = argparse.ArgumentParser(
        description="Generate plaintext and ciphertext data for test and "
                    "training data sets")
    parser.add_argument(
        "data_type",
        help="Type of data to randomly generate",
        nargs="+",
        choices=DataType.values())
    parser.add_argument(
        "-c", "--compress",
        help="Whether or not to compress generated plaintexts and if so, "
             "what compression algorithm",
        choices=CompressionType.values())
    parser.add_argument(
        "-e", "--encrypt-algs",
        help="Ciphers to use to encrypt data. If compression is enabled, "
             "encryption takes place on the compressed data. If not, on the "
             "plaintext",
        choices=CipherType.values(),
        nargs="+")
    # TODO: doesn't jive well with accepting multiple ciphers. Maybe accept
    # "ALG-<KEY_SIZE>" (so probably not an enum for encrypt algs since that'd be
    # quite a large list)
    # parser.add_argument(
    #     "--key-size",
    #     help="Key size (in bits) to use for encryption",
    #     type=int)
    parsed_args = parser.parse_args(args)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

