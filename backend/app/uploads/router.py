from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends
from .service import FileUploadService
from .dependencies import get_upload_service
import uuid

router = APIRouter(prefix="/uploads")

class UploadRouter:
    def __init__(self):
        self.router = router

    def register_routes(self):
        @self.router.post("/", response_model=dict)
        async def upload(
            upload_service: Annotated[FileUploadService, Depends(get_upload_service)],
            file: UploadFile = File(...)
        ):
            file_id = str(uuid.uuid4())
            response = await upload_service.upload(file, file_id)
            return response.model_dump()

upload_router = UploadRouter()
upload_router.register_routes()
