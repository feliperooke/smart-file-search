from fastapi import UploadFile
import hashlib
import logging
import os
import asyncio
from app.text_extraction.service import TextExtractionService
from app.uploads.service import FileUploadService
from app.file_processing.repository import FileProcessingRepository
from app.common.exceptions import FileProcessingError, TextExtractionError, FileUploadError
from .schemas import FileProcessResponse
from .models import FileProcessingRecord
from datetime import datetime
from io import BytesIO
from typing import Optional

# Constants
SAMPLE_SIZE_BYTES = 32768  # 32KB
HASH_ALGORITHM = 'md5'

# Configure logger
logger = logging.getLogger(__name__)

class FileProcessorService:
    """
    Service responsible for processing and uploading files.
    
    This service coordinates the text extraction, file upload, and storage operations.
    It ensures files are processed efficiently and maintains a record of processed files.
    """
    
    def __init__(
        self, 
        text_extraction_service: TextExtractionService, 
        upload_service: FileUploadService
    ):
        """
        Initialize the FileProcessorService.
        
        Args:
            text_extraction_service: Service for extracting text from files
            upload_service: Service for handling file uploads
        """
        self.text_extraction_service = text_extraction_service
        self.upload_service = upload_service
        self.repository = FileProcessingRepository()

    async def process_and_upload(self, file: UploadFile) -> FileProcessResponse:
        """
        Process a file by extracting its text and uploading it.
        
        This method:
        1. Generates a unique identifier for the file
        2. Checks if the file was already processed
        3. Creates an initial record with status "received"
        4. Extracts text from the file and updates status to "extracted"
        5. Uploads the file and updates status to "stored"
        6. Completes the record with status "completed"
        7. Returns the processing response
        
        Args:
            file: The file to be processed and uploaded
            
        Returns:
            FileProcessResponse containing the processing results
            
        Raises:
            TextExtractionError: If text extraction fails
            FileUploadError: If file upload fails
            FileProcessingError: If an unexpected error occurs
        """
        try:
            logger.info(f"Starting file processing for: {file.filename}")
            file_id = self._calculate_file_identifier(file)
            
            # Check if the file was already processed
            file_record = await self._get_file_record(file_id)
            if file_record:
                return self._create_response_from_record(file_record)
            
            # Create initial record with status "received"
            file_record = await self._create_initial_record(file_id, file)
            
            try:
                # Extract text and update status to "extracted"
                extracted_text = await self._extract_text(file)
                file_record = await self._update_processing_status(file_record, "extracted")
                
                # Upload file and update status to "stored"
                upload_response = await self._upload_file(file, file_id)
                file_record = await self._update_processing_status(file_record, "stored")
                
                # Complete the record with status "completed"
                file_record = await self._complete_processing_record(
                    file_record=file_record,
                    upload_response=upload_response,
                    extracted_text=extracted_text
                )
                
                return self._create_response_from_record(file_record)
                
            except (TextExtractionError, FileUploadError) as e:
                # Update status to "error" if an error occurs
                await self._update_processing_status(file_record, "error", str(e))
                raise
                
        except Exception as e:
            logger.error(f"Unexpected error processing file {file.filename}: {str(e)}", exc_info=True)
            raise FileProcessingError(f"Unexpected error processing file: {str(e)}")

    async def _create_initial_record(self, file_id: str, file: UploadFile) -> FileProcessingRecord:
        """
        Create an initial record with status "received".
        
        Args:
            file_id: The unique identifier for the file
            file: The file being processed
            
        Returns:
            The created FileProcessingRecord
        """
        logger.info(f"Creating initial record with status 'received' for file: {file.filename}")
        
        now = datetime.utcnow()
        record = FileProcessingRecord(
            pk=file_id,
            file_name=file.filename,
            file_url="",  # Will be updated after upload
            file_size=file.size,
            file_type=file.content_type,
            markdown_content="",  # Will be updated after extraction
            processing_status="received",
            embedding_status="pending",
            created_at=now,
            updated_at=now,
            metadata={
                "original_filename": file.filename,
                "content_type": file.content_type
            }
        )
        
        await self.repository.put_item(record)
        logger.info(f"Initial record created for file: {file.filename}")
        return record
    
    async def _update_processing_status(self, record: FileProcessingRecord, new_status: str, error_message: Optional[str] = None) -> FileProcessingRecord:
        """
        Update the processing status of a file record.
        
        Args:
            record: The FileProcessingRecord to update
            new_status: The new processing status
            error_message: Optional error message if status is "error"
            
        Returns:
            The updated FileProcessingRecord
        """
        logger.info(f"Updating status to '{new_status}' for file: {record.file_name}")
        
        record.processing_status = new_status
        
        if error_message:
            record.error_message = error_message
            logger.error(f"Error message added: {error_message}")
            
        await self.repository.put_item(record)
        logger.info(f"Status updated to '{new_status}' for file: {record.file_name}")
        return record
    
    async def _complete_processing_record(
        self,
        file_record: FileProcessingRecord,
        upload_response,
        extracted_text: str
    ) -> FileProcessingRecord:
        """
        Complete the processing record with all information.
        
        Args:
            file_record: The FileProcessingRecord to complete
            upload_response: The response from the upload service
            extracted_text: The extracted text content
            
        Returns:
            The completed FileProcessingRecord
        """
        logger.info(f"Completing processing record for file: {file_record.file_name}")
        
        file_record.file_url = upload_response.url
        file_record.markdown_content = extracted_text
        file_record.processing_status = "completed"
        
        await self.repository.put_item(file_record)
        logger.info(f"Processing record completed for file: {file_record.file_name}")
        return file_record

    async def _get_file_record(self, file_id: str) -> Optional[FileProcessingRecord]:
        """
        Retrieve a file record from DynamoDB by its identifier.
        
        Args:
            file_id: The unique identifier of the file
            
        Returns:
            FileProcessingRecord if found, None otherwise
        """
        logger.info(f"Checking if file with ID {file_id} was already processed")
        record = await self.repository.get_item({"pk": file_id}, FileProcessingRecord)
        if record:
            logger.info(f"Found existing record for file: {record.file_name}")
        else:
            logger.info(f"No existing record found for file ID: {file_id}")
        return record

    def _create_response_from_record(self, file_record: FileProcessingRecord) -> FileProcessResponse:
        """
        Create a FileProcessResponse from a FileProcessingRecord.
        
        This method converts a DynamoDB record into the expected response format
        for the process_and_upload method.
        
        Args:
            file_record: The file record from DynamoDB
            
        Returns:
            FileProcessResponse containing all file information
        """
        logger.debug(f"Creating response from record: {file_record.file_name}")
        
        # Convert history list to dictionary format
        history_dict = {}
        for entry in file_record.history:
            for status, timestamp in entry.items():
                history_dict[status] = timestamp
        
        return FileProcessResponse(
            pk=file_record.pk,
            filename=file_record.file_name,
            url=file_record.file_url,
            content=file_record.markdown_content,
            file_size=file_record.file_size,
            file_type=file_record.file_type,
            markdown_content=file_record.markdown_content,
            processing_status=file_record.processing_status,
            embedding_status=file_record.embedding_status,
            created_at=file_record.created_at,
            updated_at=file_record.updated_at,
            error_message=file_record.error_message,
            metadata=file_record.metadata or {},
            history=history_dict
        )

    async def _extract_text(self, file: UploadFile) -> str:
        """
        Extract text from the file.
        
        Args:
            file: The file to extract text from
            
        Returns:
            The extracted text
            
        Raises:
            TextExtractionError: If text extraction fails
        """
        try:
            logger.info(f"Starting text extraction for file: {file.filename}")
            extract_method = self.text_extraction_service.extract
            if asyncio.iscoroutinefunction(extract_method):
                logger.debug("Using async text extraction method")
                result = await extract_method(file)
            else:
                logger.debug("Using sync text extraction method")
                result = extract_method(file)
            logger.info(f"Text extraction completed for file: {file.filename} (content length: {len(result)} characters)")
            return result
        except Exception as e:
            logger.error(f"Error extracting text from file {file.filename}: {str(e)}", exc_info=True)
            raise TextExtractionError(f"Failed to extract text from file: {str(e)}")

    async def _upload_file(self, file: UploadFile, file_id: str):
        """
        Upload the file.
        
        Args:
            file: The file to upload
            
        Returns:
            The upload response
            
        Raises:
            FileUploadError: If file upload fails
        """
        try:
            logger.info(f"Starting file upload for: {file.filename} (ID: {file_id})")
            file.file.seek(0)  # Reset file pointer for upload
            response = await self.upload_service.upload(file, file_id)
            logger.info(f"File uploaded successfully: {file.filename} (URL: {response.url})")
            return response
        except Exception as e:
            logger.error(f"Error uploading file {file.filename}: {str(e)}", exc_info=True)
            raise FileUploadError(f"Failed to upload file: {str(e)}")

    def _calculate_file_identifier(self, file: UploadFile) -> str:
        """
        Calculate a unique identifier for the file using a sample of its content.
        
        This method reads a sample from the beginning of the file and creates a hash.
        The sample size is defined by SAMPLE_SIZE_BYTES.
        
        Args:
            file: The file to generate an identifier for
            
        Returns:
            A string identifier based on the file's content sample
        """
        logger.info(f"Calculating file identifier for: {file.filename} (size: {file.size} bytes, type: {file.content_type})")
        current_position = file.file.tell()
        file.file.seek(0)
        
        try:
            sample = file.file.read(SAMPLE_SIZE_BYTES)
            file_id = hashlib.new(HASH_ALGORITHM, sample).hexdigest()
            logger.info(f"Generated file ID: {file_id} for file: {file.filename}")
            return file_id
        finally:
            file.file.seek(current_position) 