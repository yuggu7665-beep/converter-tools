"""AI & Data API Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from converters.ai_data import CSVToJSONLConverter, TokenCounterConverter, JSONToCSVConverter
from core.exceptions import ConverterException

router = APIRouter(prefix="/ai-data", tags=["AI & Data"])


# Request/Response Models
class CSVToJSONLRequest(BaseModel):
    csv_content: str = Field(..., description="CSV content to convert")

class CSVToJSONLResponse(BaseModel):
    jsonl_content: str
    line_count: int


class TokenCountRequest(BaseModel):
    text: str = Field(..., description="Text to count tokens")
    model: str = Field(default="gpt-4", description="LLM model (gpt-4, claude, gemini)")

class TokenCountResponse(BaseModel):
    characters: int
    words: int
    estimated_tokens: int
    model: str
    estimated_cost_usd: float


class JSONToCSVRequest(BaseModel):
    json_content: str = Field(..., description="JSON content (array of objects)")

class JSONToCSVResponse(BaseModel):
    csv_content: str
    row_count: int


# Endpoints
@router.post("/csv-to-jsonl", response_model=CSVToJSONLResponse, summary="Convert CSV to JSONL")
async def csv_to_jsonl(request: CSVToJSONLRequest):
    """
    Convert CSV to JSONL format for AI fine-tuning datasets.
    
    **Example Request:**
    ```json
    {
        "csv_content": "name,age\\nAlice,30\\nBob,25"
    }
    ```
    """
    try:
        result = CSVToJSONLConverter.convert(request.csv_content)
        line_count = len(result.split('\n'))
        
        return CSVToJSONLResponse(
            jsonl_content=result,
            line_count=line_count
        )
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token-count", response_model=TokenCountResponse, summary="Count tokens in text")
async def token_count(request: TokenCountRequest):
    """
    Count tokens and estimate cost for LLM prompts.
    
    **Example Request:**
    ```json
    {
        "text": "Hello, how are you?",
        "model": "gpt-4"
    }
    ```
    """
    try:
        result = TokenCounterConverter.count_tokens(request.text, request.model)
        return TokenCountResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/json-to-csv", response_model=JSONToCSVResponse, summary="Convert JSON to CSV")
async def json_to_csv(request: JSONToCSVRequest):
    """
    Convert JSON array to CSV format.
    
    **Example Request:**
    ```json
    {
        "json_content": "[{\\"name\\":\\"Alice\\",\\"age\\":30},{\\"name\\":\\"Bob\\",\\"age\\":25}]"
    }
    ```
    """
    try:
        result = JSONToCSVConverter.convert(request.json_content)
        row_count = len(result.split('\n')) - 1  # Subtract header
        
        return JSONToCSVResponse(
            csv_content=result,
            row_count=row_count
        )
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
