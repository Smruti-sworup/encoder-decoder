"""
modules/rot13.py
Implements ROT13 cipher.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class Rot13Cipher(EncoderDecoder):
    """ROT13 Cipher."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encrypts text using ROT13 cipher."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            result = []
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    new_char = chr((ord(char) - base + 13) % 26 + base)
                    result.append(new_char)
                else:
                    result.append(char)
            return "".join(result)
        except Exception as e:
            raise EncodingError(f"ROT13 encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decrypts ROT13 cipher text (which is identical to encoding)."""
        try:
            return self.encode(data, **kwargs)
        except Exception as e:
            raise DecodingError(f"ROT13 decoding failed: {str(e)}")
