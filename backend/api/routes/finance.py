"""Finance API Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from converters.finance import CurrencyConverter, CryptoPriceTracker, GSTCalculator
from core.exceptions import ConverterException

router = APIRouter(prefix="/finance", tags=["Finance"])


# Request/Response Models
class CurrencyConvertRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to convert")
    from_currency: str = Field(..., description="Source currency code (e.g., USD)")
    to_currency: str = Field(..., description="Target currency code (e.g., EUR)")


class CurrencyConvertResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
    exchange_rate: float
    timestamp: str


class CryptoPriceRequest(BaseModel):
    crypto_symbol: str = Field(..., description="Crypto symbol (BTC, ETH, etc.)")
    vs_currency: str = Field(default="USD", description="Target currency (USD, EUR, etc.)")


class CryptoPriceResponse(BaseModel):
    cryptocurrency: str
    currency: str
    price: float
    change_24h_percent: float | None
    timestamp: str


class GSTCalculateRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Base or total amount")
    tax_rate: float = Field(..., ge=0, le=100, description="Tax rate percentage")
    include_tax: bool = Field(default=False, description="True if amount includes tax")


class GSTCalculateResponse(BaseModel):
    base_amount: float
    tax_rate_percent: float
    tax_amount: float
    total_amount: float
    tax_included: bool


# Endpoints
@router.post("/currency-convert", response_model=CurrencyConvertResponse, summary="Convert currency")
async def currency_convert(request: CurrencyConvertRequest):
    """
    Convert between currencies using real-time exchange rates.
    
    **Example Request:**
    ```json
    {
        "amount": 100,
        "from_currency": "USD",
        "to_currency": "EUR"
    }
    ```
    """
    try:
        result = CurrencyConverter.convert(
            request.amount,
            request.from_currency,
            request.to_currency
        )
        return CurrencyConvertResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crypto-price", response_model=CryptoPriceResponse, summary="Get crypto price")
async def crypto_price(request: CryptoPriceRequest):
    """
    Get real-time cryptocurrency prices.
    
    **Supported coins:** BTC, ETH, BNB, XRP, ADA, DOGE, SOL, MATIC
    
    **Example Request:**
    ```json
    {
        "crypto_symbol": "BTC",
        "vs_currency": "USD"
    }
    ```
    """
    try:
        result = CryptoPriceTracker.get_price(
            request.crypto_symbol,
            request.vs_currency
        )
        return CryptoPriceResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gst-calculate", response_model=GSTCalculateResponse, summary="Calculate GST/Tax")
async def gst_calculate(request: GSTCalculateRequest):
    """
    Calculate GST/VAT/Sales Tax.
    
    **Example Request:**
    ```json
    {
        "amount": 100,
        "tax_rate": 18,
        "include_tax": false
    }
    ```
    """
    try:
        result = GSTCalculator.calculate(
            request.amount,
            request.tax_rate,
            request.include_tax
        )
        return GSTCalculateResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
