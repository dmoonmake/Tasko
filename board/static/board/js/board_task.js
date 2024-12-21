document.addEventListener("DOMContentLoaded", function () {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Utility: Fetch Wrapper
  async function fetchWithErrorHandling(url, options) {
      try {
          const response = await fetch(url, options);
          const data = await response.json();
          if (!response.ok) throw new Error(data.error || "An error occurred");
          return data;
      } catch (error) {
          console.error("Error:", error.message);
          alert(error.message);
      }
  }

  // Modal Handling
  const addTaskModal = document.getElementById("add-task-modal");
  const columnInput = document.getElementById("column-id");
  const addTaskForm = document.getElementById("add-task-form");

  function openAddTaskModal(columnId) {
      console.log("Add Task button clicked for column ID:", columnId);
      columnInput.value = columnId;
      addTaskModal.style.display = "block";
  }

  function closeAddTaskModal() {
      addTaskModal.style.display = "none";
  }

  // Event Listeners for + Buttons
  function setupAddTaskButtons() {
      document.querySelectorAll(".add-task-button").forEach((button) => {
          button.addEventListener("click", function () {
              const columnId = this.closest(".kanban-column").dataset.columnId;
              openAddTaskModal(columnId);
          });
      });
  }

  // Add Task Form Submission
  addTaskForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const columnId = columnInput.value;
      const formData = new FormData(addTaskForm);
      const url = `/boards/${columnId}/create-task/`;

      const data = await fetchWithErrorHandling(url, {
          method: "POST",
          headers: {
              "X-CSRFToken": csrfToken,
          },
          body: new URLSearchParams(formData),
      });

      if (data && data.message) {
          const taskContainer = document.getElementById(`tasks-column-${columnId}`);
          const taskCard = document.createElement("div");
          taskCard.classList.add("task-card");
          taskCard.dataset.taskId = data.task_id;
          taskCard.draggable = true;
          taskCard.innerHTML = `
              <h4>${data.task_title}</h4>
              <p>Status: ${data.task_status}</p>
          `;
          taskContainer.appendChild(taskCard);
          // Make the new task draggable
          makeTaskDraggable(taskCard);
          initializeTaskDragging();
          
          closeAddTaskModal();
      }
  });

  // Drag-and-Drop Setup
  function setupDragAndDrop() {
      document.querySelectorAll(".task-card").forEach((task) => {
        makeTaskDraggable(task); // Use the reusable function
      });

      document.querySelectorAll(".task-container").forEach((container) => {
          container.addEventListener("dragover", (e) => e.preventDefault());

          container.addEventListener("drop", async (e) => {
              e.preventDefault();
              const taskId = e.dataTransfer.getData("taskId");
              const columnId = container.closest(".kanban-column").dataset.columnId;

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
                        container.appendChild(task); // Dynamically move the task in the DOM

                        // Update task status dynamically
                        const statusText = task.querySelector(".task-status");
                        if (statusText) {
                            statusText.textContent = `Status: ${data.task_status}`;
                        }
                        // Reinitialize dragstart event
                        initializeTaskDragging();

                        console.log("Task moved successfully:", data.message);
                    } else {
                        alert(data.error);
                    }
                })
                .catch((error) => console.error("Error moving task:", error));
          });
      });
  }

  function initializeTaskDragging() {
    document.querySelectorAll(".task-card").forEach((task) => {
        // task.addEventListener("dragstart", (e) => {
        //     e.dataTransfer.setData("taskId", task.dataset.taskId);
        // });
        makeTaskDraggable(task); // Use the reusable function
    });
  }

  function makeTaskDraggable(taskElement) {
    taskElement.addEventListener("dragstart", (e) => {
        e.dataTransfer.setData("taskId", taskElement.dataset.taskId);
    });
  }
    


  // Initialize All Functions
  setupAddTaskButtons();
  setupDragAndDrop();
});
