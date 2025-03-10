from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..models import AgentExecution, Agent
from ..utils.logger import setup_logger

logger = setup_logger('ai_client')

class BaseAIClient(ABC):
    def __init__(self, model: str):
        self.model = model
        
    @abstractmethod
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        pass