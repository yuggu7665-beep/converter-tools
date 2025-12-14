"""Custom exceptions for the application"""


class ConverterException(Exception):
    """Base exception for all converter errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(ConverterException):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class ProcessingException(ConverterException):
    """Raised when conversion processing fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class RateLimitException(ConverterException):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded. Please try again later."):
        super().__init__(message, status_code=429)


class FileSizeException(ConverterException):
    """Raised when uploaded file is too large"""
    def __init__(self, message: str = "File size exceeds maximum allowed size"):
        super().__init__(message, status_code=413)


class UnsupportedFormatException(ConverterException):
    """Raised when file format is not supported"""
    def __init__(self, message: str):
        super().__init__(message, status_code=415)
