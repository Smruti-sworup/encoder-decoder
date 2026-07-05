"""
modules/chacha20.py
Implements ChaCha20 symmetric stream cipher encryption/decryption using pycryptodome.
"""

import os
import base64
from typing import Union, Any, Tuple
from Crypto.Cipher import ChaCha20
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class ChaCha20Coder(EncoderDecoder):
    """ChaCha20 Stream Cipher Coder."""
    
    def _parse_key_nonce(self, key: str, nonce: str) -> Tuple[bytes, bytes]:
        """Validates key (32 bytes) and nonce (8 or 12 bytes)."""
        if len(key) == 64 and all(c in "0123456789abcdefABCDEF" for c in key):
            key_bytes = bytes.fromhex(key)
        else:
            key_bytes = key.encode('utf-8')
            
        if len(key_bytes) != 32:
            raise ValueError(f"ChaCha20 key size must be exactly 32 bytes (256 bits). Got {len(key_bytes)} bytes.")
            
        nonce_bytes = b""
        if nonce:
            if len(nonce) in [16, 24] and all(c in "0123456789abcdefABCDEF" for c in nonce):
                nonce_bytes = bytes.fromhex(nonce)
            else:
                nonce_bytes = nonce.encode('utf-8')
                
            if len(nonce_bytes) not in [8, 12]:
                raise ValueError(f"ChaCha20 nonce must be 8 or 12 bytes. Got {len(nonce_bytes)} bytes.")
        else:
            # Generate default 12-byte nonce
            nonce_bytes = os.urandom(12)
            
        return key_bytes, nonce_bytes

    def encode(self, data: Union[str, bytes], key: str = "", nonce: str = "", **kwargs: Any) -> str:
        """
        Encrypts input data using ChaCha20.
        Returns base64-encoded ciphertext (prefixed with the nonce).
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            key_bytes, nonce_bytes = self._parse_key_nonce(key, nonce)
            
            cipher = ChaCha20.new(key=key_bytes, nonce=nonce_bytes)
            ciphertext = cipher.encrypt(data_bytes)
            
            # Prepend the nonce to ciphertext
            combined = nonce_bytes + ciphertext
            return base64.b64encode(combined).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"ChaCha20 encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], key: str = "", nonce: str = "", **kwargs: Any) -> str:
        """Decrypts ChaCha20 base64-encoded ciphertext."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            ciphertext_bytes = base64.b64decode(data_str.encode('utf-8'))
            
            if len(key) == 64 and all(c in "0123456789abcdefABCDEF" for c in key):
                key_bytes = bytes.fromhex(key)
            else:
                key_bytes = key.encode('utf-8')
                
            if len(key_bytes) != 32:
                raise ValueError("ChaCha20 key must be exactly 32 bytes.")
                
            if not nonce:
                # Assume standard 12-byte nonce is prepended
                if len(ciphertext_bytes) < 12:
                    raise ValueError("Ciphertext too short to extract 12-byte nonce.")
                extracted_nonce = ciphertext_bytes[:12]
                actual_ciphertext = ciphertext_bytes[12:]
            else:
                _, extracted_nonce = self._parse_key_nonce(key, nonce)
                actual_ciphertext = ciphertext_bytes
                
            cipher = ChaCha20.new(key=key_bytes, nonce=extracted_nonce)
            decrypted = cipher.decrypt(actual_ciphertext)
            return decrypted.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"ChaCha20 decryption failed: {str(e)}")
