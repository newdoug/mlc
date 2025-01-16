"""Cipher types"""
from ..utils import BetterEnum


class CipherType(BetterEnum):
    """Type of cipher to use"""
    # TODO: finish implementing these and testing these
    # TODO: more modes for AES: CTR, OFB, CFB, CFB8, XTS, ECB
    AESCBC128 = "AESCBC128"
    AESCBC256 = "AESCBC256"
    AESGCM128 = "AESGCM128"
    AESGCM256 = "AESGCM256"
    # TODO: more key sizes supported 32 to 448 bits in 8 bit increments
    BLOWFISH = "BLOWFISH"
    CAMELIA128 = "CAMELLIA128"
    CAMELIA192 = "CAMELLIA192"
    CAMELIA256 = "CAMELLIA256"
    # TODO: more key sizes supported 40 to 128 bits in 8 bit increments
    CAST5 = "CAST5"
    # Always 256-bit key
    CHACHA20 = "CHACHA20"
    # Always 256-bit key
    CHACHA20_POLY1305 = "CHACHA20_POLY1305"
    DES = "DES"
    # Key is always 128 bits in length
    IDEA = "IDEA"
    RC2 = "RC2"
    # TODO: other key sizes
    RC4 = "RC4"
    # Key is always 128 bits in length
    SEED = "SEED"
    SM4 = "SM4"
    TRIPLE_DES64 = "TRIPLE_DES64"
    TRIPLE_DES128 = "TRIPLE_DES128"
    TRIPLE_DES192 = "TRIPLE_DES192"
