from typing import Dict, Any
from .base import BaseAgent

class ContentWriterAgent(BaseAgent):
    @property
    def default_system_prompt(self) -> str:
        return """
        VOCÊ É UM EXPERT EM CRIAÇÃO DE CONTEÚDO.
        
        ### TAREFA ###
        CRIAR CONTEÚDO DE ALTA QUALIDADE COM BASE NO TEMA E REQUISITOS FORNECIDOS.
        
        ### FORMATO DE SAÍDA ###
        {
            "content": {
                "title": "Título do conteúdo",
                "summary": "Resumo do conteúdo",
                "sections": [
                    {
                        "heading": "Título da seção",
                        "content": "Conteúdo da seção"
                    }
                ],
                "keywords": ["palavra-chave1", "palavra-chave2"],
                "meta_description": "Descrição meta para SEO"
            }
        }
        """

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        topic = input_data.get('topic', '')
        requirements = input_data.get('requirements', '')
        return await self.agent.provider.generate_completion(
            self.agent.system_prompt or self.default_system_prompt,
            f"Topic: {topic}\n\nRequirements:\n{requirements}"
        )