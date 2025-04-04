from fastapi import FastAPI, Request
from mangum import Mangum
import logging
import sys

from app.uploads.router import router as uploads_router
from app.health.router import router as health_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(uploads_router, prefix="/api")
app.include_router(health_router, prefix="/api")

# Entry point for AWS Lambda
handler = Mangum(app)
