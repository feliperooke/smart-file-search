import pytest
from datetime import datetime
from app.chat.models import ChatHistory

def test_chat_history_creation():
    """Test the creation of a ChatHistory model"""
    now = datetime.utcnow()
    
    chat_history = ChatHistory(
        pk="file123:20230401T120000",
        file_id="file123",
        query="What is this document about?",
        response="This document is about testing.",
        created_at=now
    )
    
    assert chat_history.pk == "file123:20230401T120000"
    assert chat_history.file_id == "file123"
    assert chat_history.query == "What is this document about?"
    assert chat_history.response == "This document is about testing."
    assert chat_history.created_at == now
    assert chat_history.metadata == {}

def test_chat_history_with_metadata():
    """Test the creation of a ChatHistory model with metadata"""
    now = datetime.utcnow()
    
    chat_history = ChatHistory(
        pk="file123:20230401T120000",
        file_id="file123",
        query="What is this document about?",
        response="This document is about testing.",
        created_at=now,
        metadata={"source": "user", "context": "test"}
    )
    
    assert chat_history.pk == "file123:20230401T120000"
    assert chat_history.file_id == "file123"
    assert chat_history.metadata["source"] == "user"
    assert chat_history.metadata["context"] == "test"

def test_chat_history_model_dump():
    """Test that the model can be serialized to a dictionary"""
    now = datetime.utcnow()
    
    chat_history = ChatHistory(
        pk="file123:20230401T120000",
        file_id="file123",
        query="What is this document about?",
        response="This document is about testing.",
        created_at=now,
        metadata={"source": "user"}
    )
    
    # Convert to dict
    model_dict = chat_history.model_dump()
    
    assert isinstance(model_dict, dict)
    assert model_dict["pk"] == "file123:20230401T120000"
    assert model_dict["file_id"] == "file123"
    assert model_dict["query"] == "What is this document about?"
    assert model_dict["response"] == "This document is about testing."
    assert model_dict["metadata"] == {"source": "user"} 