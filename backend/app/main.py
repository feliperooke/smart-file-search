from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging
import sys

from app.uploads.router import router as uploads_router
from app.health.router import router as health_router
from app.file_processing.router import router as file_processing_router
from app.chat.router import ChatRouter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart File Search API",
    description="API for processing and searching files",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # URL of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(uploads_router, prefix="/api")
app.include_router(health_router, prefix="/api")
app.include_router(file_processing_router, prefix="/api")

# Register chat router
chat_router = ChatRouter()
app.include_router(chat_router.router, prefix="/api")

# AWS Lambda handler
handler = Mangum(app, lifespan="off") 