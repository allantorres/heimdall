from typing import Type
from .base import BaseAgent
from .interview_agent import InterviewAgent
from .code_review_agent import CodeReviewAgent
from .content_writer_agent import ContentWriterAgent
from .questions_agent import QuestionsAgent


class AgentFactory:
    _agents = {
        'interview': InterviewAgent,
        'code_review': CodeReviewAgent,
        'content_writer': ContentWriterAgent, 
        'questions_agent': QuestionsAgent, 
        
    }
    
    @classmethod
    def get_agent(cls, agent_type: str) -> Type[BaseAgent]:
        agent_class = cls._agents.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return agent_class

    @classmethod
    def get_available_types(cls):
        return list(cls._agents.keys())