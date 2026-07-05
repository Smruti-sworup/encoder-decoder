"""
modules/bacon.py
Implements Bacon's cipher (Baconian translation).
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError
from utils.constants import BACON_DICT_26, REVERSE_BACON_DICT_26

class BaconCipher(EncoderDecoder):
    """Baconian Cipher."""
    
    def encode(self, data: Union[str, bytes], char_a: str = "a", char_b: str = "b", **kwargs: Any) -> str:
        """
        Encrypts text to Baconian format.
        
        Args:
            char_a (str): Symbol representing 'a' (default 'a', sometimes '0').
            char_b (str): Symbol representing 'b' (default 'b', sometimes '1').
        """
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            text = text.upper()
            result = []
            for char in text:
                if char in BACON_DICT_26:
                    val = BACON_DICT_26[char]
                    # Map 'a' and 'b' to user custom representation
                    mapped_val = val.replace('a', char_a).replace('b', char_b)
                    result.append(mapped_val)
                else:
                    # Preserve spaces and non-alpha characters
                    result.append(char)
            return " ".join(result)
        except Exception as e:
            raise EncodingError(f"Bacon encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], char_a: str = "a", char_b: str = "b", **kwargs: Any) -> str:
        """Decrypts Baconian format text back to standard text."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            # Standardize custom 'a' and 'b' symbols back to literal 'a' and 'b'
            standardized = text.lower().replace(char_a.lower(), 'a').replace(char_b.lower(), 'b')
            
            # Extract 5-letter blocks
            result = []
            words = standardized.split("  ")  # preserved space
            for word in words:
                decoded_word = []
                # Clean up spaces inside blocks
                tokens = [t for t in word.split() if len(t) == 5]
                for tok in tokens:
                    if tok in REVERSE_BACON_DICT_26:
                        decoded_word.append(REVERSE_BACON_DICT_26[tok])
                    else:
                        decoded_word.append("?")
                result.append("".join(decoded_word))
                
            return " ".join(result)
        except Exception as e:
            raise DecodingError(f"Bacon decoding failed: {str(e)}")
