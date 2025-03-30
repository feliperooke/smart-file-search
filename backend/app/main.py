from fastapi import FastAPI, Request
from mangum import Mangum
import logging
import sys
import traceback
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    # Log request body if present
    try:
        body = await request.body()
        if body:
            logger.info(f"Request body: {body.decode()}")
    except Exception as e:
        logger.error(f"Error reading request body: {str(e)}")
    
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/")
def read_root():
    try:
        logger.info("Root endpoint called")
        return {"message": "Hello from FastAPI on Lambda!"}
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return {"message": "Internal Server Error", "detail": str(exc)}

# Entry point for AWS Lambda
handler = Mangum(app)

# Add debug log to confirm handler is created
logger.info("Lambda handler created successfully")
