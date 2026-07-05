"""
modules/morse.py
Implements Morse code translation for text.
"""

from typing import Union, Any
from modules.utilities import EncoderDecoder, EncodingError, DecodingError
from utils.constants import MORSE_CODE_DICT, REVERSE_MORSE_DICT

class MorseCoder(EncoderDecoder):
    """Morse Code Translator."""
    
    def encode(self, data: Union[str, bytes], char_delimiter: str = " ", word_delimiter: str = " / ", **kwargs: Any) -> str:
        """Translates text to Morse code."""
        try:
            if isinstance(data, bytes):
                text = data.decode('utf-8', errors='replace')
            else:
                text = data
                
            text = text.upper()
            result = []
            
            # Split words by space
            words = text.split(" ")
            for w in words:
                morse_word = []
                for char in w:
                    if char in MORSE_CODE_DICT:
                        morse_word.append(MORSE_CODE_DICT[char])
                    else:
                        # Ignore unknown characters
                        pass
                if morse_word:
                    result.append(char_delimiter.join(morse_word))
                    
            return word_delimiter.join(result)
        except Exception as e:
            raise EncodingError(f"Morse encoding failed: {str(e)}")
            
    def decode(self, data: Union[str, bytes], char_delimiter: str = " ", word_delimiter: str = "/", **kwargs: Any) -> str:
        """Translates Morse code back to text."""
        try:
            if isinstance(data, bytes):
                morse_str = data.decode('utf-8', errors='replace')
            else:
                morse_str = data
                
            morse_str = morse_str.strip()
            if not morse_str:
                return ""
                
            # If word_delimiter contains spaces, clean it up
            clean_word_delimiter = word_delimiter.strip()
            
            # Split by word delimiter
            words = morse_str.split(clean_word_delimiter)
            decoded_words = []
            
            for word in words:
                word = word.strip()
                if not word:
                    continue
                # Split characters
                chars = word.split(char_delimiter.strip() or " ")
                decoded_chars = []
                for morse_char in chars:
                    morse_char = morse_char.strip()
                    if not morse_char:
                        continue
                    if morse_char in REVERSE_MORSE_DICT:
                        decoded_chars.append(REVERSE_MORSE_DICT[morse_char])
                    else:
                        decoded_chars.append("?")
                decoded_words.append("".join(decoded_chars))
                
            return " ".join(decoded_words)
        except Exception as e:
            raise DecodingError(f"Morse decoding failed: {str(e)}")
