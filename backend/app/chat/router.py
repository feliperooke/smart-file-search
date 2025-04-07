from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
from .service import ChatService
from .models import ChatHistory

# Request and response models
class ChatRequest(BaseModel):
    pk: str
    search: str

class ChatResponse(BaseModel):
    content: str

class ChatHistoryResponse(BaseModel):
    pk: str
    file_id: str
    query: str
    response: str
    created_at: datetime
    metadata: Dict[str, Any] = {}

class ChatRouter:
    """
    Router for chat interactions with files.
    """
    
    def __init__(self):
        """
        Initialize the ChatRouter with a router and service.
        """
        self.router = APIRouter(prefix="/chat")
        self.service = ChatService()
        self.register_routes()
    
    def register_routes(self):
        """
        Register all routes for the chat router.
        """
        
        @self.router.post("/", response_model=ChatResponse)
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
            try:
                result = await self.service.process_chat_query(request.pk, request.search)
                return ChatResponse(content=result)
            except ValueError as e:
                # Handle expected errors with appropriate status codes
                if "not found" in str(e):
                    raise HTTPException(status_code=404, detail=str(e))
                else:
                    raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                # Handle unexpected errors
                raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")
        
        @self.router.get("/history/{file_id}", response_model=List[ChatHistoryResponse])
        async def get_chat_history(
            file_id: str, 
            limit: int = Query(10, description="Maximum number of history records to return")
        ) -> List[ChatHistoryResponse]:
            """
            Get chat history for a specific file.
            
            Args:
                file_id: The ID of the file
                limit: Maximum number of history records to return
                
            Returns:
                List of chat history records
                
            Raises:
                HTTPException: If there is an error fetching the history
            """
            try:
                # Check if file exists
                file_record = await self.service.get_file_by_id(file_id)
                if not file_record:
                    raise HTTPException(status_code=404, detail=f"File with ID {file_id} not found")
                
                # Get history
                history = await self.service.get_chat_history(file_id, limit)
                
                # Convert to response model
                return [
                    ChatHistoryResponse(
                        pk=item.pk,
                        file_id=item.file_id,
                        query=item.query,
                        response=item.response,
                        created_at=item.created_at,
                        metadata=item.metadata or {}
                    ) for item in history
                ]
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")

# Create router instance
router = ChatRouter().router 