from app.file_exploration.file_explorer import FileExplorer
from app.common.schemas import FileDTO

class BasicExplorer(FileExplorer):
    """
    A basic strategy for exploring file content.
    This strategy simply returns the file content.
    """
    
    def explore(self, search: str, file_dto: FileDTO) -> str:
        """
        Explores the file content.
        
        Args:
            search: The search query or instructions for exploring the content
            file_dto: The file DTO to be explored
            
        Returns:
            A string containing the explored file content
        """
        # Return the file content
        return file_dto.content 