"""
modules/utilities.py
Defines the base interface class and exceptions for all toolkit modules.
Ensures object-oriented, extensible structure.
"""

from abc import ABC, abstractmethod
from typing import Any, Union

class ToolkitError(Exception):
    """Base exception class for all errors in the toolkit."""
    pass

class EncodingError(ToolkitError):
    """Exception raised when an encoding operation fails."""
    pass

class DecodingError(ToolkitError):
    """Exception raised when a decoding operation fails."""
    pass

class EncoderDecoder(ABC):
    """
    Abstract Base Class defining the interface for all encoder/decoder modules.
    All encoding/decoding modules must inherit from this class.
    """
    
    @abstractmethod
    def encode(self, data: Union[str, bytes], **kwargs: Any) -> Union[str, bytes]:
        """
        Encodes the input data.
        
        Args:
            data (str or bytes): Input data to encode.
            **kwargs: Dynamic arguments specific to the algorithm.
            
        Returns:
            str or bytes: Encoded output.
            
        Raises:
            EncodingError: If the encoding process fails.
        """
        pass
        
    @abstractmethod
    def decode(self, data: Union[str, bytes], **kwargs: Any) -> Union[str, bytes]:
        """
        Decodes the input data.
        
        Args:
            data (str or bytes): Input data to decode.
            **kwargs: Dynamic arguments specific to the algorithm.
            
        Returns:
            str or bytes: Decoded output.
            
        Raises:
            DecodingError: If the decoding process fails.
        """
        pass
