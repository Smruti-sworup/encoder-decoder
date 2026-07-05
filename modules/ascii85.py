"""
modules/ascii85.py
Implements ASCII85 (Adobe/Git format) encoding and decoding.
"""

import base64
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class ASCII85Coder(EncoderDecoder):
    """ASCII85 (A85) Encoder and Decoder."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes string or bytes to ASCII85."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return base64.a85encode(data_bytes).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"ASCII85 encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes ASCII85 string to readable text."""
        try:
            if isinstance(data, str):
                clean_data = "".join(data.split())
            else:
                clean_data = "".join(data.decode('utf-8', errors='replace').split())
                
            decoded_bytes = base64.a85decode(clean_data.encode('utf-8'))
            return decoded_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"ASCII85 decoding failed: {str(e)}")
