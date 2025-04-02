from fastapi import UploadFile
from markitdown import MarkItDown
from app.text_extraction.text_extractor import TextExtractor
import io

"""
Reference: https://github.com/microsoft/markitdown
"""
class MarkItDownExtractor(TextExtractor):
    def extract(self, file: UploadFile) -> str:
        try:
            # Read the file content
            content = file.file.read()
            
            # Create a new BytesIO object with the content
            file_stream = io.BytesIO(content)
            
            # Reset the original file pointer
            file.file.seek(0)
            
            md = MarkItDown(enable_plugins=False)
            result = md.convert(file_stream)
            return result.text_content
        except Exception as e:
            raise ValueError(f"Text extraction failed: {e}")
