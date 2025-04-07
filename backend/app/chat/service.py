from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from app.common.schemas import FileDTO
from app.file_processing.repository import FileProcessingRepository
from app.file_processing.models import FileProcessingRecord
from app.file_exploration.service import FileExplorationService
from app.infrastructure.dynamodb.repository import DynamoDBRepository
from .models import ChatHistory

logger = logging.getLogger(__name__)

class ChatService:
    """
    Service responsible for handling chat interactions with files.
    """
    
    def __init__(self):
        """
        Initialize the ChatService with required dependencies.
        """
        self.file_repository = FileProcessingRepository()
        self.file_exploration_service = FileExplorationService()
        self.dynamodb_repository = DynamoDBRepository()
    
    async def get_file_by_id(self, file_id: str) -> Optional[FileProcessingRecord]:
        """
        Retrieve a file record by its ID.
        
        Args:
            file_id: The unique identifier of the file
            
        Returns:
            FileProcessingRecord if found, None otherwise
        """
        logger.info(f"Retrieving file with ID: {file_id}")
        return await self.file_repository.get_item({"pk": file_id}, FileProcessingRecord)
    
    async def get_chat_history(self, file_id: str, limit: int = 10) -> List[ChatHistory]:
        """
        Get chat history for a specific file.
        
        Args:
            file_id: The ID of the file
            limit: Maximum number of history records to return
            
        Returns:
            List of ChatHistory records sorted by created_at (newest first)
        """
        # Query history using file_id as the beginning of the primary key
        try:
            history = await self.dynamodb_repository.query(
                key_condition_expression="begins_with(pk, :file_id)",
                expression_attribute_values={
                    ":file_id": f"{file_id}:"
                },
                limit=limit,
                model_class=ChatHistory
            )
            
            # Sort by created_at (newest first)
            history.sort(key=lambda x: x.created_at, reverse=True)
            
            return history
        except Exception as e:
            logger.error(f"Error fetching chat history: {str(e)}")
            return []
    
    def create_file_dto(self, file_record: FileProcessingRecord) -> FileDTO:
        """
        Convert a FileProcessingRecord to a FileDTO.
        
        Args:
            file_record: The file record to convert
            
        Returns:
            A FileDTO containing the file data
        """
        # Convert history list to dictionary format
        history_dict = {}
        if file_record.history:
            for entry in file_record.history:
                for status, timestamp in entry.items():
                    history_dict[status] = timestamp
        
        return FileDTO(
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
            history=history_dict
        )
    
    async def save_chat_history(self, file_id: str, query: str, response: str) -> ChatHistory:
        """
        Save a chat interaction to the history.
        
        Args:
            file_id: The ID of the file
            query: The search query
            response: The AI response
            
        Returns:
            The created ChatHistory record
        """
        now = datetime.utcnow()
        timestamp = now.isoformat()
        
        history = ChatHistory(
            pk=f"{file_id}:{timestamp}",
            file_id=file_id,
            query=query,
            response=response,
            created_at=now,
            metadata={
                "timestamp": timestamp
            }
        )
        
        # Save to repository
        await self.dynamodb_repository.put_item(history)
        logger.info(f"Saved chat history for file {file_id}")
        
        return history
    
    async def process_chat_query(self, file_id: str, search_query: str) -> str:
        """
        Process a chat query for a specific file.
        
        Args:
            file_id: The ID of the file to chat with
            search_query: The query or instructions for the chat
            
        Returns:
            The AI's response to the query
            
        Raises:
            ValueError: If the file is not found or not ready
        """
        # Get the file record
        file_record = await self.get_file_by_id(file_id)
        if not file_record:
            raise ValueError(f"File with ID {file_id} not found")
        
        # Check if the file is ready
        if file_record.processing_status != "completed":
            raise ValueError(
                f"File processing is not complete. Current status: {file_record.processing_status}"
            )
        
        # Convert to DTO and process
        file_dto = self.create_file_dto(file_record)
        logger.info(f"Processing chat query for file: {file_record.file_name}")
        
        # Get response from AI
        response = self.file_exploration_service.explore(search_query, file_dto)
        
        # Save chat history (don't wait for this to complete)
        try:
            await self.save_chat_history(file_id, search_query, response)
        except Exception as e:
            logger.error(f"Error saving chat history: {str(e)}")
        
        return response 