from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class ChatHistory(BaseModel):
    """
    Model representing a chat history entry in DynamoDB.
    """
    pk: str = Field(..., description="Primary key - composite of 'file_id:timestamp'")
    file_id: str = Field(..., description="ID of the file being chatted with")
    query: str = Field(..., description="Search query or instructions")
    response: str = Field(..., description="AI response to the query")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Time of chat interaction")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata about the chat") 