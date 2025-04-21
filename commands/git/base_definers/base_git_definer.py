from abc import ABC, abstractmethod

class BaseGitDefiner(ABC):
    
    @abstractmethod
    def define():
        ...