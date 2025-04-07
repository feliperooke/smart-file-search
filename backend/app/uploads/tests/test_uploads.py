from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from fastapi import UploadFile
from app.uploads.schemas import FileUploadResponse
from app.uploads.service import FileUploadService
from app.uploads.s3_client import S3Client
from botocore.exceptions import NoCredentialsError
from datetime import datetime
import uuid

client = TestClient(app)

@pytest.fixture
def mock_s3_upload():
    with patch("app.uploads.s3_client.S3Client.upload_file") as mock_upload:
        mock_upload.return_value = "https://mocked-s3-url.com/example.pdf"
        yield mock_upload

@pytest.fixture
def mock_file():
    mock = MagicMock(spec=UploadFile)
    mock.filename = "example.pdf"
    mock.file = MagicMock()
    mock.size = 13
    mock.content_type = "application/pdf"
    return mock

# Patcheamos o próprio serviço para não afetar outros testes
@pytest.fixture
def mock_upload_service():
    with patch("app.uploads.service.FileUploadService.upload") as mock_method:
        async def mock_implementation(*args, **kwargs):
            return FileUploadResponse(
                pk="test-id",
                filename="example.pdf",
                url="https://mocked-s3-url.com/example.pdf",
                content="",
                file_size=13,
                file_type="application/pdf",
                markdown_content="",
                processing_status="stored",
                embedding_status="pending",
                created_at=datetime.now().replace(microsecond=0),
                updated_at=datetime.now().replace(microsecond=0),
                metadata={},
                history={}
            )
        mock_method.side_effect = mock_implementation
        yield mock_method

def test_upload_file_without_file():
    response = client.post(
        "/api/uploads/",
        files={}
    )
    assert response.status_code == 422  # Validation error

def test_s3_client():
    # Testa a criação da classe
    s3_client = S3Client()
    assert s3_client is not None
    assert s3_client.client is None

def test_file_upload_service():
    # Testa a criação do serviço
    mock_s3_client = MagicMock()
    service = FileUploadService(s3_client=mock_s3_client)
    assert service is not None
    assert service.s3_client is mock_s3_client

def test_file_upload_response_schema():
    now = datetime.now().replace(microsecond=0)
    
    response = FileUploadResponse(
        pk="test-id",
        filename="test.pdf",
        url="https://test-bucket.s3.amazonaws.com/test.pdf",
        content="",
        file_size=1024,
        file_type="application/pdf",
        markdown_content="",
        processing_status="stored",
        embedding_status="pending",
        created_at=now,
        updated_at=now,
        metadata={},
        history={}
    )
    
    assert response.filename == "test.pdf"
    assert response.url == "https://test-bucket.s3.amazonaws.com/test.pdf"
    assert response.pk == "test-id"

@pytest.mark.asyncio
async def test_upload_method(mock_file):
    # Simula o S3Client
    mock_s3_client = AsyncMock()
    mock_s3_client.upload_file.return_value = "https://test-bucket.s3.amazonaws.com/test-id"
    
    # Cria o serviço com o mock
    service = FileUploadService(s3_client=mock_s3_client)
    
    # Testa o método upload
    file_id = "test-id"
    response = await service.upload(mock_file, file_id)
    
    # Verifica o resultado
    assert isinstance(response, FileUploadResponse)
    assert response.pk == file_id
    assert response.filename == mock_file.filename
    assert response.url == "https://test-bucket.s3.amazonaws.com/test-id"
    mock_s3_client.upload_file.assert_called_once_with(mock_file.file, file_id)
