"""
modules/ascii.py
Implements ASCII sanitization and ordinal conversion.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class ASCCIICoder(EncoderDecoder):
    """ASCII sanitization and ordinal converter."""
    
    def encode(self, data: Union[str, bytes], mode: str = "ordinals", **kwargs: Any) -> str:
        """
        Encodes text to ASCII.
        
        Args:
            mode (str): Either 'ordinals' (space-separated ASCII numbers) or 'sanitize' (strips non-ascii).
        """
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if mode == "ordinals":
                return " ".join(str(ord(c)) for c in text if ord(c) < 128)
            else:  # sanitize
                return text.encode('ascii', errors='ignore').decode('ascii')
        except Exception as e:
            raise EncodingError(f"ASCII conversion failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], mode: str = "ordinals", **kwargs: Any) -> str:
        """Decodes ordinal ASCII values back to characters or decodes ASCII bytes."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('ascii', errors='replace')
            else:
                data_str = data
                
            if mode == "ordinals":
                clean_str = "".join(c for c in data_str if c in "0123456789 ")
                tokens = clean_str.split()
                chars = []
                for t in tokens:
                    val = int(t)
                    if 0 <= val < 128:
                        chars.append(chr(val))
                    else:
                        raise ValueError(f"Value {val} is not a valid 7-bit ASCII code.")
                return "".join(chars)
            else:
                # Sanitize mode decode is just returning the string
                return data_str
        except Exception as e:
            raise DecodingError(f"ASCII decoding failed: {str(e)}")
