from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.common.schemas import FileDTO
from app.file_processing.repository import FileProcessingRepository
from app.file_processing.models import FileProcessingRecord
from app.file_exploration.service import FileExplorationService

# Initialize router
router = APIRouter(prefix="/chat")

# Initialize services
file_exploration_service = FileExplorationService()
file_repository = FileProcessingRepository()

# Request and response models
class ChatRequest(BaseModel):
    pk: str
    search: str

class ChatResponse(BaseModel):
    content: str
    
# Router definition
@router.post("/", response_model=ChatResponse)
async def chat_with_file(request: ChatRequest) -> ChatResponse:
    """
    Chat with a file using AI.
    
    Args:
        request: The chat request containing file PK and search query
        
    Returns:
        A response containing the AI's answer
        
    Raises:
        HTTPException: If the file is not found or there is an error
    """
    # Retrieve file data from the database
    file_record = await file_repository.get_item({"pk": request.pk}, FileProcessingRecord)
    
    if not file_record:
        raise HTTPException(status_code=404, detail=f"File with ID {request.pk} not found")
    
    if file_record.processing_status != "completed":
        raise HTTPException(
            status_code=400, 
            detail=f"File processing is not complete. Current status: {file_record.processing_status}"
        )
    
    # Convert to FileDTO for the explorer
    file_dto = FileDTO(
        pk=file_record.pk,
        filename=file_record.file_name,
        url=file_record.file_url,
        content=file_record.markdown_content,
        file_size=file_record.file_size,
        file_type=file_record.file_type,
        markdown_content=file_record.markdown_content,
        processing_status=file_record.processing_status,
        embedding_status=file_record.embedding_status,
        created_at=file_record.created_at,
        updated_at=file_record.updated_at,
        error_message=file_record.error_message,
        metadata=file_record.metadata or {},
        history={} if not file_record.history else {
            k: v for entry in file_record.history for k, v in entry.items()
        }
    )
    
    # Process the search query
    try:
        result = file_exploration_service.explore(request.search, file_dto)
        return ChatResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}") 