"""
modules/aes.py
Implements AES symmetric key encryption and decryption using pycryptodome.
"""

import os
import base64
from typing import Union, Any, Tuple
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class AESCoder(EncoderDecoder):
    """AES Encryption and Decryption (supports CBC, CTR, ECB modes)."""
    
    def _parse_key_iv(self, key: str, iv: str, mode: str) -> Tuple[bytes, bytes]:
        """Validates and processes key and IV from strings to bytes."""
        # Detect if key is hex or raw text
        if len(key) in [32, 48, 64] and all(c in "0123456789abcdefABCDEF" for c in key):
            key_bytes = bytes.fromhex(key)
        else:
            key_bytes = key.encode('utf-8')
            
        if len(key_bytes) not in [16, 24, 32]:
            raise ValueError(f"AES key size must be 128, 192, or 256 bits (16, 24, or 32 bytes). Got {len(key_bytes)} bytes.")
            
        iv_bytes = b""
        if mode in ["CBC", "CTR"]:
            if iv:
                if len(iv) == 32 and all(c in "0123456789abcdefABCDEF" for c in iv):
                    iv_bytes = bytes.fromhex(iv)
                else:
                    iv_bytes = iv.encode('utf-8')
                    
                if len(iv_bytes) != 16:
                    raise ValueError(f"AES IV must be 128 bits (16 bytes). Got {len(iv_bytes)} bytes.")
            else:
                # Generate random IV if empty
                iv_bytes = os.urandom(16)
                
        return key_bytes, iv_bytes

    def encode(self, data: Union[str, bytes], key: str = "", iv: str = "", mode: str = "CBC", **kwargs: Any) -> str:
        """
        Encrypts input data using AES.
        Returns base64-encoded ciphertext (prefixed with IV if CBC/CTR).
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            key_bytes, iv_bytes = self._parse_key_iv(key, iv, mode)
            
            if mode == "CBC":
                cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
                padded_data = pad(data_bytes, AES.block_size)
                ciphertext = cipher.encrypt(padded_data)
                # Prepended IV is returned with ciphertext for easy decryption
                combined = iv_bytes + ciphertext
            elif mode == "CTR":
                # Using iv_bytes as initial value for counter
                cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=iv_bytes[:8])
                ciphertext = cipher.encrypt(data_bytes)
                combined = iv_bytes[:8] + ciphertext
            else:  # ECB (no IV)
                cipher = AES.new(key_bytes, AES.MODE_ECB)
                padded_data = pad(data_bytes, AES.block_size)
                combined = cipher.encrypt(padded_data)
                
            return base64.b64encode(combined).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"AES Encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], key: str = "", iv: str = "", mode: str = "CBC", **kwargs: Any) -> str:
        """Decrypts AES base64-encoded ciphertext."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            ciphertext_bytes = base64.b64decode(data_str.encode('utf-8'))
            
            # Detect key and verify
            if len(key) in [32, 48, 64] and all(c in "0123456789abcdefABCDEF" for c in key):
                key_bytes = bytes.fromhex(key)
            else:
                key_bytes = key.encode('utf-8')
                
            if len(key_bytes) not in [16, 24, 32]:
                raise ValueError("AES key must be 16, 24, or 32 bytes.")
                
            if mode == "CBC":
                # Extract IV from prepended data if not explicitly provided
                if not iv:
                    if len(ciphertext_bytes) < 16:
                        raise ValueError("Ciphertext is too short for CBC decryption.")
                    extracted_iv = ciphertext_bytes[:16]
                    actual_ciphertext = ciphertext_bytes[16:]
                else:
                    _, extracted_iv = self._parse_key_iv(key, iv, mode)
                    actual_ciphertext = ciphertext_bytes
                    
                cipher = AES.new(key_bytes, AES.MODE_CBC, extracted_iv)
                decrypted_padded = cipher.decrypt(actual_ciphertext)
                decrypted = unpad(decrypted_padded, AES.block_size)
            elif mode == "CTR":
                if not iv:
                    if len(ciphertext_bytes) < 8:
                        raise ValueError("Ciphertext is too short for CTR decryption.")
                    nonce = ciphertext_bytes[:8]
                    actual_ciphertext = ciphertext_bytes[8:]
                else:
                    nonce = iv.encode('utf-8')[:8]
                    actual_ciphertext = ciphertext_bytes
                    
                cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=nonce)
                decrypted = cipher.decrypt(actual_ciphertext)
            else:  # ECB
                cipher = AES.new(key_bytes, AES.MODE_ECB)
                decrypted_padded = cipher.decrypt(ciphertext_bytes)
                decrypted = unpad(decrypted_padded, AES.block_size)
                
            return decrypted.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"AES Decryption failed: {str(e)}")
