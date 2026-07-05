"""
modules/base32.py
Implements Base32 encoding and decoding.
"""

import base64
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class Base32Coder(EncoderDecoder):
    """Base32 Encoder and Decoder."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes input data to Base32."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return base64.b32encode(data_bytes).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"Base32 encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes Base32 string to readable text."""
        try:
            if isinstance(data, str):
                clean_data = "".join(data.split())
            else:
                clean_data = "".join(data.decode('utf-8', errors='replace').split())
            
            # Ensure correct padding is added if missing
            padding_needed = len(clean_data) % 8
            if padding_needed:
                clean_data += "=" * (8 - padding_needed)
                
            decoded_bytes = base64.b32decode(clean_data.upper().encode('utf-8'))
            return decoded_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Base32 decoding failed: {str(e)}")
