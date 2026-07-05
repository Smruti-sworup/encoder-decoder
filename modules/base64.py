"""
modules/base64.py
Implements Base64 encoding and decoding.
"""

import base64
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class Base64Coder(EncoderDecoder):
    """Base64 Encoder and Decoder."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes string or bytes to Base64."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return base64.b64encode(data_bytes).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"Base64 encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes Base64 string to readable text."""
        try:
            if isinstance(data, str):
                clean_data = "".join(data.split())
            else:
                clean_data = "".join(data.decode('utf-8', errors='replace').split())
                
            # Ensure correct padding is added if missing
            padding_needed = len(clean_data) % 4
            if padding_needed:
                clean_data += "=" * (4 - padding_needed)
                
            decoded_bytes = base64.b64decode(clean_data.encode('utf-8'), validate=True)
            return decoded_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Base64 decoding failed. Ensure correct characters and padding: {str(e)}")
