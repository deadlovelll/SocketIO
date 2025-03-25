from abc import ABC, abstractstaticmethod

class BaseDockerDefiner(ABC):
    
    @abstractstaticmethod
    def define():
        pass