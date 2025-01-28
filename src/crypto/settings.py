"""Cipher settings"""

from base64 import b64decode, b64encode
from dataclasses import dataclass
from typing import Optional


def _b64_decode(value: Optional[str]) -> Optional[bytes]:
    return b64decode(value.encode("UTF-8")) if value else None


def _b64_encode(value: Optional[bytes]) -> Optional[str]:
    return b64encode(value).decode("UTF-8") if value else None


@dataclass
class CipherInputSettings:
    """Settings for a cipher. Some fields may or may not be present depending
    on the cipher (e.g., some ciphers don't use an IV or a nonce or have
    different modes, etc.).
    These are settings as they could be input by a user.
    """
    key_size_bits: int
    mode: Optional[str] = None

    @property
    def key_size_bytes(self) -> int:
        """Key size in bytes. Rounded down if not evenly divisible by 8"""
        return self.key_size_bits // 8

    @property
    def key_size_bytes_raw(self) -> float:
        """Key size in bytes as a float, unrounded"""
        return self.key_size_bits / 8

    def to_dict(self) -> dict:
        """Settings to JSON-serializable dict"""
        return {
            "key_size_bits": self.key_size_bits,
            "mode": self.mode,
        }

    @staticmethod
    def from_dict(settings_dict: dict):
        """From a dictionary, make and return a CipherInputSettings object"""
        return CipherInputSettings(
            key_size_bits=settings_dict["key_size_bits"],
            mode=settings_dict.get("mode"),
        )


@dataclass
class CipherOutputSettings:
    """Cipher output settings.
    Same as input settings plus any ephemeral information/settings like keys,
    IVs, nonces, etc.
    """
    key_size_bits: int
    mode: Optional[str] = None
    nonce: Optional[bytes] = None
    initialization_vector: Optional[bytes] = None

    @property
    def key_size_bytes(self) -> int:
        """Key size in bytes. Rounded down if not evenly divisible by 8"""
        return self.key_size_bits // 8

    @property
    def key_size_bytes_raw(self) -> float:
        """Key size in bytes as a float, unrounded"""
        return self.key_size_bits / 8

    @property
    def iv(self) -> Optional[bytes]:
        """Get initialization vector (IV)"""
        # pylint: disable=invalid-name
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

    def to_dict(self) -> dict:
        """Settings to JSON-serializable dict"""
        return {
            "key_size_bits": self.key_size_bits,
            "nonce": _b64_encode(self.nonce),
            "iv": _b64_encode(self.iv),
            "mode": self.mode,
        }

    @staticmethod
    def from_dict(settings_dict: dict):
        """From a dictionary, make and return a CipherOutputSettings object"""
        return CipherOutputSettings(
            key_size_bits=settings_dict["key_size_bits"],
            nonce=_b64_decode(settings_dict.get("nonce")),
            initialization_vector=_b64_decode(settings_dict.get("iv")),
            mode=settings_dict.get("mode"),
        )


if __name__ == "__main__":
    import os

    def _input_settings():
        print("Input settings test")
        dict1 = {
            "key_size_bits": 128,
            #"nonce": b64encode(os.urandom(16)).decode(),
            #"iv": b64encode(os.urandom(16)).decode(),
            "mode": "CBC",
        }
        print(f"orig dict: {dict1}")
        cls1 = CipherInputSettings.from_dict(dict1)
        cls2 = CipherInputSettings.from_dict(cls1.to_dict())
        print(f"Settings: {cls1}")
        print(f"to_dict: {cls1.to_dict()}")
        print(f"Settings again: {cls2}")
        print(f"Same class? {cls1 == cls2}")
        print(f"Same dicts? {dict1 == cls1.to_dict() == cls2.to_dict()}")

    def _output_settings():
        print("Output settings test")
        dict1 = {
            "key_size_bits": 128,
            "nonce": b64encode(os.urandom(16)).decode(),
            "iv": b64encode(os.urandom(16)).decode(),
            "mode": "CBC",
        }
        print(f"orig dict: {dict1}")
        cls1 = CipherOutputSettings.from_dict(dict1)
        cls2 = CipherOutputSettings.from_dict(cls1.to_dict())
        print(f"Settings: {cls1}")
        print(f"to_dict: {cls1.to_dict()}")
        print(f"Settings again: {cls2}")
        print(f"Same class? {cls1 == cls2}")
        print(f"Same dicts? {dict1 == cls1.to_dict() == cls2.to_dict()}")

    _input_settings()
    _output_settings()
