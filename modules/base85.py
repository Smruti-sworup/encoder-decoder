"""
modules/base85.py
Implements Base85 encoding and decoding.
"""

import base64
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class Base85Coder(EncoderDecoder):
    """Base85 Encoder and Decoder (RFC 1924 variant)."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes string or bytes to Base85."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return base64.b85encode(data_bytes).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"Base85 encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes Base85 string to readable text."""
        try:
            if isinstance(data, str):
                clean_data = "".join(data.split())
            else:
                clean_data = "".join(data.decode('utf-8', errors='replace').split())
                
            decoded_bytes = base64.b85decode(clean_data.encode('utf-8'))
            return decoded_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Base85 decoding failed: {str(e)}")
