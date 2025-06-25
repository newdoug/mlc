from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

from mlc.crypto.metadata import CipherMetadata


def encrypt_chacha20(metadata: CipherMetadata, data: bytes) -> bytes:
    cipher = Cipher(algorithms.ChaCha20(metadata.key, metadata.nonce), mode=None)
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()


def decrypt_chacha20(metadata: CipherMetadata, data: bytes) -> bytes:
    cipher = Cipher(algorithms.ChaCha20(metadata.key, metadata.nonce), mode=None)
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()
