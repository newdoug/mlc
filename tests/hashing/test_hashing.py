"""`hashing` module hashing file tests"""
import os
from typing import Union
import unittest

from mlc.hashing.hashing import hash_data, HashType as HT


class TestHashData(unittest.TestCase):
    """Tests for the `hash_data` function"""

    def _sim_test(self, hash_type: HT, data: bytes,
                  expected: Union[bytes, str]) -> None:
        """Simple common hash test"""
        if isinstance(expected, bytes):
            expected = expected.hex().lower()
        got = hash_data(data, hash_type).hex().lower()
        self.assertEqual(got, expected)

    def _comp_test(self, hash_type: HT, hash_len: int,
                   num_iters: int = 100) -> None:
        """Complex common hash test"""
        for i in range(num_iters):
            # Either 1 or 2 byte length
            len_len = os.urandom(1)[0] % 2 + 1
            # length can be between 1 and 65536 bytes
            length = int.from_bytes(os.urandom(len_len), byteorder="little")
            # Just in case we unluckily got 0
            length += 1
            data = os.urandom(length)
            with self.subTest(i=i, len_len=len_len, length=length,
                              num_iters=num_iters, hash_type=hash_type,
                              hash_len=hash_len):
                got = hash_data(data, hash_type)
                self.assertIsInstance(got, bytes)
                self.assertEqual(len(got), hash_len)

    def test_md5_basic(self):
        """Basic MD5 test"""
        self._sim_test(HT.MD5, b"\x00"* 3, "693e9af84d3dfcc71e640e005bdc5e2e")

    def test_md5_random(self):
        """MD5 test on more random samples"""
        self._comp_test(HT.MD5, 16)

    def test_sha1_basic(self):
        """Basic SHA1 test"""
        self._sim_test(HT.SHA1, b"\x00"* 3,
                       "29e2dcfbb16f63bb0254df7585a15bb6fb5e927d")

    def test_sha1_random(self):
        """SHA1 test on more random samples"""
        self._comp_test(HT.SHA1, 20)

    def test_sha224_basic(self):
        """Basic SHA224 test"""
        self._sim_test(HT.SHA224, b"\x00"* 3,
                       ("8e25d811cf8fb0998f130c33062a4162edcf418a621ab0"
                        "4145489337"))

    def test_sha224_random(self):
        """SHA224 test on more random samples"""
        self._comp_test(HT.SHA224, 224 // 8)

    def test_sha3_224_basic(self):
        """Basic SHA3_224 test"""
        self._sim_test(HT.SHA3_224, b"\x00"* 3,
                       ("eb3043283ebd5b64c6aedeca57ccc52bd6c51d2c780f30"
                        "63314a2c6a"))

    def test_sha3_224_random(self):
        """SHA3_224 test on more random samples"""
        self._comp_test(HT.SHA3_224, 224 // 8)

    def test_sha256_basic(self):
        """Basic SHA256 test"""
        self._sim_test(HT.SHA256, b"\x00"* 3,
                       ("709e80c88487a2411e1ee4dfb9f22a861492d20c4765150"
                        "c0c794abd70f8147c"))

    def test_sha256_random(self):
        """SHA256 test on more random samples"""
        self._comp_test(HT.SHA256, 256 // 8)

    def test_sha3_256_basic(self):
        """Basic SHA3_256 test"""
        self._sim_test(HT.SHA3_256, b"\x00"* 3,
                       ("4f808a691382f10c81d6bbad4a2016bf155f36623197b97"
                        "e3bb47afec194cead"))

    def test_sha3_256_random(self):
        """SHA3_256 test on more random samples"""
        self._comp_test(HT.SHA3_256, 256 // 8)

    def test_sha384_basic(self):
        """Basic SHA384 test"""
        self._sim_test(HT.SHA384, b"\x00"* 3,
                       ("cd6bd1dcfebeffe9bb9ee705724f0312b5972417bc69473b"
                        "520598d6d3ab910cebbdff8bdcc9cfbbe6ae543d2657b2ab"))

    def test_sha384_random(self):
        """SHA384 test on more random samples"""
        self._comp_test(HT.SHA384, 384 // 8)

    def test_sha3_384_basic(self):
        """Basic SHA3_384 test"""
        self._sim_test(HT.SHA3_384, b"\x00"* 3,
                       ("8c7438752fa76780ebc786098c5346b6494c9078fedf2344"
                        "b7bf077a61134ff7af7dc36a17b2ca6df9ef7e6b22182881"))

    def test_sha3_384_random(self):
        """SHA3_384 test on more random samples"""
        self._comp_test(HT.SHA3_384, 384 // 8)

    def test_sha512_basic(self):
        """Basic SHA512 test"""
        self._sim_test(HT.SHA512, b"\x00"* 3,
                       ("6d518f8b31d1882feace10a9215f5d8cf5afe037652a1d11d"
                        "9c1408d988c2a4f71a5edfc85d0712fa3f4e21b2c0a244c8c"
                        "0d333bab454311e24067d2a83e5e59"))

    def test_sha512_random(self):
        """SHA512 test on more random samples"""
        self._comp_test(HT.SHA512, 512 // 8)

    def test_sha3_512_basic(self):
        """Basic SHA3_512 test"""
        self._sim_test(HT.SHA3_512, b"\x00"* 3,
                       ("0a7b1406be477b9b994a976a49a236ddf177ea65d04e77026"
                        "4b32c240eb229603f05b573772d406fbb321b8a80f90e73a8"
                        "eac5182e2dacb1e93b37c9ae380c37"))

    def test_sha3_512_random(self):
        """SHA3_512 test on more random samples"""
        self._comp_test(HT.SHA3_512, 512 // 8)

    def test_md2_basic(self):
        """Basic MD2 test"""
        self._sim_test(HT.MD2, b"The quick brown fox jumps over the lazy dog",
                       "03d85a0d629d2c442e987525319fc471")

    def test_md2_random(self):
        """MD2 test on more random samples"""
        self._comp_test(HT.MD2, 16)

    def test_md4_basic(self):
        """Basic MD4 test"""
        self._sim_test(HT.MD4, b"The quick brown fox jumps over the lazy dog",
                       "1bee69a46ba811185c194762abaeae90")

    def test_md4_random(self):
        """MD4 test on more random samples"""
        self._comp_test(HT.MD4, 16)
