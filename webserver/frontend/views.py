from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from backend.models import Project, Agent, AIProvider, AgentExecution
from backend.agents.factory import AgentFactory
from django.db.models import Avg, Count
from django.db.models.functions import TruncDay
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def home(request):
    return render(request, 'frontend/home.html')

@login_required
def projects(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        url = request.POST.get('url', '')
        
        project = Project.objects.create(
            name=name,
            description=description,
            url=url,
            user=request.user  # Associate the project with the current user
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'id': project.id, 'name': project.name})
        return redirect('projects')
        
    user_projects = Project.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'frontend/projects.html', {'projects': user_projects})

@login_required
def agents(request):
    context = {
        'agents': Agent.objects.filter(project__user=request.user),
        'projects': Project.objects.filter(user=request.user),
        'providers': AIProvider.objects.all(),
        'agent_types': Agent.AGENT_TYPES
    }
    return render(request, 'frontend/agents.html', context)

@login_required
def metrics(request):
    # Get date range
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Get user's agents
    user_agents = Agent.objects.filter(project__user=request.user)
    
    # Get executions
    executions = AgentExecution.objects.filter(
        agent__in=user_agents,
        created_at__range=(start_date, end_date)
    )
    
    # Calculate metrics
    total_executions = executions.count()
    avg_response_time = executions.aggregate(Avg('execution_time'))['execution_time__avg'] or 0
    total_cost = sum(float(e.cost) for e in executions)
    success_rate = (executions.filter(status='success').count() / total_executions * 100) if total_executions > 0 else 0
    
    # Get executions by day
    daily_executions = executions.annotate(
        date=TruncDay('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Calculate cost change compared to previous period
    previous_start = start_date - timedelta(days=30)
    previous_end = end_date - timedelta(days=30)
    
    previous_executions = AgentExecution.objects.filter(
        agent__in=user_agents,
        created_at__range=(previous_start, previous_end)
    )
    
    previous_cost = sum(float(e.cost) for e in previous_executions)
    cost_change = ((total_cost - previous_cost) / previous_cost * 100) if previous_cost > 0 else 0
    
    # Calculate other comparison metrics
    previous_total = previous_executions.count()
    execution_increase = ((total_executions - previous_total) / previous_total * 100) if previous_total > 0 else 0
    
    previous_avg_time = previous_executions.aggregate(Avg('execution_time'))['execution_time__avg'] or 0
    response_time_improvement = ((previous_avg_time - avg_response_time) / previous_avg_time * 100) if previous_avg_time > 0 else 0
    
    previous_success = (previous_executions.filter(status='success').count() / previous_total * 100) if previous_total > 0 else 0
    success_rate_increase = success_rate - previous_success
    
    # Get daily costs and token usage
    daily_costs = []
    token_usage = []
    for execution in executions:
        daily_costs.append(float(execution.cost))
        token_usage.append(execution.tokens_used)
    
    # Get agent costs breakdown
    agent_costs = []
    agent_names = []
    for agent in user_agents:
        agent_executions = executions.filter(agent=agent)
        agent_cost = sum(float(e.cost) for e in agent_executions)
        if agent_cost > 0:  # Only include agents with costs
            agent_costs.append(agent_cost)
            agent_names.append(agent.name)
    
    # Get execution statuses for CSV export
    statuses = [e.status for e in executions]
    
    # Prepare data for JavaScript
    js_data = {
        'executionDates': [e['date'].strftime('%Y-%m-%d') for e in daily_executions],
        'executionCounts': [e['count'] for e in daily_executions],
        'dailyCosts': daily_costs,
        'tokenUsage': token_usage,
        'agentCosts': agent_costs,
        'agentNames': agent_names,
        'statuses': statuses,
        'responseTimes': [float(e.execution_time) for e in executions],
    }

    context = {
        'total_executions': total_executions,
        'avg_response_time': round(avg_response_time, 2),
        'total_cost': round(total_cost, 2),
        'success_rate': round(success_rate, 1),
        'cost_change': round(cost_change, 1),
        'execution_increase': round(execution_increase, 1),
        'response_time_improvement': round(response_time_improvement, 1),
        'success_rate_increase': round(success_rate_increase, 1),
        'recent_executions': executions.select_related('agent').order_by('-created_at')[:50],
        'metrics_data': json.dumps(js_data, cls=DjangoJSONEncoder),  # Serialize data for JavaScript
    }
    
    return render(request, 'frontend/metrics.html', context)
