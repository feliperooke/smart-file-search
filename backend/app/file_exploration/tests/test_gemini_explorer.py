import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, UTC
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
def mock_gemini_response():
    """Create a mock Gemini API response"""
    response = MagicMock()
    response.text = "This is a response from Gemini AI"
    return response

@pytest.fixture
def mock_gemini_model(mock_gemini_response):
    """Create a mock Gemini model"""
    model = MagicMock()
    model.generate_content.return_value = mock_gemini_response
    return model

@pytest.mark.parametrize("has_text_attr,has_parts_attr,expected_response", [
    (True, False, "This is a response from Gemini AI"),
    (False, True, "This is a response from Gemini AI"),
    (False, False, "Unable to process response from Gemini API")
])
def test_gemini_explorer_explore_response_types(
    mock_file_dto, 
    mock_gemini_model, 
    has_text_attr, 
    has_parts_attr, 
    expected_response
):
    """Test different response types from Gemini API"""
    # Configure the mock response based on the test parameters
    response = MagicMock()
    
    if has_text_attr:
        type(response).text = "This is a response from Gemini AI"
    else:
        # Delete text attribute if it exists
        if hasattr(response, "text"):
            delattr(response, "text")
    
    if has_parts_attr:
        part = MagicMock()
        part.text = "This is a response from Gemini AI"
        response.parts = [part]
    else:
        # Delete parts attribute if it exists
        if hasattr(response, "parts"):
            delattr(response, "parts")
    
    mock_gemini_model.generate_content.return_value = response
    
    # Create the explorer with the mock model
    with patch("google.generativeai.GenerativeModel", return_value=mock_gemini_model), \
         patch("google.generativeai.configure"):
        explorer = GeminiExplorer(api_key="fake_api_key")
        explorer.model = mock_gemini_model
        
        # Call the explore method
        result = explorer.explore("What is this document about?", mock_file_dto)
        
        # Verify the result
        assert result == expected_response
        
        # Verify the model was called with correct parameters
        mock_gemini_model.generate_content.assert_called_once()

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_gemini_explorer_initialization(mock_generative_model, mock_configure):
    """Test the initialization of GeminiExplorer"""
    # Create an instance with a custom API key
    explorer = GeminiExplorer(api_key="custom_api_key")
    
    # Verify that the API was configured with the key
    mock_configure.assert_called_once_with(api_key="custom_api_key")
    
    # Verify that the model was created
    mock_generative_model.assert_called_once_with("gemini-2.0-flash")
    
    # Verify the properties
    assert explorer.api_key == "custom_api_key"
    assert explorer.model_name == "gemini-2.0-flash"

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_gemini_explorer_custom_model(mock_generative_model, mock_configure):
    """Test the initialization with a custom model name"""
    # Create an instance with a custom model name
    explorer = GeminiExplorer(api_key="custom_api_key", model_name="custom-model")
    
    # Verify that the model was created with the custom name
    mock_generative_model.assert_called_once_with("custom-model")
    
    # Verify the properties
    assert explorer.model_name == "custom-model"

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_gemini_explorer_no_api_key(mock_generative_model, mock_configure):
    """Test that initialization fails without an API key"""
    # Attempt to create an instance without an API key
    with patch("app.infrastructure.config.settings.GOOGLE_API_KEY", None):
        with pytest.raises(ValueError, match="Google API key is required"):
            GeminiExplorer()

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_gemini_explorer_create_prompt(mock_generative_model, mock_configure, mock_file_dto):
    """Test the _create_prompt method"""
    # Create an instance
    explorer = GeminiExplorer(api_key="custom_api_key")
    
    # Call the _create_prompt method
    prompt = explorer._create_prompt("What is this document about?", mock_file_dto)
    
    # Verify that the prompt contains the search query and the content
    assert "What is this document about?" in prompt
    assert mock_file_dto.markdown_content in prompt

@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_gemini_explorer_error_handling(mock_generative_model, mock_configure, mock_file_dto):
    """Test error handling in explore method"""
    # Configure the mock model to raise an exception
    model_instance = MagicMock()
    model_instance.generate_content.side_effect = Exception("API error")
    mock_generative_model.return_value = model_instance
    
    # Create an instance
    explorer = GeminiExplorer(api_key="custom_api_key")
    
    # Call the explore method
    result = explorer.explore("What is this document about?", mock_file_dto)
    
    # Verify that an error message is returned
    assert "Error exploring content with Gemini" in result
    assert "API error" in result 