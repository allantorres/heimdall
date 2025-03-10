from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models import Agent

class BaseAgent(ABC):
    def __init__(self, agent_instance: Agent):
        self.agent = agent_instance
        
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @property
    @abstractmethod
    def default_system_prompt(self) -> str:
        pass