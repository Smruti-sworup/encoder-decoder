"""
modules/atbash.py
Implements Atbash (substitution) cipher.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class AtbashCipher(EncoderDecoder):
    """Atbash Cipher."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encrypts text using Atbash cipher."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            result = []
            for char in text:
                if char.isalpha():
                    if char.isupper():
                        result.append(chr(ord('Z') - (ord(char) - ord('A'))))
                    else:
                        result.append(chr(ord('z') - (ord(char) - ord('a'))))
                else:
                    result.append(char)
            return "".join(result)
        except Exception as e:
            raise EncodingError(f"Atbash encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decrypts Atbash cipher (identical to encoding)."""
        try:
            return self.encode(data, **kwargs)
        except Exception as e:
            raise DecodingError(f"Atbash decoding failed: {str(e)}")
