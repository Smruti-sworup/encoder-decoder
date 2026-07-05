"""
modules/zlib.py
Implements Zlib compression and decompression.
Outputs are base64 encoded for text compatibility.
"""

import zlib
import base64
from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class ZlibCoder(EncoderDecoder):
    """Zlib Compression and Decompression Coder."""
    
    def encode(self, data: Union[str, bytes], compression_level: int = 6, **kwargs: Any) -> str:
        """
        Compresses input data using Zlib.
        Returns base64 encoded string of compressed bytes.
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            compressed = zlib.compress(data_bytes, level=compression_level)
            return base64.b64encode(compressed).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"Zlib compression failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> str:
        """
        Decodes base64 encoded compressed data and decompresses using Zlib.
        """
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            clean_str = "".join(data_str.split())
            compressed_bytes = base64.b64decode(clean_str.encode('utf-8'))
            
            decompressed = zlib.decompress(compressed_bytes)
            return decompressed.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Zlib decompression failed: {str(e)}")
