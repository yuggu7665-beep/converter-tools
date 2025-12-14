"""Education & Engineering API Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from converters.education import NumberSystemConverter, ColorCodeConverter, PercentageCalculator
from core.exceptions import ConverterException
from typing import Any, Optional

router = APIRouter(prefix="/education", tags=["Education & Engineering"])


# Request/Response Models
class NumberSystemRequest(BaseModel):
    number: str = Field(..., description="Number to convert")
    from_system: str = Field(..., description="Source system (binary, octal, decimal, hexadecimal)")
    to_system: str = Field(..., description="Target system")


class NumberSystemResponse(BaseModel):
    original_number: str
    original_system: str
    converted_number: str
    converted_system: str
    decimal_value: int


class ColorConvertRequest(BaseModel):
    color_value: str = Field(..., description="Color value (HEX or RGB as 'r,g,b')")
    from_format: str = Field(..., description="Source format (hex, rgb)")
    to_format: Optional[str] = Field(default=None, description="Target format (optional, returns all if not specified)")


class PercentageRequest(BaseModel):
    calculation_type: str = Field(..., description="Type: percentage_of, what_percent, increase, decrease, change")
    values: dict[str, float] = Field(..., description="Values for calculation")


# Endpoints
@router.post("/number-system", response_model=NumberSystemResponse, summary="Convert number systems")
async def number_system(request: NumberSystemRequest):
    """
    Convert between number systems (Binary, Octal, Decimal, Hexadecimal).
    
    **Example Request:**
    ```json
    {
        "number": "255",
        "from_system": "decimal",
        "to_system": "hexadecimal"
    }
    ```
    """
    try:
        result = NumberSystemConverter.convert(
            request.number,
            request.from_system,
            request.to_system
        )
        return NumberSystemResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/color-convert", summary="Convert color codes")
async def color_convert(request: ColorConvertRequest):
    """
    Convert between color code formats (HEX, RGB, HSL, CMYK).
    
    **Example Request:**
    ```json
    {
        "color_value": "#FF5733",
        "from_format": "hex"
    }
    ```
    """
    try:
        result = ColorCodeConverter.convert(
            request.color_value,
            request.from_format,
            request.to_format
        )
        return result
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/percentage-calculate", summary="Calculate percentage")
async def percentage_calculate(request: PercentageRequest):
    """
    Calculate percentages.
    
    **Types:**
    - percentage_of: What is X% of Y? (values: percentage, total)
    - what_percent: X is what % of Y? (values: value, total)
    - increase: Increase X by Y% (values: value, percentage)
    - decrease: Decrease X by Y% (values: value, percentage)
    - change: % change from X to Y (values: old_value, new_value)
    
    **Example Request:**
    ```json
    {
        "calculation_type": "percentage_of",
        "values": {"percentage": 20, "total": 500}
    }
    ```
    """
    try:
        result = PercentageCalculator.calculate(
            request.calculation_type,
            **request.values
        )
        return result
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
