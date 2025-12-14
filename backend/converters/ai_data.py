"""AI & Data Converters"""
import csv
import json
import io
from typing import Dict, List, Any
from core.exceptions import ValidationException, ProcessingException


class CSVToJSONLConverter:
    """Convert CSV data to JSONL format for AI fine-tuning"""
    
    @staticmethod
    def convert(csv_content: str) -> str:
        """
        Convert CSV to JSONL
        
        Args:
            csv_content: CSV string content
            
        Returns:
            JSONL formatted string
        """
        try:
            csv_file = io.StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            jsonl_lines = []
            for row in reader:
                jsonl_lines.append(json.dumps(row))
            
            if not jsonl_lines:
                raise ValidationException("CSV file is empty or has no valid rows")
                
            return "\n".join(jsonl_lines)
        except csv.Error as e:
            raise ProcessingException(f"CSV parsing error: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"Conversion failed: {str(e)}")


class TokenCounterConverter:
    """Count tokens in text for LLM usage estimation"""
    
    # Approximate token counts (1 token ≈ 4 characters for English)
    CHARS_PER_TOKEN = 4
    
    @staticmethod
    def count_tokens(text: str, model: str = "gpt-4") -> Dict[str, Any]:
        """
        Count tokens in text
        
        Args:
            text: Input text
            model: LLM model name (gpt-4, claude, gemini)
            
        Returns:
            Dictionary with character count, word count, and estimated tokens
        """
        if not text:
            raise ValidationException("Text cannot be empty")
        
        # Basic counts
        char_count = len(text)
        word_count = len(text.split())
        
        # Estimate tokens (simple approximation)
        # In production, you'd use tiktoken for GPT or model-specific tokenizers
        estimated_tokens = char_count // TokenCounterConverter.CHARS_PER_TOKEN
        
        # Cost estimation (example rates, update with current pricing)
        cost_per_1k_tokens = {
            "gpt-4": 0.03,
            "gpt-3.5-turbo": 0.002,
            "claude": 0.024,
            "gemini": 0.00025
        }
        
        rate = cost_per_1k_tokens.get(model.lower(), 0.01)
        estimated_cost = (estimated_tokens / 1000) * rate
        
        return {
            "characters": char_count,
            "words": word_count,
            "estimated_tokens": estimated_tokens,
            "model": model,
            "estimated_cost_usd": round(estimated_cost, 6)
        }


class JSONToCSVConverter:
    """Convert JSON data to CSV format"""
    
    @staticmethod
    def convert(json_content: str) -> str:
        """
        Convert JSON to CSV
        
        Args:
            json_content: JSON string content (array of objects)
            
        Returns:
            CSV formatted string
        """
        try:
            data = json.loads(json_content)
            
            # Handle single object
            if isinstance(data, dict):
                data = [data]
            
            if not isinstance(data, list):
                raise ValidationException("JSON must be an array of objects")
            
            if not data:
                raise ValidationException("JSON array is empty")
            
            # Get all unique keys from all objects
            all_keys = set()
            for item in data:
                if isinstance(item, dict):
                    all_keys.update(item.keys())
            
            if not all_keys:
                raise ValidationException("No valid objects found in JSON")
            
            # Sort keys for consistent output
            fieldnames = sorted(all_keys)
            
            # Write CSV
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in data:
                if isinstance(item, dict):
                    writer.writerow(item)
            
            return output.getvalue()
            
        except json.JSONDecodeError as e:
            raise ValidationException(f"Invalid JSON: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"Conversion failed: {str(e)}")
