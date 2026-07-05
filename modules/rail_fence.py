"""
modules/rail_fence.py
Implements Rail Fence (zigzag) cipher.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class RailFenceCipher(EncoderDecoder):
    """Rail Fence Transposition Cipher."""
    
    def encode(self, data: Union[str, bytes], rails: int = 3, **kwargs: Any) -> str:
        """Encrypts text using Rail Fence cipher with specified rail count."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if rails <= 1:
                return text
                
            # Create fence structure
            fence = [[] for _ in range(rails)]
            rail = 0
            direction = 1
            
            for char in text:
                fence[rail].append(char)
                rail += direction
                # Reverse direction when hitting boundary rails
                if rail == rails - 1 or rail == 0:
                    direction = -direction
                    
            return "".join("".join(row) for row in fence)
        except Exception as e:
            raise EncodingError(f"Rail Fence encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], rails: int = 3, **kwargs: Any) -> str:
        """Decrypts Rail Fence cipher text."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if rails <= 1:
                return text
                
            # Reconstruct the zigzag pattern of index locations
            pattern = [[] for _ in range(rails)]
            rail = 0
            direction = 1
            
            for i in range(len(text)):
                pattern[rail].append(i)
                rail += direction
                if rail == rails - 1 or rail == 0:
                    direction = -direction
                    
            # Rebuild string by populating positions
            result = [None] * len(text)
            idx = 0
            for r in range(rails):
                for pos in pattern[r]:
                    result[pos] = text[idx]
                    idx += 1
                    
            return "".join(result)  # type: ignore
        except Exception as e:
            raise DecodingError(f"Rail Fence decryption failed: {str(e)}")
