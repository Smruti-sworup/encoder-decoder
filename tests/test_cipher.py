"""
tests/test_cipher.py
Unit tests for classical and modern ciphers (Caesar, Vigenere, Atbash, Rail Fence, Bacon, Affine, XOR, AES).
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.caesar import CaesarCipher
from modules.vigenere import VigenereCipher
from modules.atbash import AtbashCipher
from modules.rail_fence import RailFenceCipher
from modules.bacon import BaconCipher
from modules.affine import AffineCipher
from modules.xor import XORCipher
from modules.aes import AESCoder

class TestCipherSuite(unittest.TestCase):
    def setUp(self):
        self.plain_text = "The Quick Brown Fox Jumps Over 13 Lazy Dogs!"
        
    def test_caesar_cipher(self):
        coder = CaesarCipher()
        enc = coder.encode(self.plain_text, shift=5)
        dec = coder.decode(enc, shift=5)
        self.assertEqual(dec, self.plain_text)

    def test_vigenere_cipher(self):
        coder = VigenereCipher()
        enc = coder.encode(self.plain_text, key="SECRETKEY")
        dec = coder.decode(enc, key="SECRETKEY")
        self.assertEqual(dec, self.plain_text)

    def test_atbash_cipher(self):
        coder = AtbashCipher()
        enc = coder.encode(self.plain_text)
        dec = coder.decode(enc)
        self.assertEqual(dec, self.plain_text)

    def test_rail_fence_cipher(self):
        coder = RailFenceCipher()
        enc = coder.encode(self.plain_text, rails=4)
        dec = coder.decode(enc, rails=4)
        self.assertEqual(dec, self.plain_text)

    def test_bacon_cipher(self):
        coder = BaconCipher()
        text = "HELLOWORLD"
        enc = coder.encode(text)
        dec = coder.decode(enc)
        self.assertEqual(dec, text)

    def test_affine_cipher(self):
        coder = AffineCipher()
        enc = coder.encode(self.plain_text, a=5, b=8)
        dec = coder.decode(enc, a=5, b=8)
        self.assertEqual(dec, self.plain_text)

    def test_xor_cipher(self):
        coder = XORCipher()
        enc = coder.encode(self.plain_text, key="SECURE_XOR_KEY", output_format="Hex")
        dec = coder.decode(enc, key="SECURE_XOR_KEY", input_format="Hex")
        self.assertEqual(dec, self.plain_text)

    def test_aes_cipher(self):
        coder = AESCoder()
        key = "this_is_a_very_secure_aes_key_32"  # 32 bytes
        iv = "random_iv_16_chr"                # 16 bytes
        enc = coder.encode(self.plain_text, key=key, iv=iv, mode="CBC")
        dec = coder.decode(enc, key=key, mode="CBC")
        self.assertEqual(dec, self.plain_text)

if __name__ == "__main__":
    unittest.main()
