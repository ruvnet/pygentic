from abc import ABC, abstractmethod

class BaseConnector(ABC):
    
    @abstractmethod
    def initialize(self, config: dict):
        pass

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass
