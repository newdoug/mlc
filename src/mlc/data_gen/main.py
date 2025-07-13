#!/usr/bin/env python3
"""Data (plaintext and ciphertext) generation script.
Written in Python because the overhead of doing this in C/C++ may not be
worth it. If it is worth it, then we can do it later.
"""

import argparse
import enum

# TODO: pass work jobs to distributed processing stuff. Especially large
#       jobs and especially since data will go into a DB.
import multiprocessing
import os
import sys
import tempfile
from typing import Iterable, List, Tuple

from mlc.compression import compress, CompressionType
from mlc.crypto.cipher_types import CipherType
from mlc.data_gen.data_type_base import DataTypeSettingKey
from mlc.data_gen.random_data import RandomDataType, rand_int_in_range
from mlc.utils.config import load_config
from mlc.utils.io import eprint, LOG, set_up_logger
from mlc.utils.log_db_handler import DatabaseLogHandler
from mlc.startup import pg


def _gen_out_filename() -> str:
    with tempfile.NamedTemporaryFile(
        prefix="gen_data_", suffix=".csv", delete=False, dir=os.getcwd()
    ) as temp_file:
        return temp_file.name


def _get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate plaintext and ciphertext data for test and training data sets"
    )
    # TODO: update this to support split output files, direct to DB, to a dir with automatically split files, etc.
    parser.add_argument(
        "-o",
        "--output",
        help="Filename to write the output file to. If not provided, a default filename will be generated",
        type=str,
    )
    parser.add_argument(
        "--random-data",
        help="Generate these types of random dat",
        nargs="+",
        type=str,
        choices=RandomDataType.names(),
    )
    parser.add_argument(
        "-n",
        "--num-samples",
        help="Number of samples to generate",
        type=int,
    )
    parser.add_argument(
        "--size-range",
        help="Range (in bytes) of lengths of generated data samples",
        nargs=2,
        type=int,
    )
    # Compression arguments
    parser.add_argument(
        "--compress",
        help="Whether or not to compress generated plaintexts and if so, "
        "what compression algorithm",
        choices=CompressionType.names(),
    )
    parser.add_argument(
        "--keep-uncompressed",
        help="Only matters if --compress is also given. If set, both the compressed and uncompressed sample is "
        "generated and possibly encrypted",
        action="store_true",
    )
    # Encryption arguments
    parser.add_argument(
        "--cipher",
        help="Cipher(s) to use to encrypt data. If compression is enabled, "
        "encryption takes place on the compressed data. If not, on the "
        "plaintext",
        choices=CipherType.names(),
        nargs="+",
        default=[],
    )
    parser.add_argument(
        "--key-size",
        help="Key size (in bits) to use for encryption",
        type=int,
        default=256,
    )
    parser.add_argument(
        "--num-encryptions",
        help="Number of times (different keys and/or IVs) to encrypt each sample",
        default=1,
        type=int,
    )
    return parser


def _gen_plaintext_samples(
    num_samples: int, size_range: Tuple[int, int], data_type: RandomDataType
) -> Iterable[bytes]:
    for _ in range(num_samples):
        length = rand_int_in_range(size_range[0], size_range[1])
        yield data_type.generate(
            {
                DataTypeSettingKey.LENGTH.name: length,
            }
        )


# TODO: finish data gen (e.g., here)
def _compress_samples(
    samples: Iterable[bytes], compression_type: CompressionType
) -> Iterable[bytes]:
    for sample in samples:
        yield compress(sample, compression_type)


def _encrypt_samples(
    samples: Iterable[bytes], cipher_type: CipherType, key_size_bits: int
) -> Iterable[bytes]:
    for sample in samples:
        yield _encrypt_sample(sample, cipher_type, key_size_bits)


def main(args: List[str]) -> int:
    """main returns exit code"""

    parser = _get_argparser()
    parsed_args = parser.parse_args(args)
    out_filename = parsed_args.output or _gen_out_filename()

    config = load_config()
    db_manager = pg.set_up_db(
        db_name=config["DB_NAME"], db_user=config["DB_USER"], db_pass=config["DB_PASS"]
    )
    set_up_logger(additional_handlers=DatabaseLogHandler(db_manager))

    # Some validation
    if parsed_args.cipher or parsed_args.key_size:
        if len(parsed_args.cipher) != len(parsed_args.key_size):
            eprint("Number of ciphers must equal number of key sizes")
            return 1

    if parsed_args.random_data:
        if not parsed_args.size_range:
            eprint("Size range is required when generating random data")
            return 1
        if not parsed_args.num_samples or parsed_args.num_samples < 1:
            eprint(
                "Number of samples (must be positive) is required when " "generating random data"
            )
            return 1

        print(f"Writing to file '{out_filename}'")
        with open(out_filename, "w") as handle:
            for data_type in parsed_args.random_data:
                for data in _gen_plaintext_samples(
                    parsed_args.num_samples,
                    parsed_args.size_range,
                    RandomDataType[data_type],
                ):
                    handle.write(data.hex())
                    handle.write("\n")
        print(f"Wrote data to file '{out_filename}'")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
