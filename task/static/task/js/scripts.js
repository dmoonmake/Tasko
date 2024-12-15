// Initialize Sortable.js for each task container
const todoContainer = document.getElementById('todo');
const inProgressContainer = document.getElementById('inprogress');
const doneContainer = document.getElementById('done');

[todoContainer, inProgressContainer, doneContainer].forEach(container => {
    new Sortable(container, {
        group: 'shared', // Allows dragging between containers
        animation: 150, // Smooth animation
        onEnd: function (evt) {
            const taskId = evt.item.dataset.id; // Get task ID from data attribute
            const newStatus = evt.to.id; // Get the new container's ID (todo, inprogress, done)
            
            // Send the updated status to the server
            updateTaskStatus(taskId, newStatus);
        }
    });
});

// Function to update task status on the server
function updateTaskStatus(taskId, newStatus) {
    fetch(`/tasks/update-status/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Include CSRF token
        },
        body: JSON.stringify({ id: taskId, status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log server response
    })
    .catch(error => console.error('Error updating task status:', error));
}

// Helper function to get CSRF token
function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Open the modal and load task details
function openTaskDetails(taskId) {
    // Get the modal
    const modal = document.getElementById('taskModal');
    const taskDetails = document.getElementById('taskDetails');

    // Show the modal
    modal.style.display = 'block';

    // Fetch task details via AJAX
    fetch(`/tasks/${taskId}/`)
        .then(response => response.json())
        .then(data => {
            // Populate the modal with task details
            taskDetails.innerHTML = `
                <h2>${data.task_title}</h2>
                <p><strong>Description:</strong> ${data.task_description}</p>
                <p><strong>Status:</strong> ${data.task_status}</p>
                <p><strong>Created At:</strong> ${data.task_created_at}</p>
                <a href="/tasks/edit/${taskId}/">Edit</a> |
                <a href="/tasks/delete/${taskId}/">Delete</a>
            `;
        })
        .catch(error => console.error('Error fetching task details:', error));
}

// // Open the modal and load task details
// function openTaskDetails(taskId) {
//     // Get the modal and task details container
//     const modal = document.getElementById('taskModal');
//     const taskDetails = document.getElementById('taskDetails');

//     // Show the modal
//     modal.style.display = 'block';

//     // Fetch task details via AJAX
//     fetch(`/tasks/${taskId}/`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Failed to fetch task details');
//             }
//             return response.json();
//         })
//         .then(data => {
//             // Populate the modal with task details
//             taskDetails.innerHTML = `
//                 <h2>${data.task_title}</h2>
//                 <p><strong>Description:</strong> ${data.task_description}</p>
//                 <p><strong>Status:</strong> ${data.task_status}</p>
//                 <p><strong>Created At:</strong> ${data.task_created_at}</p>
//                 <a href="/tasks/edit/${taskId}/">Edit</a> |
//                 <a href="/tasks/delete/${taskId}/">Delete</a>
//             `;
//         })
//         .catch(error => {
//             // Handle errors and display a message in the modal
//             console.error('Error fetching task details:', error);
//             taskDetails.innerHTML = `<p style="color: red;">Failed to load task details. Please try again.</p>`;
//         });
// }

// Close the modal
function closeTaskDetails() {
    const modal = document.getElementById('taskModal');
    modal.style.display = 'none';
}

