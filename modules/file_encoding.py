"""
modules/file_encoding.py
Implements encoder/decoder utilities for entire files (Base64, Hex, Binary representation, Data URI).
"""

import base64
import os
import mimetypes
from typing import Tuple, Union

class FileEncoder:
    """File Encoder and Decoder."""
    
    def encode_file_to_base64(self, file_bytes: bytes) -> str:
        """Encodes raw file bytes to a Base64 string."""
        return base64.b64encode(file_bytes).decode('utf-8')
        
    def decode_base64_to_file(self, base64_str: str) -> bytes:
        """Decodes a Base64 string back to file bytes."""
        clean_str = "".join(base64_str.split())
        padding_needed = len(clean_str) % 4
        if padding_needed:
            clean_str += "=" * (4 - padding_needed)
        return base64.b64decode(clean_str.encode('utf-8'))
        
    def encode_file_to_hex(self, file_bytes: bytes) -> str:
        """Encodes file bytes to a Hexadecimal string."""
        return file_bytes.hex()
        
    def decode_hex_to_file(self, hex_str: str) -> bytes:
        """Decodes a Hexadecimal string to file bytes."""
        clean_str = "".join(c for c in hex_str if c in "0123456789abcdefABCDEF")
        if len(clean_str) % 2 != 0:
            clean_str = "0" + clean_str
        return bytes.fromhex(clean_str)
        
    def encode_file_to_binary(self, file_bytes: bytes) -> str:
        """Encodes file bytes to space-separated binary bits."""
        return " ".join(f"{b:08b}" for b in file_bytes)
        
    def decode_binary_to_file(self, binary_str: str) -> bytes:
        """Decodes a space-separated binary bit string to file bytes."""
        clean_str = "".join(c for c in binary_str if c in "01 ")
        blocks = clean_str.split()
        if len(blocks) == 1 and len(blocks[0]) > 8:
            single = blocks[0]
            blocks = [single[i:i+8] for i in range(0, len(single), 8)]
            
        byte_arr = bytearray()
        for block in blocks:
            if block:
                byte_arr.append(int(block, 2))
        return bytes(byte_arr)

    def encode_to_data_uri(self, file_bytes: bytes, filename: str) -> str:
        """
        Encodes file bytes into a browser-executable Data URI (e.g. data:image/png;base64,...).
        """
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            # Fallbacks based on common extensions if guessing failed
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.pdf':
                mime_type = 'application/pdf'
            elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
                mime_type = f'image/{ext[1:]}'
                if ext == '.jpg':
                    mime_type = 'image/jpeg'
            else:
                mime_type = 'application/octet-stream'
                
        base64_data = self.encode_file_to_base64(file_bytes)
        return f"data:{mime_type};base64,{base64_data}"
