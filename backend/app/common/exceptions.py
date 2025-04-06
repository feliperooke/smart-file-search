"""
Common exceptions used across the application.
"""

class FileProcessingError(Exception):
    """Base exception for file processing errors."""
    pass

class TextExtractionError(FileProcessingError):
    """Raised when text extraction fails."""
    pass

class FileUploadError(FileProcessingError):
    """Raised when file upload fails."""
    pass 