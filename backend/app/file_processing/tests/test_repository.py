import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, UTC
from app.file_processing.repository import FileProcessingRepository
from app.file_processing.models import FileProcessingRecord

@pytest.fixture
def mock_file_record():
    """Create a mock FileProcessingRecord for testing"""
    return FileProcessingRecord(
        pk="file123",
        file_name="test.pdf",
        file_url="https://example.com/test.pdf",
        file_size=1024,
        file_type="application/pdf",
        markdown_content="# Test Document\n\nThis is a test document.",
        processing_status="pending",
        embedding_status="pending",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        history=None,
        metadata={"pages": 5, "title": "Test Document"}
    )

@pytest.mark.asyncio
@patch("app.infrastructure.dynamodb.repository.DynamoDBRepository.put_item")
async def test_put_item_adds_history_entry(mock_put_item, mock_file_record):
    """Test that put_item adds a history entry for the processing_status"""
    # Configure the mock
    mock_put_item.return_value = {"pk": "file123"}
    
    # Call the method
    result = await FileProcessingRepository.put_item(mock_file_record)
    
    # Verify that updated_at was updated
    assert mock_file_record.updated_at.date() == datetime.now(UTC).date()
    
    # Verify that history was created and has an entry for the processing_status
    assert mock_file_record.history is not None
    assert len(mock_file_record.history) == 1
    assert "pending" in mock_file_record.history[0]
    
    # Verify that the parent method was called
    mock_put_item.assert_called_once_with(mock_file_record)
    
    # Verify the result
    assert result == {"pk": "file123"}

@pytest.mark.asyncio
@patch("app.infrastructure.dynamodb.repository.DynamoDBRepository.put_item")
async def test_put_item_with_existing_history(mock_put_item, mock_file_record):
    """Test put_item with an existing history"""
    # Add an existing history entry
    mock_file_record.history = [{"started": "2023-04-01T12:00:00"}]
    mock_file_record.processing_status = "processing"
    
    # Configure the mock
    mock_put_item.return_value = {"pk": "file123"}
    
    # Call the method
    result = await FileProcessingRepository.put_item(mock_file_record)
    
    # Verify that history was updated
    assert len(mock_file_record.history) == 2
    assert "started" in mock_file_record.history[0]
    assert "processing" in mock_file_record.history[1]
    
    # Verify that the parent method was called
    mock_put_item.assert_called_once_with(mock_file_record)

@pytest.mark.asyncio
@patch("app.infrastructure.dynamodb.repository.DynamoDBRepository.put_item")
async def test_put_item_with_same_status(mock_put_item, mock_file_record):
    """Test put_item with the same processing status in history"""
    # Add an existing history entry with the same status
    timestamp = datetime.now(UTC).isoformat()
    mock_file_record.history = [{"pending": timestamp}]
    mock_file_record.processing_status = "pending"
    
    # Configure the mock
    mock_put_item.return_value = {"pk": "file123"}
    
    # Call the method
    result = await FileProcessingRepository.put_item(mock_file_record)
    
    # Verify that history wasn't updated with a duplicate entry
    assert len(mock_file_record.history) == 1
    assert "pending" in mock_file_record.history[0]
    
    # Verify that the parent method was called
    mock_put_item.assert_called_once_with(mock_file_record)

@pytest.mark.asyncio
@patch("app.infrastructure.dynamodb.repository.DynamoDBRepository.put_item")
async def test_put_item_with_empty_processing_status(mock_put_item):
    """Test put_item with an empty processing_status string"""
    # Create a record with empty processing_status
    record = FileProcessingRecord(
        pk="file123",
        file_name="test.pdf",
        file_url="https://example.com/test.pdf",
        file_size=1024,
        file_type="application/pdf",
        markdown_content="# Test Document\n\nThis is a test document.",
        processing_status="",  # Empty status
        embedding_status="pending",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        history=[],
        metadata={"pages": 5, "title": "Test Document"}
    )
    
    # Configure the mock
    mock_put_item.return_value = {"pk": "file123"}
    
    # Call the method
    result = await FileProcessingRepository.put_item(record)
    
    # Verify that history wasn't updated because processing_status is empty
    assert record.history == []
    
    # Verify that the parent method was called
    mock_put_item.assert_called_once_with(record)

@pytest.mark.asyncio
@patch("app.infrastructure.dynamodb.repository.DynamoDBRepository.get_item")
async def test_get_item(mock_get_item):
    """Test that get_item calls the parent method correctly"""
    # Configure the mock
    mock_get_item.return_value = FileProcessingRecord(
        pk="file123",
        file_name="test.pdf",
        file_url="https://example.com/test.pdf",
        file_size=1024,
        file_type="application/pdf",
        markdown_content="# Test Document\n\nThis is a test document.",
        processing_status="completed",
        embedding_status="completed",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        history=[{"started": "2023-04-01T12:00:00"}, {"completed": "2023-04-01T12:05:00"}],
        metadata={"pages": 5, "title": "Test Document"}
    )
    
    # Call the method
    result = await FileProcessingRepository.get_item({"pk": "file123"}, FileProcessingRecord)
    
    # Verify that the parent method was called
    mock_get_item.assert_called_once_with({"pk": "file123"}, FileProcessingRecord)
    
    # Verify the result
    assert result.pk == "file123"
    assert result.processing_status == "completed"
    assert len(result.history) == 2

@pytest.mark.asyncio
@patch("app.infrastructure.dynamodb.repository.DynamoDBRepository.query")
async def test_query(mock_query):
    """Test that query calls the parent method correctly"""
    # Configure the mock
    mock_query.return_value = [
        FileProcessingRecord(
            pk="file123",
            file_name="test1.pdf",
            file_url="https://example.com/test1.pdf",
            file_size=1024,
            file_type="application/pdf",
            markdown_content="# Test Document 1",
            processing_status="completed",
            embedding_status="completed",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            history=[],
            metadata={}
        ),
        FileProcessingRecord(
            pk="file456",
            file_name="test2.pdf",
            file_url="https://example.com/test2.pdf",
            file_size=2048,
            file_type="application/pdf",
            markdown_content="# Test Document 2",
            processing_status="completed",
            embedding_status="completed",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            history=[],
            metadata={}
        )
    ]
    
    # Call the method
    result = await FileProcessingRepository.query(
        key_condition_expression="begins_with(pk, :prefix)",
        expression_attribute_values={":prefix": "file"},
        model_class=FileProcessingRecord
    )
    
    # Verify that the parent method was called
    mock_query.assert_called_once_with(
        key_condition_expression="begins_with(pk, :prefix)",
        expression_attribute_values={":prefix": "file"},
        model_class=FileProcessingRecord
    )
    
    # Verify the result
    assert len(result) == 2
    assert result[0].pk == "file123"
    assert result[1].pk == "file456"

@pytest.mark.asyncio
@patch("app.infrastructure.dynamodb.repository.DynamoDBRepository.delete_item")
async def test_delete_item(mock_delete_item):
    """Test that delete_item calls the parent method correctly"""
    # Configure the mock
    mock_delete_item.return_value = {"pk": "file123"}
    
    # Call the method
    result = await FileProcessingRepository.delete_item({"pk": "file123"})
    
    # Verify that the parent method was called
    mock_delete_item.assert_called_once_with({"pk": "file123"})
    
    # Verify the result
    assert result == {"pk": "file123"} 