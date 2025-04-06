"""
Repository for FileProcessingRecord operations.
"""
from typing import Dict, Any, Optional, List, TypeVar
from pydantic import BaseModel
from datetime import datetime
from app.infrastructure.dynamodb.repository import DynamoDBRepository
from app.file_processing.models import FileProcessingRecord


# Define T as FileProcessingRecord
T = TypeVar('T', bound=FileProcessingRecord)


class FileProcessingRepository(DynamoDBRepository):
    """
    Repository for FileProcessingRecord operations.
    Extends DynamoDBRepository with specific methods for file processing records.
    """
    
    @staticmethod
    async def put_item(item: FileProcessingRecord) -> Dict[str, Any]:
        """
        Put an item in the DynamoDB table.
        
        If the item has a processing_status, it will add a history entry.
        The updated_at field is automatically set to the current time.
        
        Args:
            item: FileProcessingRecord instance to save
            
        Returns:
            The response from DynamoDB
        """
        # Set updated_at to current time
        item.updated_at = datetime.utcnow()
        
        # Add a history entry for the processing_status
        if hasattr(item, "processing_status") and item.processing_status:
            # Initialize history if it doesn't exist
            if not item.history:
                item.history = []
            
            # if the last history entry is not the current processing_status, add a new entry
            if not item.history or not item.history[-1].get(item.processing_status):
                timestamp = datetime.utcnow().isoformat()
                item.history.append({
                    f"{item.processing_status}": timestamp
                })
        
        # Call the parent class method to save the item
        return await DynamoDBRepository.put_item(item) 