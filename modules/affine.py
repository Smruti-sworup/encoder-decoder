"""
modules/affine.py
Implements Affine cipher.
"""

import math
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class AffineCipher(EncoderDecoder):
    """Affine Cipher."""
    
    def _mod_inverse(self, a: int, m: int = 26) -> int:
        """Finds the modular multiplicative inverse of a modulo m."""
        for x in range(1, m):
            if ((a % m) * (x % m)) % m == 1:
                return x
        return -1
        
    def encode(self, data: Union[str, bytes], a: int = 5, b: int = 8, **kwargs: Any) -> str:
        """
        Encrypts text using Affine cipher: E(x) = (a*x + b) mod 26.
        a and 26 must be coprime.
        """
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if math.gcd(a, 26) != 1:
                raise ValueError(f"Key 'a' ({a}) and 26 must be coprime (share no common factors). Valid 'a' values: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25.")
                
            result = []
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    x = ord(char) - base
                    enc_val = (a * x + b) % 26
                    result.append(chr(base + enc_val))
                else:
                    result.append(char)
            return "".join(result)
        except Exception as e:
            raise EncodingError(f"Affine encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], a: int = 5, b: int = 8, **kwargs: Any) -> str:
        """
        Decrypts Affine cipher text: D(x) = a^-1 * (x - b) mod 26.
        """
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if math.gcd(a, 26) != 1:
                raise ValueError("Key 'a' and 26 must be coprime.")
                
            a_inv = self._mod_inverse(a, 26)
            if a_inv == -1:
                raise ValueError("Modular inverse of key 'a' could not be found.")
                
            result = []
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    y = ord(char) - base
                    dec_val = (a_inv * (y - b)) % 26
                    result.append(chr(base + dec_val))
                else:
                    result.append(char)
            return "".join(result)
        except Exception as e:
            raise DecodingError(f"Affine decryption failed: {str(e)}")
