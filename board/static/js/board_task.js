document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".add-task-form").forEach((form) => {
      form.addEventListener("submit", function (e) {
          e.preventDefault();

          const columnId = form.dataset.columnId;
          const taskTitle = form.querySelector("input[name='task_title']").value;
          const assignedTo = form.querySelector("select[name='assigned_to']").value;
          const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

          fetch(`/boards/${columnId}/add-task/`, {
              method: "POST",
              headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                  "X-CSRFToken": csrfToken,
              },
              body: new URLSearchParams({
                  task_title: taskTitle,
                  assigned_to: assignedTo,
              }),
          })
              .then((response) => response.json())
              .then((data) => {
                  if (data.message) {
                      const taskList = document.getElementById(`tasks-column-${columnId}`);
                      const newTask = document.createElement("li");
                      newTask.textContent = `${data.task_title} ${
                          data.assigned_to ? `(Assigned to: ${data.assigned_to})` : "(Unassigned)"
                      }`;
                      taskList.appendChild(newTask);

                      // Clear the form
                      form.reset();
                  } else {
                      alert(data.error);
                  }
              })
              .catch((error) => console.error("Error adding task:", error));
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Enable dragging for tasks
  document.querySelectorAll(".task-card").forEach((task) => {
      task.addEventListener("dragstart", (e) => {
          e.dataTransfer.setData("taskId", task.dataset.taskId);
      });
  });

  // Enable dropping for columns
  document.querySelectorAll(".task-container").forEach((container) => {
      container.addEventListener("dragover", (e) => {
          e.preventDefault(); // Allow drop
      });

      container.addEventListener("drop", (e) => {
          e.preventDefault();
          const taskId = e.dataTransfer.getData("taskId");
          const columnId = container.closest(".kanban-column").dataset.columnId;

          // Send POST request to update the task's column
          fetch("/boards/move-task/", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": csrfToken,
              },
              body: JSON.stringify({ task_id: taskId, column_id: columnId }),
          })
              .then((response) => response.json())
              .then((data) => {
                  if (data.message) {
                      const task = document.querySelector(`[data-task-id="${taskId}"]`);
                      container.appendChild(task); // Move the task to the new column
                      // Update the task's status dynamically
                      const statusText = task.querySelector(".task-status");
                      if (statusText) {
                        statusText.textContent = `Status: ${data.task_status}`;
                    }
                  } else {
                      alert(data.error);
                  }
              })
              .catch((error) => console.error("Error moving task:", error));
      });
  });
});
