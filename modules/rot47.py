"""
modules/rot47.py
Implements ROT47 cipher.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class Rot47Cipher(EncoderDecoder):
    """ROT47 Cipher (covers printable ASCII chars)."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encrypts text using ROT47 cipher."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            result = []
            for char in text:
                val = ord(char)
                if 33 <= val <= 126:
                    result.append(chr(33 + ((val - 33 + 47) % 94)))
                else:
                    result.append(char)
            return "".join(result)
        except Exception as e:
            raise EncodingError(f"ROT47 encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decrypts ROT47 cipher (which is identical to encoding)."""
        try:
            return self.encode(data, **kwargs)
        except Exception as e:
            raise DecodingError(f"ROT47 decoding failed: {str(e)}")
