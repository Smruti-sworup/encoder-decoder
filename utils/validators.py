"""
utils/validators.py
Provides parsing validation and type checking functions to prevent exceptions.
"""

import re
import base64
from typing import Tuple, Any

def is_hex(data: str) -> bool:
    """Checks if a string is a valid hexadecimal sequence."""
    clean_data = "".join(data.split())
    if not clean_data:
        return False
    return bool(re.match(r"^[0-9a-fA-F]+$", clean_data))

def is_binary(data: str) -> bool:
    """Checks if a string consists only of 0s, 1s, and whitespace."""
    clean_data = "".join(data.split())
    if not clean_data:
        return False
    return bool(re.match(r"^[01]+$", clean_data))

def is_octal(data: str) -> bool:
    """Checks if a string consists only of octal digits (0-7) and whitespace."""
    clean_data = "".join(data.split())
    if not clean_data:
        return False
    return bool(re.match(r"^[0-7]+$", clean_data))

def is_decimal(data: str) -> bool:
    """Checks if a string consists only of decimal digits and whitespace."""
    clean_data = "".join(data.split())
    if not clean_data:
        return False
    return bool(re.match(r"^[0-9]+$", clean_data))

def is_base64(data: str) -> bool:
    """Checks if a string is valid Base64 encoded data."""
    clean_data = "".join(data.split())
    if not clean_data:
        return False
    # Length of base64 should be a multiple of 4 (if padded)
    if len(clean_data) % 4 != 0:
        # Check if we can pad and decode
        clean_data += "=" * (4 - len(clean_data) % 4)
    try:
        # Check matching characters
        if not re.match(r"^[A-Za-z0-9+/=]+$", clean_data):
            return False
        base64.b64decode(clean_data, validate=True)
        return True
    except Exception:
        return False

def validate_aes_key(key: str, key_format: str) -> Tuple[bool, str]:
    """
    Validates key size and format for AES encryption.
    AES keys must be 16, 24, or 32 bytes.
    """
    if not key:
        return False, "Key cannot be empty."
    
    try:
        if key_format == "Hex":
            if not is_hex(key):
                return False, "Key must be a valid hexadecimal string."
            key_bytes = bytes.fromhex(key)
        else:  # Text/UTF-8
            key_bytes = key.encode("utf-8")
            
        if len(key_bytes) not in [16, 24, 32]:
            return False, f"AES key size must be 16, 24, or 32 bytes. Got {len(key_bytes)} bytes."
        return True, ""
    except Exception as e:
        return False, f"Invalid key: {str(e)}"
