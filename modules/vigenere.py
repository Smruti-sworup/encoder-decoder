"""
modules/vigenere.py
Implements Vigenere cipher.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class VigenereCipher(EncoderDecoder):
    """Vigenere Cipher."""
    
    def encode(self, data: Union[str, bytes], key: str = "KEY", **kwargs: Any) -> str:
        """Encrypts text using Vigenere cipher with given keyword key."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if not key or not key.isalpha():
                raise ValueError("Key must be a non-empty alphabetic string.")
                
            key = key.upper()
            result = []
            key_index = 0
            
            for char in text:
                if char.isalpha():
                    # Calculate shift from key character
                    shift = ord(key[key_index % len(key)]) - ord('A')
                    
                    base = ord('A') if char.isupper() else ord('a')
                    new_char = chr((ord(char) - base + shift) % 26 + base)
                    result.append(new_char)
                    key_index += 1
                else:
                    result.append(char)
            return "".join(result)
        except Exception as e:
            raise EncodingError(f"Vigenere encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], key: str = "KEY", **kwargs: Any) -> str:
        """Decrypts Vigenere cipher text by shifting backwards."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if not key or not key.isalpha():
                raise ValueError("Key must be a non-empty alphabetic string.")
                
            key = key.upper()
            result = []
            key_index = 0
            
            for char in text:
                if char.isalpha():
                    # Calculate negative shift from key character
                    shift = ord(key[key_index % len(key)]) - ord('A')
                    
                    base = ord('A') if char.isupper() else ord('a')
                    new_char = chr((ord(char) - base - shift) % 26 + base)
                    result.append(new_char)
                    key_index += 1
                else:
                    result.append(char)
            return "".join(result)
        except Exception as e:
            raise DecodingError(f"Vigenere decryption failed: {str(e)}")
