"""
modules/qr.py
Implements QR code generation and decoding utilities.
Generates using qrcode and decodes using OpenCV.
"""

import io
import cv2
import numpy as np
from PIL import Image
import qrcode
from typing import Tuple, Union, Optional

class QRTool:
    """QR Code Generator and Decoder."""
    
    def generate_qr(self, text: str, box_size: int = 10, border: int = 4, fill_color: str = "black", back_color: str = "white") -> bytes:
        """
        Generates a QR code image as PNG bytes.
        """
        try:
            qr = qrcode.QRCode(
                version=None,  # Automatically fit data
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=box_size,
                border=border,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            # Save PIL image to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        except Exception as e:
            raise RuntimeError(f"Failed to generate QR code: {str(e)}")
            
    def decode_qr(self, image_bytes: bytes) -> Tuple[bool, str]:
        """
        Decodes a QR code from image bytes using OpenCV's QRCodeDetector.
        
        Returns:
            Tuple[bool, str]: (success, decoded_data_or_error)
        """
        try:
            # Load PIL image from bytes
            pil_img = Image.open(io.BytesIO(image_bytes))
            
            # Convert PIL image to RGB/BGR OpenCV numpy array
            np_img = np.array(pil_img.convert('RGB'))
            opencv_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
            
            # Use OpenCV QR Code Detector
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(opencv_img)
            
            if bbox is not None and data:
                return True, data
            
            # Try nested fallback - sometimes grayscale helps
            gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
            data, bbox, _ = detector.detectAndDecode(gray)
            if bbox is not None and data:
                return True, data
                
            return False, "No QR Code detected in the image."
        except Exception as e:
            return False, f"Failed to decode QR code: {str(e)}"
