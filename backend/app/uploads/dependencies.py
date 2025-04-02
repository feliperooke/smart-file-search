from typing import Annotated
from fastapi import Depends
from .service import FileUploadService
from .s3_client import S3Client

def get_upload_service(s3_client: Annotated[S3Client, Depends(S3Client)]) -> FileUploadService:
    return FileUploadService(s3_client) 