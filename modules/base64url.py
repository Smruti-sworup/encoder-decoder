"""
modules/base64url.py
Implements Base64 URL Safe encoding and decoding.
"""

import base64
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class Base64UrlCoder(EncoderDecoder):
    """Base64 URL Safe Encoder and Decoder."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes string or bytes to URL Safe Base64."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return base64.urlsafe_b64encode(data_bytes).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"Base64 URL encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes URL Safe Base64 string to readable text."""
        try:
            if isinstance(data, str):
                clean_data = "".join(data.split())
            else:
                clean_data = "".join(data.decode('utf-8', errors='replace').split())
                
            # Ensure correct padding is added if missing
            padding_needed = len(clean_data) % 4
            if padding_needed:
                clean_data += "=" * (4 - padding_needed)
                
            decoded_bytes = base64.urlsafe_b64decode(clean_data.encode('utf-8'))
            return decoded_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Base64 URL decoding failed: {str(e)}")
