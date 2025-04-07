import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from datetime import datetime
from app.chat.router import ChatRouter, ChatRequest, ChatResponse, ChatHistoryResponse
from app.chat.models import ChatHistory

@pytest.fixture
def mock_chat_service():
    """Create a mock chat service"""
    service = AsyncMock()
    return service

@pytest.fixture
def chat_router(mock_chat_service):
    """Create a ChatRouter with the mock service injected"""
    router = ChatRouter()
    # Replace the service with our mock
    router.service = mock_chat_service
    return router

@pytest.fixture
def test_app(chat_router):
    """Create a test FastAPI app with the chat router that has a mocked service."""
    app = FastAPI()
    app.include_router(chat_router.router)
    return app

@pytest.fixture
def client(test_app):
    """Create a test client for the test app."""
    return TestClient(test_app)

def test_chat_router_initialization():
    """Test the initialization of the ChatRouter"""
    router = ChatRouter()
    
    assert router.router is not None
    assert router.service is not None

@pytest.mark.asyncio
async def test_chat_with_file(client, mock_chat_service):
    """Test the chat_with_file endpoint"""
    # Configure the mock service
    mock_chat_service.process_chat_query.return_value = "This is an AI response"
    
    # Make the request
    response = client.post("/chat/", json={
        "pk": "file123",
        "search": "Tell me about this document"
    })
    
    # Check the response
    assert response.status_code == 200
    assert response.json() == {"content": "This is an AI response"}
    
    # Verify the service was called correctly
    mock_chat_service.process_chat_query.assert_called_once_with(
        "file123", "Tell me about this document"
    )

@pytest.mark.asyncio
async def test_chat_with_file_not_found(client, mock_chat_service):
    """Test the chat_with_file endpoint when file is not found"""
    # Configure the mock service to raise an error
    mock_chat_service.process_chat_query.side_effect = ValueError("File with ID file123 not found")
    
    # Make the request
    response = client.post("/chat/", json={
        "pk": "file123",
        "search": "Tell me about this document"
    })
    
    # Check the response
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_chat_with_file_validation_error(client, mock_chat_service):
    """Test the chat_with_file endpoint with validation error"""
    # Configure the mock service to raise an error
    mock_chat_service.process_chat_query.side_effect = ValueError("File is not ready")
    
    # Make the request
    response = client.post("/chat/", json={
        "pk": "file123",
        "search": "Tell me about this document"
    })
    
    # Check the response
    assert response.status_code == 400
    assert "not ready" in response.json()["detail"]

@pytest.mark.asyncio
async def test_chat_with_file_server_error(client, mock_chat_service):
    """Test the chat_with_file endpoint with server error"""
    # Configure the mock service to raise an unexpected error
    mock_chat_service.process_chat_query.side_effect = Exception("Internal server error")
    
    # Make the request
    response = client.post("/chat/", json={
        "pk": "file123",
        "search": "Tell me about this document"
    })
    
    # Check the response
    assert response.status_code == 500
    assert "Error processing chat request" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_chat_history(client, mock_chat_service):
    """Test the get_chat_history endpoint"""
    # Create mock data
    now = datetime.utcnow()
    mock_file_record = MagicMock()
    mock_file_record.pk = "file123"
    
    mock_history = [
        ChatHistory(
            pk=f"file123:{now.isoformat()}",
            file_id="file123",
            query="What is this document about?",
            response="This document is about testing.",
            created_at=now,
            metadata={"source": "user"}
        )
    ]
    
    # Configure the mock service
    mock_chat_service.get_file_by_id.return_value = mock_file_record
    mock_chat_service.get_chat_history.return_value = mock_history
    
    # Make the request
    response = client.get("/chat/history/file123?limit=5")
    
    # Check the response
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 1
    assert result[0]["file_id"] == "file123"
    assert result[0]["query"] == "What is this document about?"
    assert result[0]["response"] == "This document is about testing."
    assert result[0]["metadata"] == {"source": "user"}
    
    # Verify the service was called correctly
    mock_chat_service.get_file_by_id.assert_called_once_with("file123")
    mock_chat_service.get_chat_history.assert_called_once_with("file123", 5)

@pytest.mark.asyncio
async def test_get_chat_history_file_not_found(client, mock_chat_service):
    """Test the get_chat_history endpoint when file is not found"""
    # Configure the mock service
    mock_chat_service.get_file_by_id.return_value = None
    
    # Make the request
    response = client.get("/chat/history/file123")
    
    # Check the response
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
    
    # Verify the service was called correctly
    mock_chat_service.get_file_by_id.assert_called_once_with("file123")
    mock_chat_service.get_chat_history.assert_not_called()

@pytest.mark.asyncio
async def test_get_chat_history_server_error(client, mock_chat_service):
    """Test the get_chat_history endpoint with server error"""
    # Configure the mock service
    mock_file_record = MagicMock()
    mock_file_record.pk = "file123"
    mock_chat_service.get_file_by_id.return_value = mock_file_record
    mock_chat_service.get_chat_history.side_effect = Exception("Database error")
    
    # Make the request
    response = client.get("/chat/history/file123")
    
    # Check the response
    assert response.status_code == 500
    assert "Error fetching chat history" in response.json()["detail"] 