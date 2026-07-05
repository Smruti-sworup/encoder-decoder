"""
modules/punycode.py
Implements Punycode (RFC 3492) encoding and decoding for internationalized domain names.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class PunycodeCoder(EncoderDecoder):
    """Punycode and IDNA domain name coder."""
    
    def encode(self, data: Union[str, bytes], mode: str = "Punycode (Raw)", **kwargs: Any) -> str:
        """
        Encodes text to Punycode or IDNA format.
        
        Args:
            mode (str): 'Punycode (Raw)' (e.g. mnchen-3ya) or 'IDNA (Domain)' (e.g. xn--mnchen-3ya)
        """
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if not text:
                return ""
                
            if mode == "IDNA (Domain)":
                return text.encode('idna').decode('ascii')
            else:  # Raw punycode
                return text.encode('punycode').decode('ascii')
        except Exception as e:
            raise EncodingError(f"Punycode encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], mode: str = "Punycode (Raw)", **kwargs: Any) -> str:
        """Decodes Punycode/IDNA string back to text."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            data_str = "".join(data_str.split())
            if not data_str:
                return ""
                
            if mode == "IDNA (Domain)" or data_str.lower().startswith("xn--"):
                return data_str.encode('ascii').decode('idna')
            else:  # Raw punycode
                return data_str.encode('ascii').decode('punycode')
        except Exception as e:
            raise DecodingError(f"Punycode decoding failed: {str(e)}")
