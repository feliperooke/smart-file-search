import aioboto3
from botocore.exceptions import NoCredentialsError
from app.core.config import settings

class S3Client:
    def __init__(self):
        self.session = aioboto3.Session()
        self.client = self.session.client("s3", region_name=settings.AWS_REGION)

    async def upload_file(self, file_obj, filename: str) -> str:
        try:
            async with self.client as s3:
                await s3.upload_fileobj(file_obj, settings.S3_BUCKET, filename)
            return f"https://{settings.S3_BUCKET}.s3.amazonaws.com/{filename}"
        except NoCredentialsError:
            raise RuntimeError("AWS credentials not found")
        except Exception as e:
            raise RuntimeError(f"S3 upload failed: {str(e)}")
