"""Cipher settings"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CipherSettings:
    """Settings for a cipher. Some fields may or may not be present depending
    on the cipher (e.g., some ciphers don't use an IV or a nonce or have
    different modes, etc.).
    """
    key_size_bits: int
    nonce: Optional[bytes] = None
    initialization_vector: Optional[bytes] = None
    mode: Optional[str] = None

    @property
    def iv(self) -> Optional[bytes]:
        """Get initialization vector (IV)"""
        return self.initialization_vector

    @property
    def nonce_hex(self) -> Optional[str]:
        """Return nonce as hex string or None if None"""
        return self.nonce.hex() if self.nonce is not None else None

    @property
    def iv_hex(self) -> Optional[str]:
        """Return IV as hex string or None if None"""
        return self.iv.hex() if self.iv is not None else None

    @property
    def initialization_vector_hex(self) -> Optional[str]:
        """Return initialization vector (IV) as hex string or None if None"""
        return self.iv_hex

    @property
    def key_size_bytes(self) -> int:
        """Key size in bytes. Rounded down if not evenly divisible by 8"""
        return self.key_size_bits // 8

    @property
    def key_size_bytes_raw(self) -> float:
        """Key size in bytes as a float, unrounded"""
        return self.key_size_bits / 8

