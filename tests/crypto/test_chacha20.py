import os
import random

from mlc.crypto.chacha20 import decrypt_chacha20, encrypt_chacha20
from mlc.crypto.metadata import CipherMetadata


def _run_encrypt_decrypt_test(
    encrypt_func,
    decrypt_func,
    len_min: int = 4,
    len_max: int = 16 * 1024,
    num_bits: int = 256,
    iters: int = 100,
    mode: str = None,
    nonce_num_bytes: int = 16,
) -> None:
    assert num_bits % 8 == 0
    for _ in range(iters):
        metadata = CipherMetadata(
            name="ChaCha20",
            num_bits=num_bits,
            key=os.urandom(num_bits // 8),
            nonce=os.urandom(nonce_num_bytes),
            mode=mode,
        )
        data_size = random.randint(len_min, len_max)
        data = os.urandom(data_size)
        ciphertext = encrypt_func(metadata, data)
        plaintext = decrypt_func(metadata, ciphertext)
        assert data == plaintext


def test_chacha20_encrypt_decrypt():
    _run_encrypt_decrypt_test(encrypt_chacha20, decrypt_chacha20, num_bits=256)
