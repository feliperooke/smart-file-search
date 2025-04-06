import aioboto3
from botocore.exceptions import NoCredentialsError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class S3Client:
    def __init__(self):
        self.session = aioboto3.Session()
        self.client = self.session.client("s3", region_name=settings.AWS_REGION)
        logger.info(f"Initialized S3Client with region: {settings.AWS_REGION}")

    async def upload_file(self, file_obj, filename: str) -> str:
        try:
            logger.info(f"Attempting to upload file {filename} to bucket {settings.S3_BUCKET_NAME}")
            async with self.client as s3:
                await s3.upload_fileobj(file_obj, settings.S3_BUCKET_NAME, filename)
            return f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise RuntimeError("AWS credentials not found")
        except Exception as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise RuntimeError(f"S3 upload failed: {str(e)}") 