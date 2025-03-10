from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from .agents.interview_agent import InterviewAgent

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Agent, AgentExecution
from .serializers import AgentSerializer, AgentExecutionSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    
    # Add authentication exemption if needed during development
    # Remove or modify this for production
    authentication_classes = []
    permission_classes = []
    
    def get_queryset(self):
        return Agent.objects.filter(project__user=self.request.user)

    @action(detail=True, methods=['post'])
    async def execute(self, request, pk=None):
        agent = self.get_object()
        input_data = request.data
        
        try:
            agent_instance = AgentFactory.get_agent(agent.agent_type)(agent)
            result = await agent_instance.execute(input_data)
            return Response(result)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    async def generate_questions(self, request, pk=None):
        agent = self.get_object()
        job_description = request.data.get('job_description')
        
        if not job_description:
            return Response(
                {'error': 'Job description is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        interview_agent = InterviewAgent(agent)
        try:
            result = await interview_agent.generate_interview_questions(job_description)
            return Response(result)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    async def execute(self, request, pk=None):
        agent = self.get_object()
        input_data = request.data
        start_time = time.time()
        
        try:
            # Create agent instance based on type
            agent_class = self.get_agent_class(agent.type)
            agent_instance = agent_class(agent)
            
            # Execute agent
            result = await agent_instance.execute(input_data)
            
            # Calculate metrics
            execution_time = time.time() - start_time
            
            # Record execution
            execution = AgentExecution.objects.create(
                agent=agent,
                input_data=input_data,
                output_data=result,
                execution_time=execution_time,
                tokens_used=result.get('usage', {}).get('total_tokens', 0),
                cost=result.get('cost', 0),
                status='success'
            )
            
            return Response({
                'execution_id': execution.id,
                'result': result,
                'metrics': {
                    'execution_time': execution_time,
                    'tokens_used': execution.tokens_used,
                    'cost': float(execution.cost)
                }
            })
            
        except Exception as e:
            # Record failed execution
            AgentExecution.objects.create(
                agent=agent,
                input_data=input_data,
                output_data={},
                execution_time=time.time() - start_time,
                tokens_used=0,
                cost=0,
                status='error',
                error_message=str(e)
            )
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_agent_class(self, agent_type):
        # Map agent types to their classes
        agent_classes = {
            'interview': InterviewAgent,
            # Add other agent types here
        }
        return agent_classes.get(agent_type)
