from abc import ABC, abstractmethod

class BaseOSDetector(ABC):
    
    """Abstract base class for OS detectors."""
    
    @abstractmethod
    def detect (
        self,
    ) -> str:
        
        """Detects and returns the OS name."""
        
        pass