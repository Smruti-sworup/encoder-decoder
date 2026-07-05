"""
modules/triple_des.py
Implements Triple DES (3DES) symmetric key encryption/decryption using pycryptodome.
"""

import os
import base64
from typing import Union, Any, Tuple
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class TripleDESCoder(EncoderDecoder):
    """Triple DES (3DES) Encryption and Decryption (supports CBC, ECB modes)."""
    
    def _parse_key_iv(self, key: str, iv: str, mode: str) -> Tuple[bytes, bytes]:
        """Validates and processes key and IV (key must be 16 or 24 bytes, IV 8 bytes)."""
        if len(key) in [32, 48] and all(c in "0123456789abcdefABCDEF" for c in key):
            key_bytes = bytes.fromhex(key)
        else:
            key_bytes = key.encode('utf-8')
            
        if len(key_bytes) not in [16, 24]:
            raise ValueError(f"Triple DES key size must be 16 or 24 bytes (128 or 192 bits). Got {len(key_bytes)} bytes.")
            
        # Adjust 16-byte key to 24-byte key (standard 3DES option 2) if needed
        key_bytes = DES3.adjust_key_parity(key_bytes)
            
        iv_bytes = b""
        if mode == "CBC":
            if iv:
                if len(iv) == 16 and all(c in "0123456789abcdefABCDEF" for c in iv):
                    iv_bytes = bytes.fromhex(iv)
                else:
                    iv_bytes = iv.encode('utf-8')
                    
                if len(iv_bytes) != 8:
                    raise ValueError(f"Triple DES IV must be exactly 8 bytes. Got {len(iv_bytes)} bytes.")
            else:
                iv_bytes = os.urandom(8)
                
        return key_bytes, iv_bytes

    def encode(self, data: Union[str, bytes], key: str = "", iv: str = "", mode: str = "CBC", **kwargs: Any) -> str:
        """
        Encrypts input data using Triple DES.
        Returns base64-encoded ciphertext (prefixed with IV if CBC).
        """
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            key_bytes, iv_bytes = self._parse_key_iv(key, iv, mode)
            
            if mode == "CBC":
                cipher = DES3.new(key_bytes, DES3.MODE_CBC, iv_bytes)
                padded_data = pad(data_bytes, DES3.block_size)
                ciphertext = cipher.encrypt(padded_data)
                combined = iv_bytes + ciphertext
            else:  # ECB
                cipher = DES3.new(key_bytes, DES3.MODE_ECB)
                padded_data = pad(data_bytes, DES3.block_size)
                combined = cipher.encrypt(padded_data)
                
            return base64.b64encode(combined).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"Triple DES Encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], key: str = "", iv: str = "", mode: str = "CBC", **kwargs: Any) -> str:
        """Decrypts Triple DES base64-encoded ciphertext."""
        try:
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            ciphertext_bytes = base64.b64decode(data_str.encode('utf-8'))
            
            if len(key) in [32, 48] and all(c in "0123456789abcdefABCDEF" for c in key):
                key_bytes = bytes.fromhex(key)
            else:
                key_bytes = key.encode('utf-8')
                
            if len(key_bytes) not in [16, 24]:
                raise ValueError("Triple DES key must be 16 or 24 bytes.")
                
            key_bytes = DES3.adjust_key_parity(key_bytes)
                
            if mode == "CBC":
                if not iv:
                    if len(ciphertext_bytes) < 8:
                        raise ValueError("Ciphertext too short for CBC decryption.")
                    extracted_iv = ciphertext_bytes[:8]
                    actual_ciphertext = ciphertext_bytes[8:]
                else:
                    _, extracted_iv = self._parse_key_iv(key, iv, mode)
                    actual_ciphertext = ciphertext_bytes
                    
                cipher = DES3.new(key_bytes, DES3.MODE_CBC, extracted_iv)
                decrypted_padded = cipher.decrypt(actual_ciphertext)
                decrypted = unpad(decrypted_padded, DES3.block_size)
            else:  # ECB
                cipher = DES3.new(key_bytes, DES3.MODE_ECB)
                decrypted_padded = cipher.decrypt(ciphertext_bytes)
                decrypted = unpad(decrypted_padded, DES3.block_size)
                
            return decrypted.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"Triple DES Decryption failed: {str(e)}")
