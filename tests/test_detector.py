"""
tests/test_detector.py
Unit tests for modules/auto_detector.py.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.auto_detector import AutoDetector

class TestAutoDetector(unittest.TestCase):
    def setUp(self):
        self.detector = AutoDetector()
        
    def test_jwt_detection(self):
        # A mock JWT token structure
        jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        results = self.detector.detect(jwt_token)
        self.assertEqual(results[0]["format"], "JSON Web Token (JWT)")
        self.assertGreater(results[0]["confidence"], 0.90)

    def test_morse_detection(self):
        morse_text = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        results = self.detector.detect(morse_text)
        self.assertEqual(results[0]["format"], "Morse Code")
        self.assertGreater(results[0]["confidence"], 0.90)

    def test_binary_detection(self):
        bin_text = "01001000 01100101 01101100 01101100 01101111"
        results = self.detector.detect(bin_text)
        self.assertEqual(results[0]["format"], "Binary Representation")
        self.assertGreater(results[0]["confidence"], 0.90)

    def test_hex_detection(self):
        hex_text = "0x48 0x65 0x6c 0x6c 0x6f"
        results = self.detector.detect(hex_text)
        self.assertEqual(results[0]["format"], "Hexadecimal")
        self.assertGreater(results[0]["confidence"], 0.90)

if __name__ == "__main__":
    unittest.main()

