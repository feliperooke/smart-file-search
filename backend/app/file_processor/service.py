from fastapi import UploadFile
from app.text_extraction.service import TextExtractionService
from app.uploads.service import FileUploadService
from .schemas import FileProcessResponse

class FileProcessorService:
    def __init__(self, text_extraction_service: TextExtractionService, upload_service: FileUploadService):
        self.text_extraction_service = text_extraction_service
        self.upload_service = upload_service

    async def process_and_upload(self, file: UploadFile) -> FileProcessResponse:
        # Extract text from the file
        extracted_text = self.text_extraction_service.extract(file)
        
        # Reset file pointer for upload
        file.file.seek(0)
        
        # Upload the file
        upload_response = await self.upload_service.upload(file)
        
        # Create response with extracted text
        return FileProcessResponse(
            filename=upload_response.filename,
            url=upload_response.url,
            content=extracted_text
        ) 