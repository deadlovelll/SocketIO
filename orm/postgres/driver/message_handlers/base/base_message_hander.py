from abc import ABC, abstractmethod


class PostgresDriverBaseMessageHandler(ABC):
    
    @abstractmethod
    def handle(): ...