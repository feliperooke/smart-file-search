from fastapi import UploadFile
from app.text_extraction.text_extractor import TextExtractor
from app.text_extraction.strategies.markitdown import MarkItDownExtractor

class TextExtractionService:
    def __init__(self, extractor: TextExtractor = None):
        self.extractor = extractor or MarkItDownExtractor()

    def extract(self, file: UploadFile) -> str:
        return self.extractor.extract(file)