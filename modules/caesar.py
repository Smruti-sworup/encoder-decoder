"""
modules/caesar.py
Implements Caesar shift cipher.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class CaesarCipher(EncoderDecoder):
    """Caesar Cipher shift translator."""
    
    def encode(self, data: Union[str, bytes], shift: int = 3, **kwargs: Any) -> str:
        """Encrypts text using Caesar cipher with given shift key."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            shift = shift % 26
            result = []
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    new_char = chr((ord(char) - base + shift) % 26 + base)
                    result.append(new_char)
                else:
                    result.append(char)
            return "".join(result)
        except Exception as e:
            raise EncodingError(f"Caesar encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], shift: int = 3, **kwargs: Any) -> str:
        """Decrypts Caesar cipher text by shifting backwards."""
        try:
            return self.encode(data, shift=-shift, **kwargs)
        except Exception as e:
            raise DecodingError(f"Caesar decryption failed: {str(e)}")
