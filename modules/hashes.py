"""
modules/hashes.py
Implements various hashing algorithms (MD5, SHA-1, SHA-2, SHA-3, BLAKE2, BLAKE3, RIPEMD160) for text and files.
"""

import hashlib
from typing import Union, Dict, Any, List

# Try importing blake3 package, else provide standard fallback
try:
    import blake3
    BLAKE3_AVAILABLE = True
except ImportError:
    BLAKE3_AVAILABLE = False

class HashCoder:
    """Hasher for text and binary inputs."""
    
    SUPPORTED_ALGORITHMS = [
        "MD5", "SHA-1", "SHA-224", "SHA-256", "SHA-384", "SHA-512",
        "SHA3-224", "SHA3-256", "SHA3-384", "SHA3-512",
        "BLAKE2b", "BLAKE2s", "BLAKE3", "RIPEMD-160"
    ]
    
    def hash_text(self, text: str, algorithm: str) -> str:
        """Hashes a text string and returns the hex digest."""
        try:
            data_bytes = text.encode('utf-8')
            return self.hash_bytes(data_bytes, algorithm)
        except Exception as e:
            return f"Error hashing text: {str(e)}"
            
    def hash_bytes(self, data: bytes, algorithm: str) -> str:
        """Hashes binary bytes and returns the hex digest."""
        algo = algorithm.upper().replace(" ", "")
        
        # BLAKE3 custom handling
        if algo == "BLAKE3":
            if BLAKE3_AVAILABLE:
                try:
                    return blake3.blake3(data).hexdigest()
                except Exception as e:
                    return f"BLAKE3 error: {str(e)}"
            else:
                # Fallback to BLAKE2b if package not installed
                algo = "BLAKE2B"
                
        # RIPEMD-160 custom handling
        if algo == "RIPEMD-160" or algo == "RIPEMD160":
            try:
                h = hashlib.new('ripemd160')
                h.update(data)
                return h.hexdigest()
            except ValueError:
                # Fallback if RIPEMD-160 is not supported in the local OpenSSL compilation
                return "RIPEMD-160 not supported by local OpenSSL assembly. Please use SHA-256."

        # Map to standard hashlib names
        hash_mapping = {
            "MD5": hashlib.md5,
            "SHA-1": hashlib.sha1,
            "SHA1": hashlib.sha1,
            "SHA-224": hashlib.sha224,
            "SHA224": hashlib.sha224,
            "SHA-256": hashlib.sha256,
            "SHA256": hashlib.sha256,
            "SHA-384": hashlib.sha384,
            "SHA384": hashlib.sha384,
            "SHA-512": hashlib.sha512,
            "SHA512": hashlib.sha512,
            "SHA3-224": hashlib.sha3_224,
            "SHA3-256": hashlib.sha3_256,
            "SHA3-384": hashlib.sha3_384,
            "SHA3-512": hashlib.sha3_512,
            "BLAKE2B": hashlib.blake2b,
            "BLAKE2S": hashlib.blake2s,
        }
        
        if algo in hash_mapping:
            h = hash_mapping[algo]()
            h.update(data)
            return h.hexdigest()
        else:
            raise ValueError(f"Unsupported hashing algorithm: {algorithm}")

    def hash_file(self, file_path: str, algorithm: str) -> str:
        """Reads a file in chunks to hash it without loading large files into memory."""
        algo = algorithm.upper().replace(" ", "")
        
        # Initialize hash objects
        if algo == "BLAKE3" and BLAKE3_AVAILABLE:
            h = blake3.blake3()
        elif algo == "RIPEMD-160" or algo == "RIPEMD160":
            try:
                h = hashlib.new('ripemd160')
            except ValueError:
                return "RIPEMD-160 not supported by local OpenSSL assembly."
        else:
            # Map standard
            hash_mapping = {
                "MD5": hashlib.md5,
                "SHA-1": hashlib.sha1,
                "SHA-224": hashlib.sha224,
                "SHA-256": hashlib.sha256,
                "SHA-384": hashlib.sha384,
                "SHA-512": hashlib.sha512,
                "SHA3-224": hashlib.sha3_224,
                "SHA3-256": hashlib.sha3_256,
                "SHA3-384": hashlib.sha3_384,
                "SHA3-512": hashlib.sha3_512,
                "BLAKE2B": hashlib.blake2b,
                "BLAKE2S": hashlib.blake2s,
                "BLAKE3": hashlib.blake2b, # Fallback
            }
            if algo not in hash_mapping:
                raise ValueError(f"Unsupported hash algorithm: {algorithm}")
            h = hash_mapping[algo]()

        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            return h.hexdigest()
        except Exception as e:
            return f"Error reading file for hashing: {str(e)}"
