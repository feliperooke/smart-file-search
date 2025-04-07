import os
from typing import Dict, Any, Optional
import google.generativeai as genai
import logging
from app.file_exploration.file_explorer import FileExplorer
from app.common.schemas import FileDTO
from app.infrastructure.config import settings

logger = logging.getLogger(__name__)

class GeminiExplorer(FileExplorer):
    """
    A strategy that uses Google's Gemini model to explore file content.
    This strategy analyzes the content based on the search query.
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash"):
        """
        Initializes the Gemini explorer.
        
        Args:
            api_key: Google API key for Gemini (defaults to settings.GOOGLE_API_KEY)
            model_name: The Gemini model to use (default: gemini-2.0-flash)
        """
        self.api_key = api_key or settings.GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("Google API key is required for GeminiExplorer")
        
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def explore(self, search: str, file_dto: FileDTO) -> str:
        """
        Explores the file content using Gemini AI.
        
        Args:
            search: The search query or instructions for exploring the content
            file_dto: The file DTO containing the content to be explored
            
        Returns:
            A string containing the AI's response based on the content and search query
        """
        try:
            # Prepare the prompt combining the search query and file content
            prompt = self._create_prompt(search, file_dto)
            
            # Set parameters for better control
            generation_config = {
                "temperature": 0.3,
                "top_p": 0.8,
                "max_output_tokens": 2048
            }
            
            # Call Gemini API with generation config
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Return the response text
            if hasattr(response, "text"):
                return response.text
            elif hasattr(response, "parts"):
                return "".join(part.text for part in response.parts)
            else:
                return "Unable to process response from Gemini API"
                
        except Exception as e:
            logger.error(f"Error using Gemini to explore content: {str(e)}")
            return f"Error exploring content with Gemini: {str(e)}"
    
    def _create_prompt(self, search: str, file_dto: FileDTO) -> str:
        """
        Creates a prompt for the Gemini model.
        
        Args:
            search: The search query or instructions
            file_dto: The file DTO containing content
            
        Returns:
            A formatted prompt string
        """
        return f"""
You are an AI assistant specialized in analyzing and exploring document content.

INSTRUCTIONS:
{search}

DOCUMENT CONTENT:
{file_dto.markdown_content}

Please respond directly to the instructions above based solely on the document content provided.
Be concise and accurate. If the answer is not in the document, say so clearly.
""" 