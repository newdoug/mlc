from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

from mlc.crypto.metadata import CipherMetadata


def encrypt_aes(metadata: CipherMetadata, data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(metadata.key), metadata.mode_str_to_mode()(metadata.iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(cipher.algorithm.block_size).padder()
    return encryptor.update(padder.update(data) + padder.finalize()) + encryptor.finalize()


def decrypt_aes(metadata: CipherMetadata, data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(metadata.key), metadata.mode_str_to_mode()(metadata.iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()
    unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()
    return unpadder.update(plaintext) + unpadder.finalize()
