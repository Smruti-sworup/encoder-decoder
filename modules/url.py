"""
modules/url.py
Implements URL percent-encoding and decoding.
"""

import urllib.parse
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class URLCoder(EncoderDecoder):
    """URL (Percent-encoding) Encoder and Decoder."""
    
    def encode(self, data: Union[str, bytes], encode_plus: bool = False, **kwargs: Any) -> str:
        """
        URL encodes string.
        
        Args:
            encode_plus (bool): If True, replaces spaces with '+' instead of '%20'.
        """
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if encode_plus:
                return urllib.parse.quote_plus(text)
            return urllib.parse.quote(text)
        except Exception as e:
            raise EncodingError(f"URL encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], decode_plus: bool = False, **kwargs: Any) -> str:
        """URL decodes string."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if decode_plus:
                return urllib.parse.unquote_plus(text)
            return urllib.parse.unquote(text)
        except Exception as e:
            raise DecodingError(f"URL decoding failed: {str(e)}")
