"""
modules/hexadecimal.py
Implements Hexadecimal conversions (Text <-> formatted hex bytes).
"""

import re
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class HexadecimalCoder(EncoderDecoder):
    """Hexadecimal representation converter with formatting options."""
    
    def encode(self, data: Union[str, bytes], delimiter: str = " ", prefix: str = "", **kwargs: Any) -> str:
        """
        Encodes text or bytes to formatted hex representation.
        
        Args:
            delimiter (str): Separator between hex values (e.g., ' ', ',', or '').
            prefix (str): Prefix before each byte (e.g., '0x', '\\x').
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            hex_list = [f"{prefix}{b:02x}" for b in data_bytes]
            return delimiter.join(hex_list)
        except Exception as e:
            raise EncodingError(f"Hexadecimal encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """
        Decodes formatted hex string back to text.
        Automatically handles spaces, commas, 0x, \\x prefixes.
        """
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            # Strip standard prefixes like 0x or \x and separators
            clean_str = re.sub(r'0x|\\x|0X|\\X|[\s,;:]', '', data_str)
            
            if not clean_str:
                return ""
                
            if len(clean_str) % 2 != 0:
                raise ValueError("Hex string length must be an even number.")
                
            byte_arr = bytes.fromhex(clean_str)
            return byte_arr.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Hexadecimal decoding failed: {str(e)}")
