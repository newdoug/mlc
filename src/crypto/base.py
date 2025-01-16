"""Base encryptor/decryptor class(es)"""
import abc
import os


class Crypter:
    """Base class for encryptor/decrytor objects"""
    def __init__(self, key_size_bits: int = 256):
        assert key_size_bits % 8 == 0
        self.key_size_bits = key_size_bits
        self.key_size_bytes = key_size_bits // 8

    def gen_key(self) -> bytes:
        """Generate random key for this cipher"""
        return os.urandom(self.key_size_bytes)

    @abc.abstractmethod
    def gen_iv(self) -> bytes:
        """Generate an IV (or nonce depending on cipher) usable by this cipher
        """
        raise NotImplementedError()

    @abc.abstractmethod
    # TODO: better interface: not all have IVs
    def encrypt(self, data: bytes, iv: bytes) -> bytes:
        """Encrypt data"""
        raise NotImplementedError()

    @abc.abstractmethod
    def decrypt(self, data: bytes, iv: bytes) -> bytes:
        """Decrypt data"""
        raise NotImplementedError()
