"""
tests/test_hash.py
Unit tests for hashing algorithms inside modules/hashes.py.
"""

import sys
import unittest
import tempfile
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.hashes import HashCoder

class TestHashCoder(unittest.TestCase):
    def setUp(self):
        self.hasher = HashCoder()
        self.sample_text = "test_string_for_hashing_validation"
        
    def test_md5_hash(self):
        digest = self.hasher.hash_text(self.sample_text, "MD5")
        # Known MD5 checksum for this string
        expected = "68472ce2b29ec412b15314a095fa4322"
        self.assertEqual(digest, expected)

    def test_sha256_hash(self):
        digest = self.hasher.hash_text(self.sample_text, "SHA-256")
        expected = "687247d16061d5d80a4fb9c837a3012dfffc3f715f2b88b01a53d2bcccdcb487"
        self.assertEqual(digest, expected)

    def test_file_hashing(self):
        # Create temp file with contents
        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f:
            f.write(self.sample_text)
            temp_path = f.name
            
        try:
            digest = self.hasher.hash_file(temp_path, "SHA-256")
            expected = "687247d16061d5d80a4fb9c837a3012dfffc3f715f2b88b01a53d2bcccdcb487"
            self.assertEqual(digest, expected)
        finally:
            os.unlink(temp_path)

if __name__ == "__main__":
    unittest.main()
