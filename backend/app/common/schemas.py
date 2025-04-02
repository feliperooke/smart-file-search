from pydantic import BaseModel

class FileResponse(BaseModel):
    filename: str
    url: str
    content: str 