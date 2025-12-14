"""Daily Utility API Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from converters.utility import UnitConverter, TimezoneConverter, QRCodeGenerator
from core.exceptions import ConverterException
from typing import Optional

router = APIRouter(prefix="/utility", tags=["Daily Utility"])


# Request/Response Models
class UnitConvertRequest(BaseModel):
    value: float = Field(..., description="Value to convert")
    from_unit: str = Field(..., description="Source unit")
    to_unit: str = Field(..., description="Target unit")
    category: str = Field(..., description="Unit category (length, weight, temperature, area)")


class UnitConvertResponse(BaseModel):
    original_value: float
    original_unit: str
    converted_value: float
    converted_unit: str
    category: str


class TimezoneConvertRequest(BaseModel):
    time_str: str = Field(..., description="Time in HH:MM format")
    from_timezone: str = Field(..., description="Source timezone (e.g., America/New_York)")
    to_timezone: str = Field(..., description="Target timezone (e.g., Europe/London)")
    date_str: Optional[str] = Field(default=None, description="Optional date in YYYY-MM-DD format")


class TimezoneConvertResponse(BaseModel):
    source_datetime: str
    target_datetime: str
    source_timezone: str
    target_timezone: str
    time_difference_hours: int


class QRCodeRequest(BaseModel):
    data: str = Field(..., description="Text or URL to encode")
    size: int = Field(default=10, ge=1, le=40, description="QR code size")
    border: int = Field(default=4, ge=4, description="Border size")


class QRCodeResponse(BaseModel):
    qr_code_image: str
    data: str
    size: int
    border: int


# Endpoints
@router.post("/unit-convert", response_model=UnitConvertResponse, summary="Convert units")
async def unit_convert(request: UnitConvertRequest):
    """
    Convert between different units.
    
    **Categories:** length, weight, temperature, area
    
    **Example Request:**
    ```json
    {
        "value": 100,
        "from_unit": "meter",
        "to_unit": "foot",
        "category": "length"
    }
    ```
    """
    try:
        result = UnitConverter.convert(
            request.value,
            request.from_unit,
            request.to_unit,
            request.category
        )
        return UnitConvertResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/timezone-convert", response_model=TimezoneConvertResponse, summary="Convert timezone")
async def timezone_convert(request: TimezoneConvertRequest):
    """
    Convert times between timezones.
    
    **Example Request:**
    ```json
    {
        "time_str": "14:30",
        "from_timezone": "America/New_York",
        "to_timezone": "Europe/London"
    }
    ```
    """
    try:
        result = TimezoneConverter.convert(
            request.time_str,
            request.from_timezone,
            request.to_timezone,
            request.date_str
        )
        return TimezoneConvertResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/qr-generate", response_model=QRCodeResponse, summary="Generate QR code")
async def qr_generate(request: QRCodeRequest):
    """
    Generate QR codes from text or URLs.
    
    **Example Request:**
    ```json
    {
        "data": "https://example.com",
        "size": 10,
        "border": 4
    }
    ```
    """
    try:
        result = QRCodeGenerator.generate(
            request.data,
            request.size,
            request.border
        )
        return QRCodeResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
