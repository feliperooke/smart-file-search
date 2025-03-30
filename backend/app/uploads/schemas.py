from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    filename: str
    url: str