from groq import AsyncGroq
from typing import Dict, Any, Optional
from ..base import BaseAIClient
import os

class GroqClient(BaseAIClient):
    def __init__(self, model: str):
        super().__init__(model)
        self.client = AsyncGroq(api_key=os.getenv('GROQ_API_KEY'))
        self.cost_per_1k_tokens = {
            'llama2-70b': {'input': 0.0005, 'output': 0.0005},
            'mixtral-8x7b': {'input': 0.0003, 'output': 0.0003}
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