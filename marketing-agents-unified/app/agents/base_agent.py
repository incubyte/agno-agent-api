"""
Base Agent Implementation
Base class for all AI agents.
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def get_response(self, prompt: str, **kwargs) -> str:
        """Generate response for the given prompt"""
        pass
    
    def get_prompt_template(self) -> str:
        """Get the system prompt template for this agent"""
        return f"You are {self.name}. {self.description}"
