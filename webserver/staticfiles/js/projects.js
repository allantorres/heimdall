// CSRF token setup for AJAX requests
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Modal handling
const modal = document.getElementById('projectModal');
const createProjectBtn = document.getElementById('createProjectBtn');
const projectForm = document.getElementById('projectForm');
let currentProjectId = null;

createProjectBtn.addEventListener('click', () => {
    currentProjectId = null;
    document.getElementById('modalTitle').textContent = 'Create New Project';
    projectForm.reset();
    modal.classList.remove('hidden');
});

function closeModal() {
    modal.classList.add('hidden');
    projectForm.reset();
}

// CRUD Operations
async function createProject(data) {
    const response = await fetch('/api/projects/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to create project');
    return response.json();
}

async function updateProject(id, data) {
    const response = await fetch(`/api/projects/${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to update project');
    return response.json();
}

async function deleteProject(id) {
    if (!confirm('Are you sure you want to delete this project?')) return;
    
    const response = await fetch(`/api/projects/${id}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        }
    });
    if (!response.ok) throw new Error('Failed to delete project');
    window.location.reload();
}

async function editProject(id) {
    const response = await fetch(`/api/projects/${id}/`);
    const project = await response.json();
    
    currentProjectId = id;
    document.getElementById('modalTitle').textContent = 'Edit Project';
    document.getElementById('name').value = project.name;
    document.getElementById('description').value = project.description;
    document.getElementById('url').value = project.url || '';
    modal.classList.remove('hidden');
}

// Form submission
document.addEventListener('DOMContentLoaded', function() {
    const createProjectBtn = document.getElementById('createProjectBtn');
    const projectModal = document.getElementById('projectModal');
    const projectForm = document.getElementById('projectForm');

    // Show modal when clicking the create button
    createProjectBtn.addEventListener('click', function() {
        projectModal.classList.remove('hidden');
    });

    // Close modal
    window.closeModal = function() {
        projectModal.classList.add('hidden');
    }

    // Handle form submission
    projectForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('name', document.getElementById('name').value);
        formData.append('description', document.getElementById('description').value);
        formData.append('url', document.getElementById('url').value);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

        try {
            const response = await fetch('/projects/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                window.location.reload();
            } else {
                const error = await response.json();
                alert('Error creating project: ' + JSON.stringify(error));
            }
        } catch (error) {
            alert('Error creating project: ' + error);
        }
    });
});