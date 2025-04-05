from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends
from .service import FileProcessorService
from .dependencies import get_file_processor_service

router = APIRouter(prefix="/process")

class FileProcessorRouter:
    def __init__(self):
        self.router = router

    def register_routes(self):
        @self.router.post("/", response_model=dict)
        async def process_file(
            processor_service: Annotated[FileProcessorService, Depends(get_file_processor_service)],
            file: UploadFile = File(...)
        ):
            response = await processor_service.process_and_upload(file)
            return response.model_dump()

file_processor_router = FileProcessorRouter()
file_processor_router.register_routes() 