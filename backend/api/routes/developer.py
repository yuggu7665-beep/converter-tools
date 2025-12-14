"""Developer Tools API Routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from converters.developer import JSONToYAMLConverter, Base64Converter, JWTDecoder
from core.exceptions import ConverterException
from typing import Any, Optional

router = APIRouter(prefix="/developer", tags=["Developer Tools"])


# Request/Response Models
class JSONToYAMLRequest(BaseModel):
    json_content: str = Field(..., description="JSON content")


class YAMLToJSONRequest(BaseModel):
    yaml_content: str = Field(..., description="YAML content")
    pretty: bool = Field(default=True, description="Pretty print JSON")


class Base64EncodeRequest(BaseModel):
    text: str = Field(..., description="Text to encode")


class Base64DecodeRequest(BaseModel):
    encoded_text: str = Field(..., description="Base64 encoded text")


class JWTDecodeRequest(BaseModel):
    token: str = Field(..., description="JWT token")
    verify: bool = Field(default=False, description="Verify signature")
    secret: Optional[str] = Field(default=None, description="Secret key for verification")


class JWTDecodeResponse(BaseModel):
    header: dict[str, Any]
    payload: dict[str, Any]
    signature: Optional[str]
    verified: bool
    algorithm: str


# Endpoints
@router.post("/json-to-yaml", summary="Convert JSON to YAML")
async def json_to_yaml(request: JSONToYAMLRequest):
    """
    Convert JSON to YAML format.
    
    **Example Request:**
    ```json
    {
        "json_content": "{\\"name\\":\\"test\\",\\"value\\":123}"
    }
    ```
    """
    try:
        result = JSONToYAMLConverter.json_to_yaml(request.json_content)
        return {"yaml_content": result}
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/yaml-to-json", summary="Convert YAML to JSON")
async def yaml_to_json(request: YAMLToJSONRequest):
    """
    Convert YAML to JSON format.
    
    **Example Request:**
    ```json
    {
        "yaml_content": "name: test\\nvalue: 123",
        "pretty": true
    }
    ```
    """
    try:
        result = JSONToYAMLConverter.yaml_to_json(request.yaml_content, request.pretty)
        return {"json_content": result}
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/base64-encode", summary="Encode to Base64")
async def base64_encode(request: Base64EncodeRequest):
    """
    Encode text to Base64.
    
    **Example Request:**
    ```json
    {
        "text": "Hello, World!"
    }
    ```
    """
    try:
        result = Base64Converter.encode(request.text)
        return {"encoded_text": result}
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/base64-decode", summary="Decode from Base64")
async def base64_decode(request: Base64DecodeRequest):
    """
    Decode Base64 to text.
    
    **Example Request:**
    ```json
    {
        "encoded_text": "SGVsbG8sIFdvcmxkIQ=="
    }
    ```
    """
    try:
        result = Base64Converter.decode(request.encoded_text)
        return {"decoded_text": result}
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jwt-decode", response_model=JWTDecodeResponse, summary="Decode JWT token")
async def jwt_decode(request: JWTDecodeRequest):
    """
    Decode and validate JWT tokens.
    
    **Example Request:**
    ```json
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "verify": false
    }
    ```
    """
    try:
        result = JWTDecoder.decode(request.token, request.verify, request.secret)
        return JWTDecodeResponse(**result)
    except ConverterException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
