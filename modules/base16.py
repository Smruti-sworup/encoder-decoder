"""
modules/base16.py
Implements Base16 (Hexadecimal) encoding and decoding.
"""

import base64
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class Base16Coder(EncoderDecoder):
    """Base16 Encoder and Decoder."""
    
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Encodes bytes or string to Base16 (Hex)."""
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            return base64.b16encode(data_bytes).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"Base16 encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Decodes Base16 (Hex) to string."""
        try:
            if isinstance(data, str):
                clean_data = "".join(data.split())
            else:
                clean_data = "".join(data.decode('utf-8', errors='replace').split())
                
            # Hex decoding must be uppercase for standard b16decode
            decoded_bytes = base64.b16decode(clean_data.upper().encode('utf-8'))
            return decoded_bytes.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Base16 decoding failed. Ensure input is valid hex: {str(e)}")
