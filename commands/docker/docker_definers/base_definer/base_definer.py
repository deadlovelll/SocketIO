from abc import ABC, abstractmethod

class BaseDockerDefiner(ABC):
    
    @abstractmethod
    def define():
        pass