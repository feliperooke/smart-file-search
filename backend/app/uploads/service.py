from .schemas import FileUploadResponse
from .s3_client import S3Client
from fastapi import UploadFile
from datetime import datetime

class FileUploadService:
    def __init__(self, s3_client: S3Client):
        self.s3_client = s3_client

    async def upload(self, file: UploadFile, file_id: str) -> FileUploadResponse:
        file_url = await self.s3_client.upload_file(file.file, file_id)
        now = datetime.now().replace(microsecond=0)
        
        return FileUploadResponse(
            pk=file_id,
            filename=file.filename,
            url=file_url,
            content="",
            file_size=file.size,
            file_type=file.content_type,
            markdown_content="",
            processing_status="stored",
            embedding_status="pending",
            created_at=now,
            updated_at=now,
            error_message=None,
            metadata={},
            history={}
        )
