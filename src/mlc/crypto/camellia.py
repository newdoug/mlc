from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

from mlc.crypto.metadata import CipherMetadata


def encrypt_camellia(metadata: CipherMetadata, data: bytes) -> bytes:
    cipher = Cipher(algorithms.Camellia(metadata.key), metadata.mode_str_to_mode()(metadata.iv))
    encryptor = cipher.encryptor()
    if metadata.mode.lower() == "cbc":
        padder = padding.PKCS7(cipher.algorithm.block_size).padder()
        data = padder.update(data) + padder.finalize()
    return encryptor.update(data) + encryptor.finalize()


def decrypt_camellia(metadata: CipherMetadata, data: bytes) -> bytes:
    cipher = Cipher(algorithms.Camellia(metadata.key), metadata.mode_str_to_mode()(metadata.iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()
    if metadata.mode.lower() == "cbc":
        unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()
        plaintext = unpadder.update(plaintext) + unpadder.finalize()
    return plaintext
