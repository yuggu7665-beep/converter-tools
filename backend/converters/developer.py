"""Developer Tools Converters"""
import json
import yaml
import base64
import jwt
from typing import Dict, Any
from core.exceptions import ValidationException, ProcessingException


class JSONToYAMLConverter:
    """Convert between JSON and YAML formats"""
    
    @staticmethod
    def json_to_yaml(json_content: str) -> str:
        """
        Convert JSON to YAML
        
        Args:
            json_content: JSON string
            
        Returns:
            YAML formatted string
        """
        try:
            data = json.loads(json_content)
            yaml_content = yaml.dump(data, default_flow_style=False, sort_keys=False)
            return yaml_content
        except json.JSONDecodeError as e:
            raise ValidationException(f"Invalid JSON: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"Conversion failed: {str(e)}")
    
    @staticmethod
    def yaml_to_json(yaml_content: str, pretty: bool = True) -> str:
        """
        Convert YAML to JSON
        
        Args:
            yaml_content: YAML string
            pretty: Pretty print JSON
            
        Returns:
            JSON formatted string
        """
        try:
            data = yaml.safe_load(yaml_content)
            if pretty:
                json_content = json.dumps(data, indent=2)
            else:
                json_content = json.dumps(data)
            return json_content
        except yaml.YAMLError as e:
            raise ValidationException(f"Invalid YAML: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"Conversion failed: {str(e)}")


class Base64Converter:
    """Encode and decode Base64"""
    
    @staticmethod
    def encode(text: str) -> str:
        """
        Encode text to Base64
        
        Args:
            text: Plain text string
            
        Returns:
            Base64 encoded string
        """
        try:
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            return encoded
        except Exception as e:
            raise ProcessingException(f"Encoding failed: {str(e)}")
    
    @staticmethod
    def decode(encoded_text: str) -> str:
        """
        Decode Base64 to text
        
        Args:
            encoded_text: Base64 encoded string
            
        Returns:
            Decoded plain text
        """
        try:
            decoded = base64.b64decode(encoded_text).decode('utf-8')
            return decoded
        except Exception as e:
            raise ValidationException(f"Invalid Base64 or decoding failed: {str(e)}")
    
    @staticmethod
    def encode_file(file_data: bytes) -> str:
        """
        Encode binary file to Base64
        
        Args:
            file_data: Binary file data
            
        Returns:
            Base64 encoded string
        """
        try:
            encoded = base64.b64encode(file_data).decode('utf-8')
            return encoded
        except Exception as e:
            raise ProcessingException(f"File encoding failed: {str(e)}")


class JWTDecoder:
    """Decode and validate JWT tokens"""
    
    @staticmethod
    def decode(token: str, verify: bool = False, secret: str = None) -> Dict[str, Any]:
        """
        Decode JWT token
        
        Args:
            token: JWT token string
            verify: Whether to verify signature
            secret: Secret key for verification (required if verify=True)
            
        Returns:
            Dictionary with header, payload, and signature
        """
        try:
            # Decode without verification first to get header and payload
            unverified_header = jwt.get_unverified_header(token)
            
            if verify:
                if not secret:
                    raise ValidationException("Secret key required for verification")
                decoded_payload = jwt.decode(token, secret, algorithms=["HS256", "RS256"])
            else:
                decoded_payload = jwt.decode(token, options={"verify_signature": False})
            
            # Split token to show parts
            parts = token.split('.')
            
            return {
                "header": unverified_header,
                "payload": decoded_payload,
                "signature": parts[2] if len(parts) > 2 else None,
                "verified": verify,
                "algorithm": unverified_header.get('alg', 'unknown')
            }
            
        except jwt.ExpiredSignatureError:
            raise ValidationException("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValidationException(f"Invalid JWT token: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"JWT decoding failed: {str(e)}")
