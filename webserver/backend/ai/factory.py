import os
from typing import Dict, Type
from .base import BaseAIClient
from .providers.openai_client import OpenAIClient
from .providers.anthropic_client import AnthropicClient
from .providers.deepseek_client import DeepseekClient

class AIFactory:
    _clients: Dict[str, Type[BaseAIClient]] = {
        'openai': OpenAIClient,
        'anthropic': AnthropicClient,
        'deepseek': DeepseekClient
    }

    @classmethod
    def register_client(cls, name: str, client_class: Type[BaseAIClient]):
        cls._clients[name.lower()] = client_class

    @classmethod
    def get_client(cls, provider: str, model: str) -> BaseAIClient:
        provider = provider.lower()
        if provider not in cls._clients:
            raise ValueError(f"Unknown AI provider: {provider}")
        
        return cls._clients[provider](model)