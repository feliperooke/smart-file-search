from .schemas import FileUploadResponse
from .s3_client import S3Client
from fastapi import UploadFile

class FileUploadService:
    def __init__(self, s3_client: S3Client):
        self.s3_client = s3_client

    async def upload(self, file: UploadFile) -> FileUploadResponse:
        file_url = await self.s3_client.upload_file(file.file, file.filename)
        return FileUploadResponse(
            filename=file.filename,
            url=file_url,
            content=""
        )
