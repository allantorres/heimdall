from rest_framework import serializers
from .models import Project, Agent, AIProvider, AgentExecution

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'url', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class AIProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIProvider
        fields = ['id', 'name', 'api_key_name', 'base_url', 'created_at']
        read_only_fields = ['created_at']

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'agent_type', 'project', 'provider', 'model',
                 'system_prompt', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class AgentExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentExecution
        fields = ['id', 'agent', 'input_data', 'output_data', 'execution_time',
                 'tokens_used', 'cost', 'status', 'error_message', 'created_at']
        read_only_fields = ['created_at']