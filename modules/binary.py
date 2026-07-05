"""
modules/binary.py
Implements Binary string conversions (Text <-> binary representation of bytes)
and number-base conversions (Binary <-> Decimal, Hex <-> Binary).
"""

import re
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class BinaryCoder(EncoderDecoder):
    """Binary representation and number base converter."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes text or bytes to space-separated binary digits."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return " ".join(f"{b:08b}" for b in data_bytes)
        except Exception as e:
            raise EncodingError(f"Binary encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes space-separated binary digits back to text."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            # Clean non-binary and whitespace
            clean_str = "".join(c for c in data_str if c in "01 ")
            binary_blocks = clean_str.split()
            
            # If they didn't use spaces, split every 8 characters
            if len(binary_blocks) == 1 and len(binary_blocks[0]) > 8:
                single_str = binary_blocks[0]
                binary_blocks = [single_str[i:i+8] for i in range(0, len(single_str), 8)]
                
            byte_arr = bytearray()
            for block in binary_blocks:
                if block:
                    byte_arr.append(int(block, 2))
                    
            return byte_arr.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Binary decoding failed: {str(e)}")

    def binary_to_decimal(self, bin_str: str) -> str:
        """Converts space-separated binary bytes into space-separated decimal values."""
        try:
            clean_bin = "".join(c for c in bin_str if c in "01 ")
            blocks = clean_bin.split()
            return " ".join(str(int(b, 2)) for b in blocks if b)
        except Exception as e:
            raise ValueError(f"Binary to Decimal conversion failed: {str(e)}")

    def decimal_to_binary(self, dec_str: str) -> str:
        """Converts space-separated decimal values into space-separated binary bytes."""
        try:
            clean_dec = "".join(c for c in dec_str if c in "0123456789 ")
            blocks = clean_dec.split()
            return " ".join(f"{int(d):08b}" for d in blocks if d)
        except Exception as e:
            raise ValueError(f"Decimal to Binary conversion failed: {str(e)}")

    def hex_to_binary(self, hex_str: str) -> str:
        """Converts formatted or raw hex string into space-separated binary bytes."""
        try:
            clean_hex = re.sub(r'0x|\\x|0X|\\X|[\s,;:]', '', hex_str)
            if not clean_hex:
                return ""
            if len(clean_hex) % 2 != 0:
                clean_hex = "0" + clean_hex
            byte_arr = bytes.fromhex(clean_hex)
            return " ".join(f"{b:08b}" for b in byte_arr)
        except Exception as e:
            raise ValueError(f"Hex to Binary conversion failed: {str(e)}")

    def binary_to_hex(self, bin_str: str) -> str:
        """Converts space-separated binary bytes into hex string."""
        try:
            clean_bin = "".join(c for c in bin_str if c in "01 ")
            blocks = clean_bin.split()
            return "".join(f"{int(b, 2):02x}" for b in blocks if b)
        except Exception as e:
            raise ValueError(f"Binary to Hex conversion failed: {str(e)}")

