from abc import ABC, abstractmethod
from fastapi import UploadFile

class TextExtractor(ABC):
    @abstractmethod
    def extract(self, file: UploadFile) -> str:
        pass