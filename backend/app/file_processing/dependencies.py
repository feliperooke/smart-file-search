from typing import Annotated
from fastapi import Depends
from app.text_extraction.service import TextExtractionService
from app.uploads.service import FileUploadService
from app.uploads.dependencies import get_upload_service
from .service import FileProcessorService

def get_text_extraction_service() -> TextExtractionService:
    return TextExtractionService()

def get_file_processor_service(
    text_extraction_service: Annotated[TextExtractionService, Depends(get_text_extraction_service)],
    upload_service: Annotated[FileUploadService, Depends(get_upload_service)]
) -> FileProcessorService:
    return FileProcessorService(text_extraction_service, upload_service) 