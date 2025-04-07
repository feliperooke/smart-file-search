import pytest
from datetime import datetime, UTC
from app.file_exploration.strategies.basic_explorer import BasicExplorer
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

def test_basic_explorer_initialization():
    """Test that BasicExplorer can be initialized"""
    explorer = BasicExplorer()
    assert explorer is not None

def test_basic_explorer_explore(mock_file_dto):
    """Test that explore method returns the file content"""
    explorer = BasicExplorer()
    
    # Call the explore method
    result = explorer.explore("Any search query", mock_file_dto)
    
    # Verify that it returns the content from the DTO
    assert result == mock_file_dto.content 