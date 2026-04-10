const API_URL = window.location.origin;

// Load available users for task creation and editing
let availableUsers = [];
async function loadAvailableUsers() {
    try {
        const response = await fetch(`${API_URL}/users/available/list`);
        const data = await response.json();
        availableUsers = data.users || [];
        
        // Update user selector for creating tasks
        const userSelect = document.getElementById('taskUserId');
        if (userSelect) {
            userSelect.innerHTML = '<option value="">-- Seleccionar Usuario --</option>';
            availableUsers.forEach(user => {
                userSelect.innerHTML += `<option value="${user.id}">${user.name}</option>`;
            });
        }
        
        // Update user selector for editing tasks
        const editUserSelect = document.getElementById('editTaskUserId');
        if (editUserSelect) {
            editUserSelect.innerHTML = '<option value="">-- Seleccionar Usuario --</option>';
            availableUsers.forEach(user => {
                editUserSelect.innerHTML += `<option value="${user.id}">${user.name}</option>`;
            });
        }
    } catch (error) {
        console.log('Error cargando usuarios disponibles:', error);
    }
}

// TASKS FUNCTIONS
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const data = await response.json();
        const tasksList = document.getElementById('tasksList');

        if (!data.tasks || data.tasks.length === 0) {
            tasksList.innerHTML = '<div class="empty-state">No hay tareas creadas</div>';
            return;
        }

        tasksList.innerHTML = data.tasks.map(task => {
            const assignedUser = availableUsers.find(u => u.id === task.user_id);
            return `
            <div class="item">
                <div class="item-info">
                    <div class="item-title">${task.content}</div>
                    <div class="item-desc">ID: ${task.id} | ${task.done ? '<i class="fas fa-check-circle"></i> Completada' : '<i class="fas fa-hourglass-start"></i> Pendiente'}</div>
                    <div class="item-desc"><i class="fas fa-user"></i> Encargado: ${assignedUser ? assignedUser.name : 'No asignado'}</div>
                </div>
                <div class="item-actions">
                    <button class="btn-warning" onclick="openEditTaskModal(${task.id}, '${task.content.replace(/'/g, "\\'")}', ${task.done}, ${task.user_id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-warning" onclick="toggleTask(${task.id}, ${!task.done})">
                        <i class="fas fa-${task.done ? 'hourglass-start' : 'check'}"></i>
                    </button>
                    <button class="btn-danger" onclick="deleteTask(${task.id})"><i class="fas fa-trash"></i></button>
                </div>
            </div>
            `;
        }).join('');
    } catch (error) {
        showMessage('tasksMessage', 'Error cargando tareas: ' + error.message, 'error', 'fas fa-warning');
    }
}

async function createTask() {
    const content = document.getElementById('taskContent').value.trim();
    const user_id = document.getElementById('taskUserId').value;
    
    if (!content) {
        showMessage('tasksMessage', 'Por favor escriba algo en la tarea', 'error', 'fas fa-warning');
        return;
    }
    
    if (!user_id) {
        showMessage('tasksMessage', 'Por favor seleccione un usuario', 'error', 'fas fa-warning');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                user_id: parseInt(user_id), 
                content, 
                done: false 
            })
        });
        const data = await response.json();

        if (response.ok) {
            showMessage('tasksMessage', 'Tarea creada correctamente', 'success', 'fas fa-check-circle');
            document.getElementById('taskContent').value = '';
            document.getElementById('taskUserId').value = '';
            loadTasks();
        } else {
            showMessage('tasksMessage', 'Error: ' + data.error, 'error', 'fas fa-warning');
        }
    } catch (error) {
        showMessage('tasksMessage', 'Error: ' + error.message, 'error', 'fas fa-warning');
    }
}

async function toggleTask(id, done) {
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ done })
        });
        if (response.ok) {
            loadTasks();
        }
    } catch (error) {
        showMessage('tasksMessage', 'Error: ' + error.message, 'error', 'fas fa-warning');
    }
}

async function deleteTask(id) {
    if (!confirm('¿Eliminando tarea...?')) return;
    try {
        const response = await fetch(`${API_URL}/tasks/${id}`, { method: 'DELETE' });
        if (response.ok) {
            showMessage('tasksMessage', 'Tarea eliminada', 'success', 'fas fa-check-circle');
            loadTasks();
        }
    } catch (error) {
        showMessage('tasksMessage', 'Error: ' + error.message, 'error', 'fas fa-warning');
    }
}

// USERS FUNCTIONS
async function loadUsers() {
    try {
        const response = await fetch(`${API_URL}/users`);
        const data = await response.json();
        const usersList = document.getElementById('usersList');

        if (!data.users || data.users.length === 0) {
            usersList.innerHTML = '<div class="empty-state">No hay usuarios creados</div>';
            return;
        }

        usersList.innerHTML = data.users.map(user => `
            <div class="item">
                <div class="item-info">
                    <div class="item-title">${user.name} ${user.lastname || ''}</div>
                    <div class="item-desc">ID: ${user.id}</div>
                    <div class="address-section">
                        <i class="fas fa-map-marker-alt"></i> ${user.city || ''}, ${user.country || ''} (${user.postal_code || ''})
                    </div>
                </div>
                <div class="item-actions">
                    <button class="btn-warning" onclick="openEditUserModal(${user.id}, '${user.name.replace(/'/g, "\\'")}', '${(user.lastname || '').replace(/'/g, "\\'")}', '${(user.city || '').replace(/'/g, "\\'")}', '${(user.country || '').replace(/'/g, "\\'")}', '${user.postal_code || ''}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-danger" onclick="deleteUser(${user.id})"><i class="fas fa-trash"></i></button>
                </div>
            </div>
        `).join('');
        
        // Reload available users for task selection
        loadAvailableUsers();
    } catch (error) {
        showMessage('usersMessage', 'Error cargando usuarios: ' + error.message, 'error', 'fas fa-warning');
    }
}

async function createUser() {
    const name = document.getElementById('userName').value.trim();
    const lastname = document.getElementById('userLastname').value.trim();
    const city = document.getElementById('userCity').value.trim();
    const country = document.getElementById('userCountry').value.trim();
    const postal_code = document.getElementById('userPostalCode').value.trim();

    if (!name) {
        showMessage('usersMessage', 'Por favor ingrese un nombre', 'error', 'fas fa-warning');
        return;
    }

    if (postal_code && !/^\d{5}$/.test(postal_code)) {
        showMessage('usersMessage', 'El código postal debe tener exactamente 5 dígitos', 'error', 'fas fa-warning');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name, lastname, city, country, postal_code
            })
        });
        const data = await response.json();

        if (response.ok) {
            showMessage('usersMessage', 'Usuario creado correctamente', 'success', 'fas fa-check-circle');
            document.getElementById('userName').value = '';
            document.getElementById('userLastname').value = '';
            document.getElementById('userCity').value = '';
            document.getElementById('userCountry').value = '';
            document.getElementById('userPostalCode').value = '';
            loadUsers();
        } else {
            showMessage('usersMessage', 'Error: ' + data.error, 'error', 'fas fa-warning');
        }
    } catch (error) {
        showMessage('usersMessage', 'Error: ' + error.message, 'error', 'fas fa-warning');
    }
}

async function deleteUser(id) {
    if (!confirm('¿Eliminar usuario...?')) return;
    try {
        const response = await fetch(`${API_URL}/users/${id}`, { method: 'DELETE' });
        if (response.ok) {
            showMessage('usersMessage', 'Usuario eliminado', 'success', 'fas fa-check-circle');
            loadUsers();
        }
    } catch (error) {
        showMessage('usersMessage', 'Error: ' + error.message, 'error', 'fas fa-warning');
    }
}

// UTILITIES
function showMessage(elementId, message, type, iconClass = null) {
    const element = document.getElementById(elementId);
    element.innerHTML = ''; // Limpiar contenido previo
    element.className = `message ${type}`;
    
    if (iconClass) {
        const icon = document.createElement('i');
        icon.className = iconClass;
        element.appendChild(icon);
        
        const text = document.createElement('span');
        text.textContent = ' ' + message;
        element.appendChild(text);
    } else {
        element.textContent = message;
    }
    
    setTimeout(() => {
        element.className = 'message';
    }, 4000);
}

// EDIT TASK FUNCTIONS
let currentEditTaskId = null;
let currentEditTaskUserId = null;

function openEditTaskModal(taskId, content, done, userId) {
    currentEditTaskId = taskId;
    currentEditTaskUserId = userId;
    document.getElementById('editTaskContent').value = content;
    document.getElementById('editTaskDone').value = done;
    document.getElementById('editTaskUserId').value = userId;
    document.getElementById('editTaskModal').style.display = 'block';
}

function closeEditTaskModal() {
    document.getElementById('editTaskModal').style.display = 'none';
    currentEditTaskId = null;
    currentEditTaskUserId = null;
}

async function saveEditTask() {
    const content = document.getElementById('editTaskContent').value.trim();
    const done = document.getElementById('editTaskDone').value === 'true';
    const user_id = parseInt(document.getElementById('editTaskUserId').value);

    if (!content) {
        showMessage('tasksMessage', 'El contenido no puede estar vacío', 'error', 'fas fa-warning');
        return;
    }

    if (!user_id || user_id <= 0) {
        showMessage('tasksMessage', 'Debe seleccionar un usuario', 'error', 'fas fa-warning');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/${currentEditTaskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content, done, user_id })
        });
        
        if (response.ok) {
            showMessage('tasksMessage', 'Tarea actualizada correctamente', 'success', 'fas fa-check-circle');
            closeEditTaskModal();
            loadTasks();
        } else {
            const data = await response.json();
            showMessage('tasksMessage', `Error: ${data.error}`, 'error', 'fas fa-warning');
        }
    } catch (error) {
        showMessage('tasksMessage', `Error: ${error.message}`, 'error', 'fas fa-warning');
    }
}

// EDIT USER FUNCTIONS
let currentEditUserId = null;

function openEditUserModal(userId, name, lastname, city, country, postalCode) {
    currentEditUserId = userId;
    document.getElementById('editUserName').value = name;
    document.getElementById('editUserLastname').value = lastname;
    document.getElementById('editUserCity').value = city;
    document.getElementById('editUserCountry').value = country;
    document.getElementById('editUserPostalCode').value = postalCode;
    document.getElementById('editUserModal').style.display = 'block';
}

function closeEditUserModal() {
    document.getElementById('editUserModal').style.display = 'none';
    currentEditUserId = null;
}

async function saveEditUser() {
    const name = document.getElementById('editUserName').value.trim();
    const lastname = document.getElementById('editUserLastname').value.trim();
    const city = document.getElementById('editUserCity').value.trim();
    const country = document.getElementById('editUserCountry').value.trim();
    const postal_code = document.getElementById('editUserPostalCode').value.trim();

    if (!name) {
        showMessage('usersMessage', 'Por favor ingrese un nombre', 'error', 'fas fa-warning');
        return;
    }

    if (postal_code && !/^\d{5}$/.test(postal_code)) {
        showMessage('usersMessage', 'El código postal debe tener exactamente 5 dígitos', 'error', 'fas fa-warning');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/users/${currentEditUserId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name, lastname, city, country, postal_code
            })
        });

        if (response.ok) {
            showMessage('usersMessage', 'Usuario actualizado correctamente', 'success', 'fas fa-check-circle');
            closeEditUserModal();
            loadUsers();
        } else {
            const data = await response.json();
            showMessage('usersMessage', `Error: ${data.error}`, 'error', 'fas fa-warning');
        }
    } catch (error) {
        showMessage('usersMessage', `Error: ${error.message}`, 'error', 'fas fa-warning');
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const taskModal = document.getElementById('editTaskModal');
    const userModal = document.getElementById('editUserModal');
    if (event.target === taskModal) {
        taskModal.style.display = 'none';
    }
    if (event.target === userModal) {
        userModal.style.display = 'none';
    }
}

// Load data on startup
window.addEventListener('load', () => {
    loadAvailableUsers();
    loadTasks();
    loadUsers();
});

// TOGGLE LISTS VISIBILITY
function toggleTasksList() {
    const tasksList = document.getElementById('tasksList');
    const icon = document.getElementById('taskToggleIcon');
    const text = document.getElementById('taskToggleText');
    
    if (tasksList.style.display === 'none') {
        tasksList.style.display = 'block';
        icon.className = 'fas fa-eye-slash';
        text.textContent = 'Ocultar';
        loadTasks();
    } else {
        tasksList.style.display = 'none';
        icon.className = 'fas fa-eye';
        text.textContent = 'Mostrar';
    }
}

function toggleUsersList() {
    const usersList = document.getElementById('usersList');
    const icon = document.getElementById('userToggleIcon');
    const text = document.getElementById('userToggleText');
    
    if (usersList.style.display === 'none') {
        usersList.style.display = 'block';
        icon.className = 'fas fa-eye-slash';
        text.textContent = 'Ocultar';
        loadUsers();
    } else {
        usersList.style.display = 'none';
        icon.className = 'fas fa-eye';
        text.textContent = 'Mostrar';
    }
}
