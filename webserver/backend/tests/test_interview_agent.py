import asyncio
import pytest
from django.contrib.auth.models import User
from backend.models import Project, AIProvider, Agent
from backend.agents.interview_agent import InterviewAgent

@pytest.mark.asyncio
async def test_interview_agent():
    # Setup
    provider = AIProvider.objects.get(name='OpenAI')
    user = User.objects.first()
    project = Project.objects.get(name='Interview Project')
    agent = Agent.objects.get(name='Interview Assistant')
    
    # Create agent instance
    interview_agent = InterviewAgent(agent)
    
    # Test job description
    job_description = """
    We are looking for a Senior Python Developer with 5+ years of experience in Django and REST APIs.
    The candidate should have strong knowledge of PostgreSQL and experience with Docker containers.
    """
    
    # Generate questions
    result = await interview_agent.generate_interview_questions(job_description)
    
    # Print results
    print("\nGenerated Questions:")
    for question in result.get('questions', []):
        print(f"\nType: {question['type']}")
        print(f"Question: {question['question']}")
        print(f"Expected Answer: {question['answer']}")
        print(f"Key Points: {', '.join(question['key_points'])}")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_interview_agent())