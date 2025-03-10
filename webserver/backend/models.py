from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AIProvider(models.Model):
    name = models.CharField(max_length=100)  # e.g., OpenAI, Anthropic, DeepSeek
    api_key_name = models.CharField(max_length=100)  # Environment variable name for the API key
    base_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Agent(models.Model):
    AGENT_TYPES = [
        ('interview', 'Interview Agent'),
        ('code_review', 'Code Review Agent'),
        ('content_writer', 'Content Writer Agent'),
        ('questions', 'Question Writer Agent'),
    ]
    
    name = models.CharField(max_length=200)
    agent_type = models.CharField(max_length=50, choices=AGENT_TYPES, default='interview')  # Added default
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='agents')
    provider = models.ForeignKey(AIProvider, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    system_prompt = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.provider.name})"

class AgentExecution(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='executions')
    input_data = models.JSONField(default=dict)
    output_data = models.JSONField(default=dict)
    execution_time = models.FloatField(default=0.0)
    tokens_used = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    status = models.CharField(max_length=20, default='pending')
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add to default

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Execution of {self.agent.name}"
