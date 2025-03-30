from fastapi import APIRouter, UploadFile, File
from .service import FileUploadService

router = APIRouter(prefix="/uploads")

class UploadRouter:
    def __init__(self):
        self.upload_service = FileUploadService()

    def register_routes(self, router: APIRouter):
        @router.post("/", response_model=dict)
        async def upload(file: UploadFile = File(...)):
            response = self.upload_service.upload(file)
            return response.dict()

upload_router = UploadRouter()
upload_router.register_routes(router)
