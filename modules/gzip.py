"""
modules/gzip.py
Implements Gzip compression and decompression.
Outputs are base64 encoded for text compatibility.
"""

import gzip
import base64
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class GzipCoder(EncoderDecoder):
    """Gzip Compression and Decompression Coder."""
    
    def encode(self, data: Union[str, bytes], compression_level: int = 9, **kwargs: Any) -> str:
        """
        Compresses input data using Gzip.
        Returns base64 encoded string of compressed bytes.
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            compressed = gzip.compress(data_bytes, compresslevel=compression_level)
            return base64.b64encode(compressed).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"Gzip compression failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """
        Decodes base64 encoded compressed data and decompresses using Gzip.
        """
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            # Clean up whitespace
            clean_str = "".join(data_str.split())
            compressed_bytes = base64.b64decode(clean_str.encode('utf-8'))
            
            decompressed = gzip.decompress(compressed_bytes)
            return decompressed.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Gzip decompression failed. Ensure input is valid base64-encoded gzip: {str(e)}")
