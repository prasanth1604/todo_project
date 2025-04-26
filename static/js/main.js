document.addEventListener('DOMContentLoaded', function() {
    // API endpoints
    const API_URL = '/tasks/api/';
    
    // DOM elements
    const tasksList = document.getElementById('tasksList');
    const searchInput = document.getElementById('searchInput');
    const dateFilter = document.getElementById('dateFilter');
    const sortByDateBtn = document.getElementById('sortByDate');
    const saveTaskBtn = document.getElementById('saveTask');
    const updateTaskBtn = document.getElementById('updateTask');
    
    // Load tasks on page load
    loadTasks();
    
    // Event listeners
    searchInput.addEventListener('input', debounce(loadTasks, 500));
    dateFilter.addEventListener('change', loadTasks);
    sortByDateBtn.addEventListener('click', toggleSortByDate);
    saveTaskBtn.addEventListener('click', saveTask);
    updateTaskBtn.addEventListener('click', updateTask);
    
    // Load tasks with filters
    function loadTasks() {
        let url = API_URL;
        const params = new URLSearchParams();
        
        if (searchInput.value) {
            params.append('search', searchInput.value);
        }
        
        if (dateFilter.value) {
            params.append('date', dateFilter.value);
        }
        
        if (sortByDateBtn.classList.contains('active')) {
            params.append('sort', 'asc');
        }
        
        if (params.toString()) {
            url += '?' + params.toString();
        }
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                displayTasks(data);
            })
            .catch(error => console.error('Error:', error));
    }
    
    // Display tasks in the UI
    function displayTasks(tasks) {
        tasksList.innerHTML = '';
        tasks.forEach(task => {
            const taskElement = createTaskElement(task);
            tasksList.appendChild(taskElement);
        });
    }
    
    // Create task element
    function createTaskElement(task) {
        const col = document.createElement('div');
        col.className = 'col-md-4 mb-4';
        col.innerHTML = `
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">${task.title}</h5>
                    <p class="card-text">${task.description}</p>
                    <p class="text-muted">Created: ${new Date(task.creation_date).toLocaleDateString()}</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-sm btn-primary edit-task" data-id="${task.id}">Edit</button>
                    <button class="btn btn-sm btn-danger delete-task" data-id="${task.id}">Delete</button>
                </div>
            </div>
        `;
        
        // Add event listeners for edit and delete buttons
        col.querySelector('.edit-task').addEventListener('click', () => openEditModal(task));
        col.querySelector('.delete-task').addEventListener('click', () => deleteTask(task.id));
        
        return col;
    }
    
    // Save new task
    function saveTask() {
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        
        fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ title, description })
        })
        .then(response => response.json())
        .then(() => {
            closeModal('addTaskModal');
            loadTasks();
        })
        .catch(error => console.error('Error:', error));
    }
    
    // Update task
    function updateTask() {
        const id = document.getElementById('editTaskId').value;
        const title = document.getElementById('editTitle').value;
        const description = document.getElementById('editDescription').value;
        
        fetch(`${API_URL}${id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ title, description })
        })
        .then(response => response.json())
        .then(() => {
            closeModal('editTaskModal');
            loadTasks();
        })
        .catch(error => console.error('Error:', error));
    }
    
    // Delete task
    function deleteTask(id) {
        if (confirm('Are you sure you want to delete this task?')) {
            fetch(`${API_URL}${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(() => loadTasks())
            .catch(error => console.error('Error:', error));
        }
    }
    
    // Open edit modal
    function openEditModal(task) {
        document.getElementById('editTaskId').value = task.id;
        document.getElementById('editTitle').value = task.title;
        document.getElementById('editDescription').value = task.description;
        new bootstrap.Modal(document.getElementById('editTaskModal')).show();
    }
    
    // Close modal
    function closeModal(modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        modal.hide();
        document.getElementById(modalId).querySelector('form').reset();
    }
    
    // Toggle sort by date
    function toggleSortByDate() {
        sortByDateBtn.classList.toggle('active');
        loadTasks();
    }
    
    // Utility function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Utility function for debouncing
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}); 