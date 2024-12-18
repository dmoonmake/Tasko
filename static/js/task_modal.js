function openTaskModal(taskId) {
  const modal = document.getElementById("task-modal");
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch(`/tasks/${taskId}/detail/`, {
      method: "GET",
      headers: {
          "X-CSRFToken": csrfToken,
      },
  })
      .then((response) => response.json())
      .then((data) => {
          document.getElementById("task-modal-title").textContent = data.task_title;
          document.getElementById("task-modal-description").textContent = data.task_description || "No description provided.";
          document.getElementById("task-modal-status").textContent = data.task_status;
          document.getElementById("task-modal-priority").textContent = data.task_priority;
          document.getElementById("task-modal-deadline").textContent = data.task_deadline || "No deadline set.";
          document.getElementById("task-modal-assigned-to").textContent = data.task_assigned_to || "Unassigned";

          // Update Edit and Delete Links
          document.getElementById("edit-task-link").href = `/tasks/edit/${data.task_id}/`;
          document.getElementById("delete-task-form").action = `/tasks/delete/${data.task_id}/`;

          // Show the modal
          modal.style.display = "block";
      })
      .catch((error) => {
          console.error("Error fetching task details:", error);
          alert("Failed to fetch task details.");
      });
}

function closeTaskModal() {
  const modal = document.getElementById("task-modal");
  modal.style.display = "none";
}
