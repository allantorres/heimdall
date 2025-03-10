from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backend.models import Project, Agent, AgentExecution
from datetime import datetime, timedelta
import random
import json

class Command(BaseCommand):
    help = 'Seeds the database with a sample agent and execution metrics'

    def handle(self, *args, **kwargs):
        # Create a test user if none exists
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            self.stdout.write(self.style.SUCCESS('Created test user'))
        else:
            user = User.objects.get(username='testuser')
            
        project = Project.objects.get(name='NovoCurriculo')
            
        # Create a test agent if none exists
        agent = Agent.objects.get(name='Interview')
            
        # Generate sample executions for the past 30 days
        start_date = datetime.now() - timedelta(days=30)
        
        # Delete existing executions for this agent
        AgentExecution.objects.filter(agent=agent).delete()
        
        # Create new executions
        for day in range(30):
            execution_date = start_date + timedelta(days=day)
            # Create 1-5 executions per day
            for _ in range(random.randint(30, 800)):
                # Randomize execution metrics
                execution_time = random.uniform(0.5, 8.0)
                tokens_used = random.randint(1000, 3000)
                cost = tokens_used * 0.000002  # Approximate cost calculation
                
                # Create sample input/output data
                input_data = {
                    'job_description': 'Senior Software Engineer with 5+ years of experience in Python and Django.'
                }
                
                output_data = {
                    'questions': [
                        'Can you describe your experience with Django ORM?',
                        'How have you implemented authentication in your Django projects?',
                        'What strategies do you use for optimizing database queries?',
                        'Describe a challenging bug you encountered and how you solved it.',
                        'How do you approach testing in your Django applications?'
                    ],
                    'usage': {
                        'prompt_tokens': tokens_used // 3,
                        'completion_tokens': tokens_used // 3 * 2,
                        'total_tokens': tokens_used
                    }
                }
                
                # Create the execution record
                AgentExecution.objects.create(
                    agent=agent,
                    input_data=input_data,
                    output_data=output_data,
                    execution_time=execution_time,
                    tokens_used=tokens_used,
                    cost=cost,
                    status='success',
                    created_at=execution_date
                )
                
        self.stdout.write(self.style.SUCCESS(f'Created {AgentExecution.objects.filter(agent=agent).count()} sample executions for the agent'))