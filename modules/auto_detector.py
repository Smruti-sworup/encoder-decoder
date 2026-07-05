"""
modules/auto_detector.py
Provides format detection of unknown text inputs using heuristics and structural validation.
"""

import re
from typing import List, Dict, Any
from utils.validators import is_hex, is_binary, is_octal, is_decimal, is_base64
from modules.base58 import Base58Coder
from modules.base62 import Base62Coder

class AutoDetector:
    """Detects the input format using heuristic rules and validation checks."""
    
    def detect(self, text: str) -> List[Dict[str, Any]]:
        """
        Analyzes the text and returns a list of formats with confidence scores,
        sorted from highest to lowest confidence.
        """
        text = text.strip()
        if not text:
            return [{"format": "Empty Input", "confidence": 1.0, "description": "No characters detected."}]
            
        results = []
        
        # 1. JWT Detector
        jwt_pattern = r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*$"
        if re.match(jwt_pattern, text):
            results.append({
                "format": "JSON Web Token (JWT)",
                "confidence": 0.98,
                "description": "Matches triple-part dot separated JSON Web Token pattern."
            })
            
        # 2. Morse Code Detector
        # Morse only contains dots, dashes, slashes, and spaces
        morse_chars = set(text)
        if morse_chars.issubset({'.', '-', '/', ' '}) and any(c in morse_chars for c in ['.', '-']):
            results.append({
                "format": "Morse Code",
                "confidence": 0.95,
                "description": "Contains only dot, dash, slash, and space markers."
            })
            
        # 3. Binary Representation
        if is_binary(text):
            results.append({
                "format": "Binary Representation",
                "confidence": 0.95,
                "description": "Contains only 1s, 0s, and separating whitespace."
            })
            
        # 4. Hexadecimal
        # Clean potential formatting characters to test structure
        clean_hex = re.sub(r'0x|\\x|0X|\\X|[\s,;:]', '', text)
        if clean_hex and all(c in "0123456789abcdefABCDEF" for c in clean_hex):
            confidence = 0.70
            if " " in text or ":" in text or "0x" in text or "\\x" in text:
                confidence = 0.95  # highly likely formatted hex
            elif len(text) >= 16:
                confidence = 0.85
            results.append({
                "format": "Hexadecimal",
                "confidence": confidence,
                "description": "Contains characters matching hexadecimal bases (0-9, A-F)."
            })
            
        # 5. Octal Representation
        if is_octal(text) and " " in text:
            results.append({
                "format": "Octal Representation",
                "confidence": 0.88,
                "description": "Space-separated digits between 0 and 7."
            })
            
        # 6. Decimal Representation
        if is_decimal(text) and " " in text:
            # Check if all numbers fit inside byte values [0, 255]
            parts = text.split()
            if all(parts[i].isdigit() and 0 <= int(parts[i]) <= 255 for i in range(min(5, len(parts)))):
                results.append({
                    "format": "Decimal Byte Representation",
                    "confidence": 0.90,
                    "description": "Space-separated numbers corresponding to ASCII/UTF-8 bytes."
                })
                
        # 7. URL Percent Encoding
        if "%" in text and re.search(r"%[0-9a-fA-F]{2}", text):
            results.append({
                "format": "URL Percent Encoding",
                "confidence": 0.95,
                "description": "Contains percent escape sequences typical of web URIs."
            })
            
        # 8. HTML Entity Encoding
        if "&" in text and (re.search(r"&[a-zA-Z0-9]+;", text) or re.search(r"&#[0-9]+;", text)):
            results.append({
                "format": "HTML Entity Encoding",
                "confidence": 0.95,
                "description": "Contains HTML glyph references starting with '&' and ending with ';'."
            })
            
        # 9. Base64 Encoding
        if is_base64(text):
            confidence = 0.65
            if text.endswith("="):
                confidence = 0.88  # Padding is a strong heuristic
            results.append({
                "format": "Base64",
                "confidence": confidence,
                "description": "Valid Base64 structure with optional padding."
            })
            
        # 10. Base32 Encoding
        clean_b32 = "".join(text.split())
        if all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=" for c in clean_b32.upper()):
            confidence = 0.55
            if clean_b32.endswith("="):
                confidence = 0.85
            results.append({
                "format": "Base32",
                "confidence": confidence,
                "description": "Contains uppercase letters and digits 2-7, typical of Base32."
            })
            
        # 11. Base58 Encoding
        b58 = Base58Coder()
        try:
            # Check if we can decode without errors
            b58.decode(text)
            results.append({
                "format": "Base58",
                "confidence": 0.50,
                "description": "Contains alphanumeric characters matching Bitcoin Base58 alphabet."
            })
        except Exception:
            pass
            
        # 12. Plain Text / Generic UTF-8 (Fallback)
        results.append({
            "format": "Plain Text (UTF-8)",
            "confidence": 0.40,
            "description": "Standard unencoded character set representation."
        })
        
        # Sort results based on confidence level desc
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results
