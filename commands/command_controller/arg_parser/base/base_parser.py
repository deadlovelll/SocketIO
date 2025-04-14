from abc import ABC, abstractmethod

class BaseArgumentParser(ABC):
    
    @abstractmethod
    def can_parse (
        self, 
        value: str,
    ) -> bool: ...

    @abstractmethod
    def parse (
        self, 
        value: str,
    ) -> object: ...
