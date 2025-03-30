from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
import pytest
from fastapi import UploadFile
from app.uploads.schemas import FileUploadResponse
from app.uploads.service import FileUploadService
from app.uploads.s3_client import S3Client
from botocore.exceptions import NoCredentialsError

client = TestClient(app)

@pytest.fixture
def mock_s3_upload():
    with patch("app.uploads.s3_client.S3Client.upload_file") as mock_upload:
        mock_upload.return_value = "https://mocked-s3-url.com/example.pdf"
        yield mock_upload

@pytest.fixture
def mock_file():
    return MagicMock(spec=UploadFile)

def test_upload_file_success(mock_s3_upload, mock_file):
    mock_file.filename = "example.pdf"
    mock_file.file = MagicMock()
    
    response = client.post(
        "/api/uploads/",
        files={"file": ("example.pdf", b"dummy content", "application/pdf")}
    )

    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["filename"] == "example.pdf"
    assert json_resp["url"] == "https://mocked-s3-url.com/example.pdf"
    mock_s3_upload.assert_called_once()

def test_upload_file_without_file():
    response = client.post(
        "/api/uploads/",
        files={}
    )
    assert response.status_code == 422  # Validation error

def test_s3_client_upload_success():
    with patch("boto3.client") as mock_boto3:
        mock_client = MagicMock()
        mock_boto3.return_value = mock_client
        mock_client.upload_fileobj = MagicMock()
        
        s3_client = S3Client()
        response = s3_client.upload_file(MagicMock(), "test.pdf")
        assert response == "https://None.s3.amazonaws.com/test.pdf"

def test_s3_client_upload_error():
    with patch("boto3.client") as mock_boto3:
        mock_client = MagicMock()
        mock_boto3.return_value = mock_client
        mock_client.upload_fileobj.side_effect = Exception("S3 Error")
        
        s3_client = S3Client()
        with pytest.raises(RuntimeError) as exc_info:
            s3_client.upload_file(MagicMock(), "test.pdf")
        assert "S3 upload failed" in str(exc_info.value)

def test_s3_client_no_credentials():
    with patch("boto3.client") as mock_boto3:
        mock_client = MagicMock()
        mock_boto3.return_value = mock_client
        mock_client.upload_fileobj.side_effect = NoCredentialsError()
        
        s3_client = S3Client()
        with pytest.raises(RuntimeError) as exc_info:
            s3_client.upload_file(MagicMock(), "test.pdf")
        assert "AWS credentials not found" in str(exc_info.value)

def test_file_upload_service():
    service = FileUploadService()
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.file = MagicMock()
    
    with patch.object(service.s3_client, "upload_file") as mock_upload:
        mock_upload.return_value = "https://test-bucket.s3.amazonaws.com/test.pdf"
        
        response = service.upload(mock_file)
        assert isinstance(response, FileUploadResponse)
        assert response.filename == "test.pdf"
        assert response.url == "https://test-bucket.s3.amazonaws.com/test.pdf"
        mock_upload.assert_called_once_with(mock_file.file, "test.pdf")

def test_file_upload_response_schema():
    response = FileUploadResponse(
        filename="test.pdf",
        url="https://test-bucket.s3.amazonaws.com/test.pdf"
    )
    assert response.filename == "test.pdf"
    assert response.url == "https://test-bucket.s3.amazonaws.com/test.pdf"
    
    # Test schema validation
    with pytest.raises(ValueError):
        FileUploadResponse(filename=None, url="https://test.com")
