import pytest
from abc import ABC
from app.file_exploration.file_explorer import FileExplorer
from app.common.schemas import FileDTO

def test_file_explorer_is_abstract():
    """Test that FileExplorer is an abstract class"""
    assert issubclass(FileExplorer, ABC)
    
    # Verify that we cannot instantiate it directly
    with pytest.raises(TypeError):
        FileExplorer() 