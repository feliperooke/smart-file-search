from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import pytest

client = TestClient(app)

@pytest.fixture
def mock_s3_upload():
    with patch("app.uploads.s3_client.S3Client.upload_file") as mock_upload:
        mock_upload.return_value = "https://mocked-s3-url.com/example.pdf"
        yield mock_upload

def test_upload_file(mock_s3_upload):
    response = client.post(
        "/api/uploads/",
        files={"file": ("example.pdf", b"dummy content", "application/pdf")}
    )

    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["filename"] == "example.pdf"
    assert json_resp["url"] == "https://mocked-s3-url.com/example.pdf"
