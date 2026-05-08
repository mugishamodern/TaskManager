let currentFilter = 'all';
let tasks = [];

// Load tasks on page load
window.addEventListener('DOMContentLoaded', loadTasks);

// Allow Enter key to add task
document.addEventListener('DOMContentLoaded', function() {
    const taskInput = document.getElementById('taskInput');
    taskInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTask();
        }
    });
});

async function loadTasks() {
    try {
        const response = await fetch('/tasks');
        tasks = await response.json();
        renderTasks();
        updateStats();
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

async function addTask() {
    const taskInput = document.getElementById('taskInput');
    const title = taskInput.value.trim();

    if (!title) {
        alert('Please enter a task!');
        return;
    }

    try {
        const response = await fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title })
        });

        if (response.ok) {
            taskInput.value = '';
            loadTasks();
        } else {
            alert('Error adding task');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function completeTask(id) {
    try {
        const response = await fetch(`/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function deleteTask(id) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    try {
        const response = await fetch(`/tasks/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function renderTasks() {
    const tasksList = document.getElementById('tasksList');
    const emptyState = document.getElementById('emptyState');
    
    tasksList.innerHTML = '';

    let filteredTasks = tasks;
    if (currentFilter === 'active') {
        filteredTasks = tasks.filter(t => !t.completed);
    } else if (currentFilter === 'completed') {
        filteredTasks = tasks.filter(t => t.completed);
    }

    if (filteredTasks.length === 0) {
        emptyState.classList.remove('hidden');
        return;
    }

    emptyState.classList.add('hidden');

    filteredTasks.forEach(task => {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''}`;
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'task-checkbox';
        checkbox.checked = task.completed;
        checkbox.onchange = () => completeTask(task.id);

        const text = document.createElement('span');
        text.className = 'task-text';
        text.textContent = task.title;

        const actions = document.createElement('div');
        actions.className = 'task-actions';

        if (!task.completed) {
            const completeBtn = document.createElement('button');
            completeBtn.className = 'btn-small btn-complete';
            completeBtn.textContent = '✓ Done';
            completeBtn.onclick = () => completeTask(task.id);
            actions.appendChild(completeBtn);
        }

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn-small btn-delete';
        deleteBtn.textContent = '🗑️ Delete';
        deleteBtn.onclick = () => deleteTask(task.id);
        actions.appendChild(deleteBtn);

        li.appendChild(checkbox);
        li.appendChild(text);
        li.appendChild(actions);
        tasksList.appendChild(li);
    });
}

function filterTasks(filter) {
    currentFilter = filter;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`filter-${filter}`).classList.add('active');
    
    renderTasks();
}

function updateStats() {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const pending = total - completed;

    document.getElementById('totalTasks').textContent = total;
    document.getElementById('completedTasks').textContent = completed;
    document.getElementById('pendingTasks').textContent = pending;
}
