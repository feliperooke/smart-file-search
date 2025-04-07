from abc import ABC, abstractmethod
from app.common.schemas import FileDTO


class FileExplorer(ABC):
    @abstractmethod
    def explore(self, search: str, file_dto: FileDTO) -> str:
        pass