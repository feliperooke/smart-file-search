import pytest
from unittest.mock import MagicMock
from datetime import datetime, UTC
from app.file_exploration.service import FileExplorationService
from app.file_exploration.file_explorer import FileExplorer
from app.file_exploration.strategies.gemini_explorer import GeminiExplorer
from app.common.schemas import FileDTO

@pytest.fixture
def mock_file_dto():
    """Create a mock FileDTO for testing"""
    return FileDTO(
        pk="file123",
        filename="test.pdf",
        url="https://example.com/test.pdf",
        content="Test content",
        markdown_content="# Test Document\n\nThis is a test document.",
        file_size=1024,
        file_type="application/pdf",
        processing_status="completed",
        embedding_status="completed",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        metadata={},
        history={}
    )

@pytest.fixture
def mock_explorer():
    """Create a mock explorer for testing"""
    explorer = MagicMock(spec=FileExplorer)
    explorer.explore.return_value = "Mock exploration result"
    return explorer

def test_service_initialization_with_custom_explorer(mock_explorer):
    """Test service initialization with a custom explorer"""
    service = FileExplorationService(explorer=mock_explorer)
    assert service.explorer == mock_explorer

def test_service_initialization_default():
    """Test service initialization with default explorer"""
    service = FileExplorationService()
    assert isinstance(service.explorer, GeminiExplorer)

def test_explore_method(mock_explorer, mock_file_dto):
    """Test that explore method calls the explorer with correct parameters"""
    service = FileExplorationService(explorer=mock_explorer)
    
    # Call the explore method
    result = service.explore("What is this document about?", mock_file_dto)
    
    # Verify the result
    assert result == "Mock exploration result"
    
    # Verify the mock was called correctly
    mock_explorer.explore.assert_called_once_with("What is this document about?", mock_file_dto) 