document.addEventListener('DOMContentLoaded', function() {
    // CSRF token setup for AJAX requests
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // Modal handling
    const modal = document.getElementById('agentModal');
    const executeModal = document.getElementById('executeModal');
    const createAgentBtn = document.getElementById('createAgentBtn');
    const agentForm = document.getElementById('agentForm');
    const executeForm = document.getElementById('executeForm');
    let currentAgentId = null;

    // Check if elements exist before adding event listeners
    if (createAgentBtn) {
        createAgentBtn.addEventListener('click', () => {
            currentAgentId = null;
            document.getElementById('modalTitle').textContent = 'Create New Agent';
            if (agentForm) agentForm.reset();
            if (modal) modal.classList.remove('hidden');
        });
    }

    // Define modal functions in window scope to make them accessible from HTML
    window.closeModal = function() {
        if (modal) modal.classList.add('hidden');
        if (agentForm) agentForm.reset();
    }

    window.closeExecuteModal = function() {
        if (executeModal) executeModal.classList.add('hidden');
        if (executeForm) executeForm.reset();
        const resultArea = document.getElementById('resultArea');
        if (resultArea) resultArea.classList.add('hidden');
    }

    window.editAgent = async function(id) {
        try {
            const response = await fetch(`/api/agents/${id}/`);
            const agent = await response.json();
            
            currentAgentId = id;
            document.getElementById('modalTitle').textContent = 'Edit Agent';
            document.getElementById('name').value = agent.name;
            document.getElementById('project').value = agent.project;
            document.getElementById('provider').value = agent.provider;
            document.getElementById('model').value = agent.model;
            document.getElementById('description').value = agent.description;
            document.getElementById('system_prompt').value = agent.system_prompt;
            if (modal) modal.classList.remove('hidden');
        } catch (error) {
            alert('Error loading agent: ' + error);
        }
    }

    window.executeAgent = function(id) {
        const agentIdField = document.getElementById('agent_id');
        const resultArea = document.getElementById('resultArea');
        
        if (agentIdField) agentIdField.value = id;
        if (resultArea) resultArea.classList.add('hidden');
        if (executeModal) executeModal.classList.remove('hidden');
    }

    // Form submissions
    if (agentForm) {
        agentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                project: document.getElementById('project').value,
                provider: document.getElementById('provider').value,
                model: document.getElementById('model').value,
                description: document.getElementById('description').value,
                system_prompt: document.getElementById('system_prompt').value
            };
            
            // Add agent_type if it exists
            const agentTypeField = document.getElementById('agent_type');
            if (agentTypeField) {
                formData.agent_type = agentTypeField.value;
            }
            
            try {
                if (currentAgentId) {
                    await updateAgent(currentAgentId, formData);
                } else {
                    await createAgent(formData);
                }
                window.location.reload();
            } catch (error) {
                alert('Error saving agent: ' + error.message);
            }
        });
    }

    if (executeForm) {
        executeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const agentId = document.getElementById('agent_id').value;
            const jobDescription = document.getElementById('job_description').value;
            
            try {
                const response = await fetch(`/api/agents/${agentId}/generate_questions/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    body: JSON.stringify({ job_description: jobDescription })
                });
                
                const result = await response.json();
                const resultArea = document.getElementById('resultArea');
                const resultContent = document.getElementById('resultContent');
                
                if (resultContent) resultContent.textContent = JSON.stringify(result, null, 2);
                if (resultArea) resultArea.classList.remove('hidden');
            } catch (error) {
                alert('Error executing agent: ' + error.message);
            }
        });
    }

    // CRUD Operations
    async function createAgent(data) {
        const response = await fetch('/api/agents/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            credentials: 'include',  // Add this line to include cookies
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to create agent');
        return response.json();
    }

    async function updateAgent(id, data) {
        const response = await fetch(`/api/agents/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to update agent');
        return response.json();
    }
});