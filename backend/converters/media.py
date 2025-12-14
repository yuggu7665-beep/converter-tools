"""Media Converters"""
import base64
import io
from PIL import Image
from PyPDF2 import PdfReader
from typing import Dict, Any
from core.exceptions import ValidationException, ProcessingException, UnsupportedFormatException


class ImageToWebPConverter:
    """Convert images to WebP format for web optimization"""
    
    @staticmethod
    def convert(image_data: bytes, quality: int = 85) -> bytes:
        """
        Convert image to WebP format
        
        Args:
            image_data: Binary image data
            quality: WebP quality (1-100)
            
        Returns:
            WebP image bytes
        """
        if not 1 <= quality <= 100:
            raise ValidationException("Quality must be between 1 and 100")
        
        try:
            # Open image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary (WebP doesn't support all modes)
            if image.mode not in ('RGB', 'RGBA'):
                image = image.convert('RGB')
            
            # Save as WebP
            output = io.BytesIO()
            image.save(output, format='WEBP', quality=quality, method=6)
            output.seek(0)
            
            return output.getvalue()
            
        except Exception as e:
            raise ProcessingException(f"Image conversion failed: {str(e)}")


class ImageCompressorConverter:
    """Compress images while maintaining quality"""
    
    @staticmethod
    def compress(image_data: bytes, max_size_kb: int = 500, quality: int = 85) -> Dict[str, Any]:
        """
        Compress image to target size
        
        Args:
            image_data: Binary image data
            max_size_kb: Maximum target size in KB
            quality: Initial quality (will be adjusted)
            
        Returns:
            Dictionary with compressed image and metadata
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            original_size = len(image_data)
            
            # Get original format
            original_format = image.format or 'JPEG'
            
            # Try to compress
            output = io.BytesIO()
            current_quality = quality
            
            while current_quality > 10:
                output.seek(0)
                output.truncate()
                
                if image.mode not in ('RGB', 'RGBA', 'L'):
                    image = image.convert('RGB')
                
                image.save(output, format=original_format, quality=current_quality, optimize=True)
                
                compressed_size = output.tell()
                
                if compressed_size <= max_size_kb * 1024 or current_quality <= 20:
                    break
                
                current_quality -= 5
            
            output.seek(0)
            compressed_data = output.getvalue()
            
            compression_ratio = (1 - len(compressed_data) / original_size) * 100
            
            return {
                "compressed_image": base64.b64encode(compressed_data).decode('utf-8'),
                "original_size_bytes": original_size,
                "compressed_size_bytes": len(compressed_data),
                "compression_ratio_percent": round(compression_ratio, 2),
                "final_quality": current_quality
            }
            
        except Exception as e:
            raise ProcessingException(f"Image compression failed: {str(e)}")


class PDFToTextConverter:
    """Extract text from PDF files"""
    
    @staticmethod
    def extract_text(pdf_data: bytes) -> Dict[str, Any]:
        """
        Extract text from PDF
        
        Args:
            pdf_data: Binary PDF data
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            pdf_file = io.BytesIO(pdf_data)
            reader = PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = []
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text_content.append({
                    "page": page_num,
                    "text": page_text.strip()
                })
            
            # Combine all text
            full_text = "\n\n".join([p["text"] for p in text_content if p["text"]])
            
            return {
                "total_pages": len(reader.pages),
                "text": full_text,
                "pages": text_content,
                "character_count": len(full_text),
                "word_count": len(full_text.split())
            }
            
        except Exception as e:
            raise ProcessingException(f"PDF text extraction failed: {str(e)}")
