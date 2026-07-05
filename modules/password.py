"""
modules/password.py
Implements cryptographically secure password generation and entropy/strength analysis.
"""

import math
import secrets
import string
from typing import Tuple, Dict, Any

class PasswordGenerator:
    """Secure password generator and strength analyzer."""
    
    def generate(self, length: int = 16, use_lower: bool = True, use_upper: bool = True, use_digits: bool = True, use_special: bool = True, custom_special: str = "") -> str:
        """
        Generates a cryptographically secure random password based on criteria.
        """
        pool = ""
        if use_lower:
            pool += string.ascii_lowercase
        if use_upper:
            pool += string.ascii_uppercase
        if use_digits:
            pool += string.digits
        if use_special:
            pool += custom_special if custom_special else "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        if not pool:
            raise ValueError("At least one character set must be selected.")
            
        # Ensure we have at least one character from each selected set
        password_chars = []
        if use_lower:
            password_chars.append(secrets.choice(string.ascii_lowercase))
        if use_upper:
            password_chars.append(secrets.choice(string.ascii_uppercase))
        if use_digits:
            password_chars.append(secrets.choice(string.digits))
        if use_special:
            password_chars.append(secrets.choice(custom_special if custom_special else "!@#$%^&*()_+-=[]{}|;:,.<>?"))
            
        # Fill the rest
        remaining = length - len(password_chars)
        if remaining > 0:
            password_chars.extend(secrets.choice(pool) for _ in range(remaining))
            
        # Shuffle the list to avoid predictable placements of guaranteed chars
        secrets.SystemRandom().shuffle(password_chars)
        return "".join(password_chars)

    def calculate_entropy(self, password: str) -> Tuple[float, str, str]:
        """
        Calculates Shannon entropy for the password: E = L * log2(R).
        
        Returns:
            Tuple[float, str, str]: (entropy_bits, strength_label, color_hex)
        """
        if not password:
            return 0.0, "Empty", "#64748b"
            
        # Deduce pool size R based on character classes present in password
        r = 0
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_digit = any(c in string.digits for c in password)
        # Check for special characters
        has_special = any(c not in (string.ascii_letters + string.digits + " \t\n\r") for c in password)
        has_space = " " in password
        
        if has_lower:
            r += 26
        if has_upper:
            r += 26
        if has_digit:
            r += 10
        if has_special:
            r += 32
        if has_space:
            r += 1
            
        if r == 0:
            r = 1  # Fallback to avoid log(0)
            
        length = len(password)
        entropy = length * math.log2(r)
        
        # Rank strength based on industry guidelines
        if entropy < 36:
            return entropy, "Very Weak", "#ef4444"  # Red
        elif 36 <= entropy < 60:
            return entropy, "Weak", "#f97316"  # Orange
        elif 60 <= entropy < 80:
            return entropy, "Medium", "#eab308"  # Yellow
        elif 80 <= entropy < 120:
            return entropy, "Strong", "#22c55e"  # Green
        else:
            return entropy, "Very Strong", "#06b6d4"  # Cyan
