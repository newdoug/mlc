"""Cipher types"""

from enum import auto

try:
    from ..utils.better_enum import BetterEnum
except (ImportError, ModuleNotFoundError):
    from utils.better_enum import BetterEnum


class CipherType(BetterEnum):
    """Type of cipher to use"""
    # TODO: finish implementing these and testing these
    # TODO: more modes for AES: CTR, OFB, CFB, CFB8, XTS, ECB, CBC, GCM
    # TODO: More asymmetric, more symmetric, more bit sizes, more modes
    #       Including less well-known ones. Don't have to be limited to just
    #       cryptography library.
    # Key sizes (bits): 128, 256
    AES = auto()
    # Key sizes supported: 32 to 448 bits in 8 bit increments
    BLOWFISH = auto()
    # Key sizes (bits): 128, 192, 256
    CAMELIA = auto()
    # Key sizes supported: 40 to 128 bits in 8 bit increments
    CAST5 = auto()
    # Always 256-bit key
    CHACHA20 = auto()
    # Always 256-bit key
    CHACHA20_POLY1305 = auto()
    # TODO: not implemented yet
    DES = auto()
    # Key is always 128 bits in length
    IDEA = auto()
    # TODO: not implemented yet
    RC2 = auto()
    # TODO: key sizes?
    RC4 = auto()
    # TODO: key sizes?
    RSA = auto()
    # Key is always 128 bits in length
    SEED = auto()
    SM4 = auto()
    # Key sizes (bits): 64, 128, 192
    TRIPLE_DES = auto()
