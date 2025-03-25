from abc import ABC, abstractstaticmethod

class FileCreator:
    
    @abstractstaticmethod
    def create_file_text (
        self,
    ) -> str:
        pass
    
    @abstractstaticmethod
    def create_file (
        self,
    ) -> None:
        
        pass