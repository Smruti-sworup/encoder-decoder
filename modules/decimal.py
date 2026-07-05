"""
modules/decimal.py
Implements Decimal conversions (Text <-> decimal representation of bytes).
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class DecimalCoder(EncoderDecoder):
    """Decimal representation converter."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes text or bytes to space-separated decimal values."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return " ".join(str(b) for b in data_bytes)
        except Exception as e:
            raise EncodingError(f"Decimal encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes space-separated decimal digits back to text."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            clean_str = "".join(c for c in data_str if c in "0123456789 ")
            decimal_blocks = clean_str.split()
            
            byte_arr = bytearray()
            for block in decimal_blocks:
                if block:
                    val = int(block)
                    if 0 <= val <= 255:
                        byte_arr.append(val)
                    else:
                        raise ValueError(f"Value {val} is out of byte range [0, 255].")
                    
            return byte_arr.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Decimal decoding failed: {str(e)}")
