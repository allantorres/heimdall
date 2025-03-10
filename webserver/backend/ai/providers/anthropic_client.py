from anthropic import AsyncAnthropic
from typing import Dict, Any, Optional
from ..base import BaseAIClient
import os

class AnthropicClient(BaseAIClient):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = AsyncAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.cost_per_1k_tokens = {
            'claude-3-opus': {'input': 0.015, 'output': 0.075},
            'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
            'claude-2.1': {'input': 0.008, 'output': 0.024}
        }

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=messages,
            system=system_prompt
        )

        return {
            'response': response.content[0].text,
            'usage': {
                'prompt_tokens': response.usage.input_tokens,
                'completion_tokens': response.usage.output_tokens
            },
            'cost': self.calculate_cost(response.usage.input_tokens, response.usage.output_tokens)
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        rates = self.cost_per_1k_tokens.get(self.model, {'input': 0, 'output': 0})
        return (input_tokens * rates['input'] + output_tokens * rates['output']) / 1000