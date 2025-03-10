from typing import Dict, Any
from .base import BaseAgent

class CodeReviewAgent(BaseAgent):
    @property
    def default_system_prompt(self) -> str:
        return """
        VOCÊ É UM EXPERT EM REVISÃO DE CÓDIGO.
        
        ### TAREFA ###
        ANALISAR O CÓDIGO E FORNECER FEEDBACK DETALHADO.
        
        ### FORMATO DE SAÍDA ###
        {
            "review": {
                "summary": "Resumo geral da análise",
                "issues": [
                    {
                        "type": "security|performance|maintainability|best_practice",
                        "severity": "high|medium|low",
                        "description": "Descrição do problema",
                        "suggestion": "Sugestão de correção",
                        "code_snippet": "Trecho relevante do código"
                    }
                ],
                "recommendations": ["Recomendação 1", "Recomendação 2"]
            }
        }
        """

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        code = input_data.get('code', '')
        language = input_data.get('language', '')
        return await self.agent.provider.generate_completion(
            self.agent.system_prompt or self.default_system_prompt,
            f"Language: {language}\n\nCode:\n{code}"
        )