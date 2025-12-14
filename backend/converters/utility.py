"""Daily Utility Converters"""
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones
import qrcode
import io
import base64
from typing import Dict, Any
from core.exceptions import ValidationException, ProcessingException


class UnitConverter:
    """Convert between different units"""
    
    CONVERSIONS = {
        # Length (to meters)
        "length": {
            "meter": 1,
            "kilometer": 1000,
            "centimeter": 0.01,
            "millimeter": 0.001,
            "mile": 1609.34,
            "yard": 0.9144,
            "foot": 0.3048,
            "inch": 0.0254
        },
        # Weight (to kilograms)
        "weight": {
            "kilogram": 1,
            "gram": 0.001,
            "milligram": 0.000001,
            "pound": 0.453592,
            "ounce": 0.0283495,
            "ton": 1000
        },
        # Temperature (special handling)
        "temperature": {
            "celsius": "celsius",
            "fahrenheit": "fahrenheit",
            "kelvin": "kelvin"
        },
        # Area (to square meters)
        "area": {
            "square_meter": 1,
            "square_kilometer": 1000000,
            "square_centimeter": 0.0001,
            "square_foot": 0.092903,
            "square_mile": 2589988,
            "acre": 4046.86,
            "hectare": 10000
        }
    }
    
    @staticmethod
    def convert(value: float, from_unit: str, to_unit: str, category: str) -> Dict[str, Any]:
        """
        Convert between units
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            category: Unit category (length, weight, temperature, area)
            
        Returns:
            Dictionary with conversion result
        """
        if category not in UnitConverter.CONVERSIONS:
            raise ValidationException(f"Unsupported category: {category}")
        
        units = UnitConverter.CONVERSIONS[category]
        
        if from_unit not in units or to_unit not in units:
            raise ValidationException(f"Invalid units for category {category}")
        
        # Special handling for temperature
        if category == "temperature":
            result = UnitConverter._convert_temperature(value, from_unit, to_unit)
        else:
            # Convert to base unit, then to target unit
            base_value = value * units[from_unit]
            result = base_value / units[to_unit]
        
        return {
            "original_value": value,
            "original_unit": from_unit,
            "converted_value": round(result, 6),
            "converted_unit": to_unit,
            "category": category
        }
    
    @staticmethod
    def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between units"""
        # Convert to Celsius first
        if from_unit == "fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "kelvin":
            celsius = value - 273.15
        else:  # celsius
            celsius = value
        
        # Convert from Celsius to target
        if to_unit == "fahrenheit":
            return celsius * 9/5 + 32
        elif to_unit == "kelvin":
            return celsius + 273.15
        else:  # celsius
            return celsius


class TimezoneConverter:
    """Convert times between timezones"""
    
    @staticmethod
    def convert(time_str: str, from_timezone: str, to_timezone: str, date_str: str = None) -> Dict[str, Any]:
        """
        Convert time between timezones
        
        Args:
            time_str: Time in HH:MM format
            from_timezone: Source timezone (e.g., 'America/New_York')
            to_timezone: Target timezone (e.g., 'Europe/London')
            date_str: Optional date in YYYY-MM-DD format (defaults to today)
            
        Returns:
            Dictionary with converted time
        """
        try:
            # Validate timezones
            if from_timezone not in available_timezones():
                raise ValidationException(f"Invalid source timezone: {from_timezone}")
            if to_timezone not in available_timezones():
                raise ValidationException(f"Invalid target timezone: {to_timezone}")
            
            # Parse date or use today
            if date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date_obj = datetime.now().date()
            
            # Parse time
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            
            # Combine date and time
            dt_naive = datetime.combine(date_obj, time_obj)
            
            # Localize to source timezone
            dt_source = dt_naive.replace(tzinfo=ZoneInfo(from_timezone))
            
            # Convert to target timezone
            dt_target = dt_source.astimezone(ZoneInfo(to_timezone))
            
            return {
                "source_datetime": dt_source.strftime("%Y-%m-%d %H:%M %Z"),
                "target_datetime": dt_target.strftime("%Y-%m-%d %H:%M %Z"),
                "source_timezone": from_timezone,
                "target_timezone": to_timezone,
                "time_difference_hours": (dt_target.hour - dt_source.hour) % 24
            }
            
        except ValueError as e:
            raise ValidationException(f"Invalid date/time format: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"Timezone conversion failed: {str(e)}")


class QRCodeGenerator:
    """Generate QR codes from text/URLs"""
    
    @staticmethod
    def generate(data: str, size: int = 10, border: int = 4) -> Dict[str, Any]:
        """
        Generate QR code
        
        Args:
            data: Text or URL to encode
            size: QR code box size (1-40)
            border: Border size in boxes (minimum 4)
            
        Returns:
            Dictionary with Base64 encoded QR code image
        """
        if not data:
            raise ValidationException("Data cannot be empty")
        
        if not 1 <= size <= 40:
            raise ValidationException("Size must be between 1 and 40")
        
        if border < 4:
            raise ValidationException("Border must be at least 4")
        
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Generate image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Encode to Base64
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return {
                "qr_code_image": f"data:image/png;base64,{img_base64}",
                "data": data,
                "size": size,
                "border": border
            }
            
        except Exception as e:
            raise ProcessingException(f"QR code generation failed: {str(e)}")
