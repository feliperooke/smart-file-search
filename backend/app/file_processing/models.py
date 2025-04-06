"""
File processing models.
"""
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, field_serializer

class FileProcessingRecord(BaseModel):
    """
    Model representing a file processing record in DynamoDB.
    """
    pk: str = Field(..., description="Unique identifier for the file processing record")
    file_name: str = Field(..., description="Original file name")
    file_url: str = Field(..., description="Url of the file in S3")
    file_size: int = Field(..., description="Size of the file in bytes")
    file_type: str = Field(..., description="MIME type of the file")
    markdown_content: str = Field(..., description="Text content of the file in markdown format")
    processing_status: str = Field(..., description="Status of the file processing")
    embedding_status: str = Field(..., description="Status of the embedding process")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the record was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the record was last updated")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata about the file")
    history: Optional[list[dict[str, Union[str, datetime]]]] = Field(
        default_factory=list,
        description="List of processing status changes with timestamps"
    )

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime, _info):
        """
        Serialize datetime fields to ISO 8601 format.
        
        Args:
            dt: The datetime object to serialize
            _info: Serialization info
            
        Returns:
            ISO 8601 formatted string
        """
        return dt.isoformat() if dt else None

    class Config:
        """
        Pydantic model configuration.
        
        - from_attributes: Allows creating the model from class attributes (like SQLAlchemy)
        - validate_assignment: Validates values during assignment (model.field = value)
        - json_encoders: Customizes serialization of specific types
        - json_schema_extra: Provides example data for documentation
        """
        from_attributes = True  # Allows creating the model from ORMs
        validate_assignment = True  # Validates data during assignment
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Customizes datetime serialization
        }
        json_schema_extra = {
            "example": {
                "pk": "123e4567-e89b-12d3-a456-426614174000",
                "file_name": "example.md",
                "file_url": "https://bucket.s3.amazonaws.com/documents/example.md",
                "file_size": 1024,
                "file_type": "text/markdown",
                "markdown_content": "# Example Document\n\nThis is a sample markdown content.",
                "processing_status": "completed",
                "embedding_status": "pending",
                "created_at": "2024-04-06T12:00:00Z",
                "updated_at": "2024-04-06T12:00:00Z",
                "error_message": None,
                "metadata": {
                    "word_count": 150,
                    "reading_time": "2 min",
                    "author": "John Doe"
                },
                "history": {
                    "pending_to_processing": "2024-04-06T12:00:00Z",
                    "processing_to_completed": "2024-04-06T12:01:00Z",
                }
            }
        } 