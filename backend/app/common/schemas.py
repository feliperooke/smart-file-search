from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class FileDTO(BaseModel):
    pk: str
    filename: str
    url: str
    content: str
    file_size: int
    file_type: str
    markdown_content: str
    processing_status: str
    embedding_status: str
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
    metadata: Dict
    history: Dict[str, str] 