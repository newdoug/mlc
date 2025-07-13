import os
import random

from mlc.crypto.camellia import decrypt_camellia, encrypt_camellia
from mlc.crypto.metadata import CipherMetadata

# TODO: test and support CTR and XTS modes


def _run_encrypt_decrypt_test(
    encrypt_func,
    decrypt_func,
    len_min: int = 4,
    len_max: int = 16 * 1024,
    num_bits: int = 256,
    iters: int = 100,
    mode: str = None,
    iv_num_bytes: int = 16,
) -> None:
    assert num_bits % 8 == 0
    for _ in range(iters):
        metadata = CipherMetadata(
            name="Camellia",
            num_bits=num_bits,
            key=os.urandom(num_bits // 8),
            iv=os.urandom(iv_num_bytes),
            mode=mode,
        )
        data_size = random.randint(len_min, len_max)
        data = os.urandom(data_size)
        ciphertext = encrypt_func(metadata, data)
        plaintext = decrypt_func(metadata, ciphertext)
        assert data == plaintext


def test_camellia_cbc_encrypt_decrypt():
    _run_encrypt_decrypt_test(encrypt_camellia, decrypt_camellia, num_bits=256, mode="CBC")


def test_camellia_cfb_encrypt_decrypt():
    _run_encrypt_decrypt_test(encrypt_camellia, decrypt_camellia, num_bits=256, mode="CFB")


def test_camellia_ofb_encrypt_decrypt():
    _run_encrypt_decrypt_test(encrypt_camellia, decrypt_camellia, num_bits=256, mode="OFB")
