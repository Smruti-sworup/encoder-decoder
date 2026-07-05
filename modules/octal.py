"""
modules/octal.py
Implements Octal conversions (Text <-> octal representation of bytes).
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class OctalCoder(EncoderDecoder):
    """Octal representation converter."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes text or bytes to space-separated octal digits."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return " ".join(f"{b:03o}" for b in data_bytes)
        except Exception as e:
            raise EncodingError(f"Octal encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes space-separated octal digits back to text."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            clean_str = "".join(c for c in data_str if c in "01234567 ")
            octal_blocks = clean_str.split()
            
            # If no spaces and length is a multiple of 3, split by 3
            if len(octal_blocks) == 1 and len(octal_blocks[0]) > 3 and len(octal_blocks[0]) % 3 == 0:
                single_str = octal_blocks[0]
                octal_blocks = [single_str[i:i+3] for i in range(0, len(single_str), 3)]
                
            byte_arr = bytearray()
            for block in octal_blocks:
                if block:
                    byte_arr.append(int(block, 8))
                    
            return byte_arr.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Octal decoding failed: {str(e)}")
