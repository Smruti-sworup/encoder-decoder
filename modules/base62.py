"""
modules/base62.py
Implements Base62 encoding and decoding algorithms without external libraries.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class Base62Coder(EncoderDecoder):
    """Base62 Encoder and Decoder (Standard Alphanumeric Alphabet)."""
    
    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes string or bytes to Base62."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            if not data_bytes:
                return ""
                
            # Count leading zero bytes
            zero_count = 0
            for b in data_bytes:
                if b == 0:
                    zero_count += 1
                else:
                    break
                    
            # Convert bytes to integer (big-endian)
            num = int.from_bytes(data_bytes, byteorder='big')
            
            result = []
            while num > 0:
                num, remainder = divmod(num, 62)
                result.append(self.ALPHABET[remainder])
                
            # Prepend '0' for each leading zero byte
            prefix = self.ALPHABET[0] * zero_count
            return prefix + "".join(reversed(result))
        except Exception as e:
            raise EncodingError(f"Base62 encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes Base62 string to readable text."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            # Clean up whitespace
            data_str = "".join(data_str.split())
            if not data_str:
                return ""
                
            # Verify alphabet
            for char in data_str:
                if char not in self.ALPHABET:
                    raise ValueError(f"Invalid character '{char}' in Base62 input.")
                    
            # Count leading '0' characters
            zero_count = 0
            for char in data_str:
                if char == self.ALPHABET[0]:
                    zero_count += 1
                else:
                    break
                    
            # Convert base62 to big integer
            num = 0
            for char in data_str:
                num = num * 62 + self.ALPHABET.index(char)
                
            if num == 0:
                num_bytes = b''
            else:
                # Calculate byte length
                byte_length = (num.bit_length() + 7) // 8
                num_bytes = num.to_bytes(byte_length, byteorder='big')
                
            decoded_bytes = (b'\x00' * zero_count) + num_bytes
            return decoded_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Base62 decoding failed: {str(e)}")
