from typing import Dict, Any, Optional
import httpx
from ..base import BaseAIClient
import os

class DeepseekClient(BaseAIClient):
    def __init__(self, model: str):
        super().__init__(model)
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.cost_per_1k_tokens = {
            'deepseek-chat': {'input': 0.0005, 'output': 0.0015},
            'deepseek-coder': {'input': 0.001, 'output': 0.002}
        }

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages
                }
            )
            data = response.json()

        return {
            'response': data['choices'][0]['message']['content'],
            'usage': {
                'prompt_tokens': data['usage']['prompt_tokens'],
                'completion_tokens': data['usage']['completion_tokens']
            },
            'cost': self.calculate_cost(data['usage']['prompt_tokens'], data['usage']['completion_tokens'])
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        rates = self.cost_per_1k_tokens.get(self.model, {'input': 0, 'output': 0})
        return (input_tokens * rates['input'] + output_tokens * rates['output']) / 1000