"""
modules/rsa.py
Implements RSA asymmetric key generation, encryption, and decryption using pycryptodome.
"""

import base64
from typing import Union, Any, Tuple
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from modules.utilities import EncoderDecoder, EncodingError, DecodingError

class RSACoder(EncoderDecoder):
    """RSA Asymmetric Cryptosystem Coder."""
    
    def generate_keypair(self, bits: int = 2048) -> Tuple[str, str]:
        """
        Generates a new RSA keypair.
        
        Returns:
            Tuple[str, str]: (private_key_pem, public_key_pem)
        """
        try:
            key = RSA.generate(bits)
            private_key = key.export_key().decode('utf-8')
            public_key = key.publickey().export_key().decode('utf-8')
            return private_key, public_key
        except Exception as e:
            raise RuntimeError(f"RSA key generation failed: {str(e)}")

    def encode(self, data: Union[str, bytes], public_key_pem: str = "", **kwargs: Any) -> str:
        """
        Encrypts data using the RSA public key.
        Returns a base64 encoded string.
        """
        try:
            if not public_key_pem:
                raise ValueError("Public key PEM is required for encryption.")
                
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
                
            recipient_key = RSA.import_key(public_key_pem.strip())
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            
            ciphertext = cipher_rsa.encrypt(data_bytes)
            return base64.b64encode(ciphertext).decode('utf-8')
        except Exception as e:
            raise EncodingError(f"RSA encryption failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], private_key_pem: str = "", **kwargs: Any) -> str:
        """
        Decrypts data using the RSA private key.
        """
        try:
            if not private_key_pem:
                raise ValueError("Private key PEM is required for decryption.")
                
            if isinstance(data, bytes):
                data_str = data.decode('utf-8', errors='replace')
            else:
                data_str = data
                
            ciphertext_bytes = base64.b64decode(data_str.encode('utf-8'))
            
            private_key = RSA.import_key(private_key_pem.strip())
            cipher_rsa = PKCS1_OAEP.new(private_key)
            
            decrypted = cipher_rsa.decrypt(ciphertext_bytes)
            return decrypted.decode('utf-8', errors='replace')
        except Exception as e:
            raise DecodingError(f"RSA decryption failed: {str(e)}")
