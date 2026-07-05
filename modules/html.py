"""
modules/html.py
Implements HTML entities escaping and unescaping.
"""

import html
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class HTMLCoder(EncoderDecoder):
    """HTML entity escape and unescape coder."""
    
    def encode(self, data: Union[str, bytes], quote: bool = True, **kwargs: Any) -> str:
        """
        Escapes HTML special characters.
        
        Args:
            quote (bool): If True, escapes double quotes (") and single quotes (').
        """
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
            return html.escape(text, quote=quote)
        except Exception as e:
            raise EncodingError(f"HTML escaping failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """Unescapes HTML entities back to characters."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
            return html.unescape(text)
        except Exception as e:
            raise DecodingError(f"HTML unescaping failed: {str(e)}")
