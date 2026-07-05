"""
tests/test_base64.py
Unit tests for base encoders/decoders (Base16, Base32, Base58, Base62, Base64, Base64URL).
"""

import sys
import unittest
from pathlib import Path

# Add project root to python path for test execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.base16 import Base16Coder
from modules.base32 import Base32Coder
from modules.base58 import Base58Coder
from modules.base62 import Base62Coder
from modules.base64 import Base64Coder
from modules.base64url import Base64UrlCoder

class TestBaseCoders(unittest.TestCase):
    def setUp(self):
        self.plain_text = "Hello, World! 🚀"
        self.b16 = Base16Coder()
        self.b32 = Base32Coder()
        self.b58 = Base58Coder()
        self.b62 = Base62Coder()
        self.b64 = Base64Coder()
        self.b64url = Base64UrlCoder()

    def test_base64_encode_decode(self):
        encoded = self.b64.encode(self.plain_text)
        decoded = self.b64.decode(encoded)
        self.assertEqual(decoded, self.plain_text)

    def test_base64url_encode_decode(self):
        encoded = self.b64url.encode(self.plain_text)
        self.assertNotIn("+", encoded)
        self.assertNotIn("/", encoded)
        decoded = self.b64url.decode(encoded)
        self.assertEqual(decoded, self.plain_text)

    def test_base16_encode_decode(self):
        encoded = self.b16.encode(self.plain_text)
        decoded = self.b16.decode(encoded)
        self.assertEqual(decoded, self.plain_text)

    def test_base32_encode_decode(self):
        encoded = self.b32.encode(self.plain_text)
        decoded = self.b32.decode(encoded)
        self.assertEqual(decoded, self.plain_text)

    def test_base58_encode_decode(self):
        encoded = self.b58.encode(self.plain_text)
        decoded = self.b58.decode(encoded)
        self.assertEqual(decoded, self.plain_text)
        
    def test_base62_encode_decode(self):
        encoded = self.b62.encode(self.plain_text)
        decoded = self.b62.decode(encoded)
        self.assertEqual(decoded, self.plain_text)

if __name__ == "__main__":
    unittest.main()
