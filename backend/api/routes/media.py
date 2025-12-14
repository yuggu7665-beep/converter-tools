"""Media API Routes"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from converters.media import ImageToWebPConverter, ImageCompressorConverter, PDFToTextConverter
from core.exceptions import ConverterException
import base64

router = APIRouter(prefix="/media", tags=["Media"])


# Response Models
class ImageConversionResponse(BaseModel):
    webp_image: str = Field(..., description="Base64 encoded WebP image")
    original_size_bytes: int
    converted_size_bytes: int


class ImageCompressionResponse(BaseModel):
    compressed_image: str
    original_size_bytes: int
    compressed_size_bytes: int
    compression_ratio_percent: float
    final_quality: int


class PDFTextResponse(BaseModel):
    total_pages: int
    text: str
    character_count: int
    word_count: int


# Endpoints
@router.post("/image-to-webp", response_model=ImageConversionResponse, summary="Convert image to WebP")
async def image_to_webp(file: UploadFile = File(...), quality: int = 85):
    """
    Convert images to WebP format for web optimization.
    
    **Parameters:**
    - file: Image file (JPEG, PNG, etc.)
    - quality: WebP quality 1-100 (default: 85)
    """
    try:
        image_data = await file.read()
        original_size = len(image_data)
        
        webp_data = ImageToWebPConverter.convert(image_data, quality)
        webp_base64 = base64.b64encode(webp_data).decode('utf-8')
        
        return ImageConversionResponse(
            webp_image=f"data:image/webp;base64,{webp_base64}",
            original_size_bytes=original_size,
            converted_size_bytes=len(webp_data)
        )
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image-compress", response_model=ImageCompressionResponse, summary="Compress image")
async def image_compress(file: UploadFile = File(...), max_size_kb: int = 500, quality: int = 85):
    """
    Compress images while maintaining quality.
    
    **Parameters:**
    - file: Image file
    - max_size_kb: Maximum target size in KB (default: 500)
    - quality: Initial compression quality (default: 85)
    """
    try:
        image_data = await file.read()
        result = ImageCompressorConverter.compress(image_data, max_size_kb, quality)
        
        return ImageCompressionResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pdf-to-text", response_model=PDFTextResponse, summary="Extract text from PDF")
async def pdf_to_text(file: UploadFile = File(...)):
    """
    Extract text content from PDF files.
    
    **Parameters:**
    - file: PDF file
    """
    try:
        pdf_data = await file.read()
        result = PDFToTextConverter.extract_text(pdf_data)
        
        return PDFTextResponse(
            total_pages=result['total_pages'],
            text=result['text'],
            character_count=result['character_count'],
            word_count=result['word_count']
        )
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
