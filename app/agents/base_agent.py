from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def get_response(self, url: str) -> str:
        pass
