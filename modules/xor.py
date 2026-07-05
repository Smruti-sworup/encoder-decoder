"""
modules/xor.py
Implements XOR (bitwise exclusive OR) cipher.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class XORCipher(EncoderDecoder):
    """XOR Cipher."""
    
    def encode(self, data: Union[str, bytes], key: str = "KEY", output_format: str = "Hex", **kwargs: Any) -> str:
        """
        Encrypts input data using XOR key.
        Returns a hex or raw string representing the output bytes.
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            if not key:
                raise ValueError("XOR key cannot be empty.")
                
            key_bytes = key.encode('utf-8')
            
            # XOR operations
            xored_bytes = bytes(data_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data_bytes)))
            
            if output_format == "Hex":
                return xored_bytes.hex()
            else:
                return xored_bytes.decode('latin-1')  # Decode as latin-1 to preserve exact bytes
        except Exception as e:
            raise EncodingError(f"XOR encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], key: str = "KEY", input_format: str = "Hex", **kwargs: Any) -> str:
        """Decrypts XOR encrypted input data."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            if not key:
                raise ValueError("XOR key cannot be empty.")
                
            key_bytes = key.encode('utf-8')
            
            if input_format == "Hex":
                # Strip spaces and prefixes
                clean_hex = "".join(c for c in data_str if c in "0123456789abcdefABCDEF")
                encrypted_bytes = bytes.fromhex(clean_hex)
            else:
                encrypted_bytes = data_str.encode('latin-1')
                
            # XOR decryption is identical to encryption
            decrypted_bytes = bytes(encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(encrypted_bytes)))
            return decrypted_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"XOR decryption failed: {str(e)}")
