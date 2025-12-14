"""Education & Engineering Converters"""
from typing import Dict, Any
from core.exceptions import ValidationException, ProcessingException


class NumberSystemConverter:
    """Convert between number systems"""
    
    SYSTEMS = {
        "binary": 2,
        "octal": 8,
        "decimal": 10,
        "hexadecimal": 16
    }
    
    @staticmethod
    def convert(number: str, from_system: str, to_system: str) -> Dict[str, Any]:
        """
        Convert between number systems
        
        Args:
            number: Number as string
            from_system: Source system (binary, octal, decimal, hexadecimal)
            to_system: Target system
            
        Returns:
            Dictionary with conversion result
        """
        from_system = from_system.lower()
        to_system = to_system.lower()
        
        if from_system not in NumberSystemConverter.SYSTEMS:
            raise ValidationException(f"Unsupported source system: {from_system}")
        
        if to_system not in NumberSystemConverter.SYSTEMS:
            raise ValidationException(f"Unsupported target system: {to_system}")
        
        try:
            # Convert to decimal first
            from_base = NumberSystemConverter.SYSTEMS[from_system]
            decimal_value = int(number, from_base)
            
            # Convert to target system
            to_base = NumberSystemConverter.SYSTEMS[to_system]
            
            if to_system == "binary":
                result = bin(decimal_value)[2:]  # Remove '0b' prefix
            elif to_system == "octal":
                result = oct(decimal_value)[2:]  # Remove '0o' prefix
            elif to_system == "decimal":
                result = str(decimal_value)
            elif to_system == "hexadecimal":
                result = hex(decimal_value)[2:].upper()  # Remove '0x' prefix
            
            return {
                "original_number": number,
                "original_system": from_system,
                "converted_number": result,
                "converted_system": to_system,
                "decimal_value": decimal_value
            }
            
        except ValueError as e:
            raise ValidationException(f"Invalid number for base {from_system}: {str(e)}")
        except Exception as e:
            raise ProcessingException(f"Conversion failed: {str(e)}")


class ColorCodeConverter:
    """Convert between color code formats"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple:
        """Convert HEX to RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            raise ValidationException("HEX color must be 6 characters")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB to HEX"""
        if not all(0 <= c <= 255 for c in [r, g, b]):
            raise ValidationException("RGB values must be between 0 and 255")
        return f"#{r:02x}{g:02x}{b:02x}".upper()
    
    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
        """Convert RGB to HSL"""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        l = (max_c + min_c) / 2.0
        
        if max_c == min_c:
            h = s = 0.0
        else:
            d = max_c - min_c
            s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
            
            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        
        return (int(h * 360), int(s * 100), int(l * 100))
    
    @staticmethod
    def rgb_to_cmyk(r: int, g: int, b: int) -> tuple:
        """Convert RGB to CMYK"""
        if not all(0 <= c <= 255 for c in [r, g, b]):
            raise ValidationException("RGB values must be between 0 and 255")
        
        if r == 0 and g == 0 and b == 0:
            return (0, 0, 0, 100)
        
        c = 1 - r / 255.0
        m = 1 - g / 255.0
        y = 1 - b / 255.0
        k = min(c, m, y)
        
        c = int(((c - k) / (1 - k)) * 100)
        m = int(((m - k) / (1 - k)) * 100)
        y = int(((y - k) / (1 - k)) * 100)
        k = int(k * 100)
        
        return (c, m, y, k)
    
    @staticmethod
    def convert(color_value: str, from_format: str, to_format: str = None) -> Dict[str, Any]:
        """
        Convert color codes
        
        Args:
            color_value: Color value (HEX, RGB as "r,g,b")
            from_format: Source format (hex, rgb)
            to_format: Target format (if None, returns all formats)
            
        Returns:
            Dictionary with color in various formats
        """
        from_format = from_format.lower()
        
        try:
            # Parse input
            if from_format == "hex":
                r, g, b = ColorCodeConverter.hex_to_rgb(color_value)
            elif from_format == "rgb":
                parts = [int(x.strip()) for x in color_value.split(',')]
                if len(parts) != 3:
                    raise ValidationException("RGB format must be 'r,g,b'")
                r, g, b = parts
            else:
                raise ValidationException(f"Unsupported source format: {from_format}")
            
            # Generate all formats
            hex_color = ColorCodeConverter.rgb_to_hex(r, g, b)
            h, s, l = ColorCodeConverter.rgb_to_hsl(r, g, b)
            c, m, y, k = ColorCodeConverter.rgb_to_cmyk(r, g, b)
            
            result = {
                "hex": hex_color,
                "rgb": f"rgb({r}, {g}, {b})",
                "hsl": f"hsl({h}, {s}%, {l}%)",
                "cmyk": f"cmyk({c}%, {m}%, {y}%, {k}%)",
                "rgb_values": {"r": r, "g": g, "b": b},
                "hsl_values": {"h": h, "s": s, "l": l},
                "cmyk_values": {"c": c, "m": m, "y": y, "k": k}
            }
            
            if to_format:
                to_format = to_format.lower()
                if to_format not in result:
                    raise ValidationException(f"Unsupported target format: {to_format}")
            
            return result
            
        except Exception as e:
            if isinstance(e, (ValidationException, ProcessingException)):
                raise
            raise ProcessingException(f"Color conversion failed: {str(e)}")


class PercentageCalculator:
    """Calculate percentages"""
    
    @staticmethod
    def calculate(calculation_type: str, **kwargs) -> Dict[str, Any]:
        """
        Calculate percentage
        
        Args:
            calculation_type: Type of calculation (percentage_of, increase, decrease, change)
            **kwargs: Values needed for calculation
            
        Returns:
            Dictionary with calculation result
        """
        calc_type = calculation_type.lower()
        
        try:
            if calc_type == "percentage_of":
                # What is X% of Y?
                percentage = kwargs.get('percentage', 0)
                total = kwargs.get('total', 0)
                result = (percentage / 100) * total
                
                return {
                    "type": "percentage_of",
                    "percentage": percentage,
                    "total": total,
                    "result": round(result, 2),
                    "formula": f"{percentage}% of {total} = {round(result, 2)}"
                }
            
            elif calc_type == "what_percent":
                # X is what % of Y?
                value = kwargs.get('value', 0)
                total = kwargs.get('total', 0)
                
                if total == 0:
                    raise ValidationException("Total cannot be zero")
                
                percentage = (value / total) * 100
                
                return {
                    "type": "what_percent",
                    "value": value,
                    "total": total,
                    "percentage": round(percentage, 2),
                    "formula": f"{value} is {round(percentage, 2)}% of {total}"
                }
            
            elif calc_type == "increase":
                # Increase X by Y%
                value = kwargs.get('value', 0)
                percentage = kwargs.get('percentage', 0)
                increase = (percentage / 100) * value
                result = value + increase
                
                return {
                    "type": "increase",
                    "original_value": value,
                    "percentage": percentage,
                    "increase_amount": round(increase, 2),
                    "result": round(result, 2),
                    "formula": f"{value} + {percentage}% = {round(result, 2)}"
                }
            
            elif calc_type == "decrease":
                # Decrease X by Y%
                value = kwargs.get('value', 0)
                percentage = kwargs.get('percentage', 0)
                decrease = (percentage / 100) * value
                result = value - decrease
                
                return {
                    "type": "decrease",
                    "original_value": value,
                    "percentage": percentage,
                    "decrease_amount": round(decrease, 2),
                    "result": round(result, 2),
                    "formula": f"{value} - {percentage}% = {round(result, 2)}"
                }
            
            elif calc_type == "change":
                # Percentage change from X to Y
                old_value = kwargs.get('old_value', 0)
                new_value = kwargs.get('new_value', 0)
                
                if old_value == 0:
                    raise ValidationException("Old value cannot be zero")
                
                change = ((new_value - old_value) / old_value) * 100
                
                return {
                    "type": "percentage_change",
                    "old_value": old_value,
                    "new_value": new_value,
                    "change_percentage": round(change, 2),
                    "direction": "increase" if change > 0 else "decrease",
                    "formula": f"Change from {old_value} to {new_value} = {round(change, 2)}%"
                }
            
            else:
                raise ValidationException(f"Unsupported calculation type: {calculation_type}")
                
        except ZeroDivisionError:
            raise ValidationException("Division by zero error")
        except Exception as e:
            if isinstance(e, (ValidationException, ProcessingException)):
                raise
            raise ProcessingException(f"Calculation failed: {str(e)}")
