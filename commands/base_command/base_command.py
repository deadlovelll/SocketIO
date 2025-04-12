from abc import ABC, abstractmethod

class BaseCommand(ABC):
    
    def __init__ (
        self, 
        **options,
    ) -> None:
        
        self.options = options
        super().__init__()
    
    @abstractmethod
    def execute():
        pass