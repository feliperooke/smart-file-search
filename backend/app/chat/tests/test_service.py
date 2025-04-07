import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
import json
from app.chat.service import ChatService
from app.chat.models import ChatHistory
from app.file_processing.models import FileProcessingRecord
from app.common.schemas import FileDTO

@pytest.fixture
def mock_file_record():
    """Mock file record for testing"""
    return FileProcessingRecord(
        pk="file123",
        file_name="test.pdf",
        file_url="https://example.com/test.pdf",
        file_size=1024,
        file_type="application/pdf",
        markdown_content="# Test Document\n\nThis is a test document.",
        processing_status="completed",
        embedding_status="completed",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        history=[{"started": "2023-04-01T12:00:00"}, {"completed": "2023-04-01T12:05:00"}],
        metadata={"pages": 5, "title": "Test Document"}
    )

@pytest.fixture
def mock_chat_history():
    """Mock chat history items"""
    now = datetime.utcnow()
    return [
        ChatHistory(
            pk=f"file123:{(now - timedelta(minutes=1)).isoformat()}",
            file_id="file123",
            query="What is the content?",
            response="The document contains test content.",
            created_at=now - timedelta(minutes=1)
        ),
        ChatHistory(
            pk=f"file123:{now.isoformat()}",
            file_id="file123",
            query="Tell me more",
            response="There is no more information available.",
            created_at=now
        )
    ]

@pytest.fixture
def chat_service():
    """Fixture for chat service with mocked dependencies"""
    service = ChatService()
    service.file_repository = AsyncMock()
    service.dynamodb_repository = AsyncMock()
    service.file_exploration_service = MagicMock()
    return service

@pytest.mark.asyncio
async def test_get_file_by_id(chat_service, mock_file_record):
    """Test retrieving a file by ID"""
    # Configure mock
    chat_service.file_repository.get_item.return_value = mock_file_record
    
    # Call method
    result = await chat_service.get_file_by_id("file123")
    
    # Verify
    assert result == mock_file_record
    chat_service.file_repository.get_item.assert_called_once_with(
        {"pk": "file123"}, FileProcessingRecord
    )

@pytest.mark.asyncio
async def test_get_file_by_id_not_found(chat_service):
    """Test retrieving a file that doesn't exist"""
    # Configure mock
    chat_service.file_repository.get_item.return_value = None
    
    # Call method
    result = await chat_service.get_file_by_id("file123")
    
    # Verify
    assert result is None

@pytest.mark.asyncio
async def test_get_chat_history(chat_service, mock_chat_history):
    """Test retrieving chat history"""
    # Configure mock
    now = datetime.utcnow()
    chat_service.dynamodb_repository.query.return_value = mock_chat_history
    
    # Call method
    result = await chat_service.get_chat_history("file123", limit=5)
    
    # Verify
    assert result == mock_chat_history
    chat_service.dynamodb_repository.query.assert_called_once_with(
        key_condition_expression="begins_with(pk, :file_id)",
        expression_attribute_values={
            ":file_id": "file123:"
        },
        limit=5,
        model_class=ChatHistory
    )

@pytest.mark.asyncio
async def test_get_chat_history_error(chat_service):
    """Test error handling in get_chat_history"""
    # Configure mock to raise exception
    chat_service.dynamodb_repository.query.side_effect = Exception("Database error")
    
    # Call method
    result = await chat_service.get_chat_history("file123")
    
    # Verify empty list is returned instead of exception
    assert result == []

@pytest.mark.asyncio
async def test_save_chat_history(chat_service):
    """Test saving chat history"""
    # Configure mock
    chat_service.dynamodb_repository.put_item.return_value = None
    
    # Call method
    result = await chat_service.save_chat_history(
        "file123",
        "What is this document about?",
        "This document is about testing."
    )
    
    # Verify
    assert isinstance(result, ChatHistory)
    assert result.file_id == "file123"
    assert result.query == "What is this document about?"
    assert result.response == "This document is about testing."
    assert isinstance(result.created_at, datetime)
    assert "timestamp" in result.metadata
    chat_service.dynamodb_repository.put_item.assert_called_once()

def test_create_file_dto(chat_service, mock_file_record):
    """Test converting a file record to DTO"""
    # Call method
    dto = chat_service.create_file_dto(mock_file_record)
    
    # Verify
    assert dto.pk == mock_file_record.pk
    assert dto.filename == mock_file_record.file_name
    assert dto.url == mock_file_record.file_url
    assert dto.content == mock_file_record.markdown_content
    assert dto.file_size == mock_file_record.file_size
    assert dto.file_type == mock_file_record.file_type
    assert dto.processing_status == mock_file_record.processing_status
    assert dto.embedding_status == mock_file_record.embedding_status
    assert dto.created_at == mock_file_record.created_at
    assert dto.updated_at == mock_file_record.updated_at
    assert dto.metadata == mock_file_record.metadata
    assert "started" in dto.history
    assert "completed" in dto.history

@pytest.mark.asyncio
async def test_process_chat_query(chat_service, mock_file_record):
    """Test processing a chat query"""
    # Configure mocks
    chat_service.file_repository.get_item.return_value = mock_file_record
    chat_service.file_exploration_service.explore.return_value = "AI generated response"
    chat_service.dynamodb_repository.put_item.return_value = None
    
    # Call method
    result = await chat_service.process_chat_query("file123", "What is this document about?")
    
    # Verify
    assert result == "AI generated response"
    chat_service.file_repository.get_item.assert_called_once()
    chat_service.file_exploration_service.explore.assert_called_once()
    chat_service.dynamodb_repository.put_item.assert_called_once()

@pytest.mark.asyncio
async def test_process_chat_query_file_not_found(chat_service):
    """Test processing a chat query when file is not found"""
    # Configure mock
    chat_service.file_repository.get_item.return_value = None
    
    # Call method and verify it raises ValueError
    with pytest.raises(ValueError, match="File with ID file123 not found"):
        await chat_service.process_chat_query("file123", "What is this document about?")

@pytest.mark.asyncio
async def test_process_chat_query_file_not_ready(chat_service, mock_file_record):
    """Test processing a chat query when file is not ready"""
    # Configure mock with incomplete status
    mock_file_record.processing_status = "processing"
    chat_service.file_repository.get_item.return_value = mock_file_record
    
    # Call method and verify it raises ValueError
    with pytest.raises(ValueError, match="File processing is not complete"):
        await chat_service.process_chat_query("file123", "What is this document about?")

@pytest.mark.asyncio
async def test_process_chat_query_history_error(chat_service, mock_file_record):
    """Test processing a chat query with history error"""
    # Configure mocks
    chat_service.file_repository.get_item.return_value = mock_file_record
    chat_service.file_exploration_service.explore.return_value = "AI generated response"
    chat_service.dynamodb_repository.put_item.side_effect = Exception("Database error")
    
    # Call method - should not raise the exception
    result = await chat_service.process_chat_query("file123", "What is this document about?")
    
    # Verify the response is still returned despite history error
    assert result == "AI generated response" 