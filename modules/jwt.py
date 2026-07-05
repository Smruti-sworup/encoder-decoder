"""
modules/jwt.py
Provides decoding, signature verification, header/payload inspection, and expiration checks for JSON Web Tokens.
"""

import jwt
import time
import json
from typing import Dict, Any, Tuple, Optional
from datetime import datetime, UTC

class JWTTool:
    """JWT Token Parser and Verifier."""
    
    def decode_unverified(self, token: str) -> Tuple[bool, Dict[str, Any], Dict[str, Any], str]:
        """
        Decodes a JWT token without verifying the signature.
        Useful for inspecting token contents.
        
        Returns:
            Tuple: (success, header, payload, error_message)
        """
        try:
            token = token.strip()
            # Split JWT to check structure
            parts = token.split('.')
            if len(parts) != 3:
                return False, {}, {}, "Invalid JWT structure. Must have header, payload, and signature separated by dots."
                
            header = jwt.get_unverified_header(token)
            payload = jwt.decode(token, options={"verify_signature": False})
            return True, header, payload, ""
        except Exception as e:
            return False, {}, {}, f"Decoding failed: {str(e)}"
            
    def verify_token(self, token: str, key: str, algorithms: Optional[list[str]] = None) -> Tuple[bool, str]:
        """
        Verifies the signature and validity of the JWT token.
        
        Args:
            token (str): JWT string.
            key (str): Symmetric secret key or Asymmetric PEM public key.
            algorithms (list): Algorithms to allow (e.g. ['HS256', 'RS256']).
            
        Returns:
            Tuple[bool, str]: (is_valid, validation_message)
        """
        try:
            if not key:
                return False, "Secret/Public Key is required for signature verification."
                
            if not algorithms:
                # Dynamically inspect header to find algorithm
                header = jwt.get_unverified_header(token)
                alg = header.get("alg", "HS256")
                algorithms = [alg]
                
            # Verify and decode
            jwt.decode(token, key, algorithms=algorithms)
            return True, "Signature verified. Token is valid."
        except jwt.ExpiredSignatureError:
            return False, "Token signature is valid but has expired."
        except jwt.InvalidSignatureError:
            return False, "Invalid signature. The token has been tampered with or key is incorrect."
        except jwt.InvalidKeyError as e:
            return False, f"Invalid key format: {str(e)}"
        except Exception as e:
            return False, f"Verification failed: {str(e)}"
            
    def check_expiration(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes the 'exp' field in the JWT payload.
        
        Returns:
            Dict: Analysis including expiration time, active status, and time remaining.
        """
        analysis = {
            "has_exp": "exp" in payload,
            "expired": False,
            "exp_date": None,
            "time_remaining": "N/A"
        }
        
        if "exp" in payload:
            exp_val = payload["exp"]
            try:
                exp_dt = datetime.fromtimestamp(exp_val, tz=UTC)
                analysis["exp_date"] = exp_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                
                now = datetime.now(UTC)
                if exp_dt < now:
                    analysis["expired"] = True
                    analysis["time_remaining"] = "Expired"
                else:
                    diff = exp_dt - now
                    # Format remaining time
                    hours, remainder = divmod(int(diff.total_seconds()), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    analysis["time_remaining"] = f"{hours}h {minutes}m {seconds}s"
            except Exception as e:
                analysis["time_remaining"] = f"Parse Error: {str(e)}"
                
        return analysis
