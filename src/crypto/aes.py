
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .bse import Crypter


class AesCbcCrypt(Crypt):
    # TODO: docstrings
    def encrypt(self, data: bytes) -> bytes:
        # TODO: obviously doesn't work: get key + iv elsewhere
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()
