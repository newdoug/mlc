"""Tracks the possible metadata associated with a cipher operation.
TODO: tracking the metadata is something we want, but writing these wrapper functions with it feels a little
unnecessarily complex.
TODO: implement more ciphers. DES, TRIPLE_DES, SM4, whatever else python-cryptography and others support.
"""

from typing import Optional

from cryptography.hazmat.primitives.ciphers import modes

from mlc.utils.base_model import BaseModel


class CipherMetadata(BaseModel):
    name: str
    num_bits: int
    key: bytes
    iv: Optional[bytes] = None
    nonce: Optional[bytes] = None
    mode: Optional[str] = None

    def mode_str_to_mode(self) -> modes.Mode:
        """Convert this object's mode string to mode type from the crypto library.
        This list matches the modes from the crypto library.
        """
        if self.mode == "CBC":
            return modes.CBC
        if self.mode == "CFB":
            return modes.CFB
        if self.mode == "CFB8":
            return modes.CFB8
        if self.mode == "CTR":
            return modes.CTR
        if self.mode == "ECB":
            return modes.ECB
        if self.mode == "GCM":
            return modes.GCM
        if self.mode == "OFB":
            return modes.OFB
        if self.mode == "XTS":
            return modes.XTS
        raise ValueError(f"No mode '{self.mode}' is known")
