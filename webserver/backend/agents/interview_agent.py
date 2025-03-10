from typing import Dict, Any, Optional
from ..models import Agent, AgentExecution
from ..ai.factory import AIFactory
from ..decorators.monitoring import monitor_execution
from .base import BaseAgent

class InterviewAgent(BaseAgent):
    @property
    def default_system_prompt(self) -> str:
        return """
        VOCÊ É UM ESPECIALISTA EM RECRUTAMENTO E SELEÇÃO.
        
        ### TAREFA ###
        GERAR PERGUNTAS PERSONALIZADAS PARA UMA ENTREVISTA.
        
        ### FORMATO DE SAÍDA ###
        {
            "questions": [
                {
                    "type": "technical|behavioral",
                    "question": "Pergunta aqui",
                    "answer": "Resposta modelo aqui",
                    "key_points": ["Ponto 1", "Ponto 2", "Ponto 3"]
                }
            ]
        }
        """

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        job_description = input_data.get('job_description', '')
        return await self.agent.provider.generate_completion(
            self.agent.system_prompt or self.default_system_prompt,
            job_description
        )

    @monitor_execution
    async def generate_interview_questions(self, job_description: str, model: Optional[str] = None) -> Dict[str, Any]:
        system_prompt = self.agent.system_prompt or """
            VOCÊ É UM ESPECIALISTA EM RECRUTAMENTO E SELEÇÃO, COM VASTA EXPERIÊNCIA EM ENTREVISTAS TÉCNICAS E COMPORTAMENTAIS.

            ### SUA TAREFA ###
            GERAR 10 PERGUNTAS PERSONALIZADAS PARA UMA ENTREVISTA COM BASE NA DESCRIÇÃO DA VAGA.

            ### INSTRUÇÕES ###
            - CRIE 10 PERGUNTAS RELEVANTES BASEADAS NA DESCRIÇÃO DA VAGA E O NÍVEL DE PERGUNTAS DEVE SER SEMPRE DE MÉDIANO PARA AVANÇADO.
            - MISTURE PERGUNTAS TÉCNICAS E COMPORTAMENTAIS.

            {
                "questions": [
                    {
                        "type": "technical|behavioral",
                        "question": "Pergunta aqui",
                        "answer": "Resposta modelo aqui",
                        "key_points": ["Ponto 1", "Ponto 2", "Ponto 3"]
                    }
                ]
            }
        """

        user_prompt = f"Analise esta descrição de vaga e gere perguntas para entrevista: {job_description}"
        
        # If model is provided, create a new client instance with the specified model
        if model:
            client = AIFactory.get_client(self.agent.provider.name.lower(), model)
        else:
            client = self.client
            
        response = await client.generate_response(user_prompt, system_prompt=system_prompt)
        
        return response