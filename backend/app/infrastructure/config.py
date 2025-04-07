import os

class Settings:
    AWS_REGION = os.getenv("AWS_REGION")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

settings = Settings()
