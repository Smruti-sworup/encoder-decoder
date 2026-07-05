"""
modules/unicode.py
Implements Unicode escape representation conversions and raw UTF-8, UTF-16, UTF-32 converters.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class UnicodeCoder(EncoderDecoder):
    """Unicode format converter (supports raw encodings and code-point escapes)."""
    
    def encode(self, data: Union[str, bytes], format_type: str = "Escape Sequence", encoding: str = "utf-8", **kwargs: Any) -> str:
        """
        Encodes text to a Unicode format representation.
        
        Args:
            format_type (str): 'Escape Sequence' (\\uXXXX) or 'Code Points' (U+XXXX) or 'Hex Bytes'
            encoding (str): 'utf-8', 'utf-16', 'utf-32'
        """
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            if format_type == "Escape Sequence":
                return text.encode('unicode_escape').decode('ascii')
            elif format_type == "Code Points":
                return " ".join(f"U+{ord(c):04X}" for c in text)
            else:  # Hex Bytes of specific encoding
                encoded_bytes = text.encode(encoding)
                return " ".join(f"{b:02X}" for b in encoded_bytes)
        except Exception as e:
            raise EncodingError(f"Unicode encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], format_type: str = "Escape Sequence", encoding: str = "utf-8", **kwargs: Any) -> str:
        """Decodes Unicode formats back to text."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            if format_type == "Escape Sequence":
                # Convert literal escape codes like \u0048 to actual characters
                return data_str.encode('utf-8').decode('unicode_escape')
            elif format_type == "Code Points":
                # Parse U+XXXX
                tokens = data_str.replace("U+", "").replace("u+", "").split()
                chars = [chr(int(tok, 16)) for tok in tokens if tok]
                return "".join(chars)
            else:  # Hex Bytes of specific encoding
                clean_str = "".join(c for c in data_str if c in "0123456789abcdefABCDEF")
                byte_arr = bytes.fromhex(clean_str)
                return byte_arr.decode(encoding, errors='replace')
        except Exception as e:
            raise DecodingError(f"Unicode decoding failed: {str(e)}")
