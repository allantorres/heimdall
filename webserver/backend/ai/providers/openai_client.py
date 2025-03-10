from openai import AsyncOpenAI
from typing import Dict, Any, Optional
from ..base import BaseAIClient
import os

class OpenAIClient(BaseAIClient):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.cost_per_1k_tokens = {
            'gpt-4': {'input': 0.03, 'output': 0.06},
            'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
            'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015}
        }

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return {
            'response': response.choices[0].message.content,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens
            },
            'cost': self.calculate_cost(response.usage.prompt_tokens, response.usage.completion_tokens)
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        rates = self.cost_per_1k_tokens.get(self.model, {'input': 0, 'output': 0})
        return (input_tokens * rates['input'] + output_tokens * rates['output']) / 1000