
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .crypter import Crypter
from .settings import CipherInputSettings


class AesCbcCrypt(Crypter):
    def encrypt(self, data: bytes, settings: CipherSettings) -> bytes:
        """Encrypt data"""
        # TODO: still need to handle padding
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    def decrypt(self, data: bytes, settings: CipherSettings) -> bytes:
        """Decrypt using AES in CBC mode"""
