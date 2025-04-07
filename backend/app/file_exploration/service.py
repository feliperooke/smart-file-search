from app.common.schemas import FileDTO
from app.file_exploration.file_explorer import FileExplorer
from app.file_exploration.strategies.gemini_explorer import GeminiExplorer

class FileExplorationService:
    """
    Service responsible for exploring file content.
    """
    
    def __init__(self, explorer: FileExplorer = None):
        self.explorer = explorer or GeminiExplorer()
    
    def explore(self, search: str, file_dto: FileDTO) -> str:
        return self.explorer.explore(search, file_dto)