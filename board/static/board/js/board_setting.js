document.addEventListener("DOMContentLoaded", function () {
    const boardData = document.getElementById("board-data");
    const boardId = boardData.dataset.boardId;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    

    // Utility function to handle fetch errors
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

    // Add Column
    function setupAddColumn() {
        const addColumnButton = document.getElementById("add-column-button");
        const addColumnModal = document.getElementById("add-column-modal");
        const addColumnForm = document.getElementById("add-column-form");

        if (addColumnButton && addColumnForm) {
            addColumnButton.addEventListener("click", function () {
                console.log("Add Column button clicked!");
                addColumnModal.style.display = "block";
            });

            addColumnForm.addEventListener("submit", async function (e) {
                e.preventDefault();
                console.log("Form submitted!");

                const columnTitle = addColumnForm.querySelector("input[name='column_title']").value;
                const url = `/boards/${boardId}/columns/create/`;

                const data = await fetchWithErrorHandling(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": csrfToken,
                    },
                    body: new URLSearchParams({ column_title: columnTitle }),
                });

                if (data?.id) {
                    const boardColumns = document.getElementById("board-columns");
                    const newColumn = document.createElement("div");
                    newColumn.classList.add("column");
                    newColumn.dataset.columnId = data.id;
                    newColumn.innerHTML = `
                        <h3>${data.name}</h3>
                        <button class="delete-column-button primary-button" data-column-id="${data.id}">
                            Delete
                        </button>`;
                    boardColumns.appendChild(newColumn);
                    addColumnModal.style.display = "none";
                }
            });
        }
    }

    // Delete Column
    function setupDeleteColumn() {
        document.addEventListener("click", async function (e) {
            if (e.target.classList.contains("delete-column-button")) {
                const columnId = e.target.dataset.columnId;

                // Confirm deletion
                if (!confirm("Are you sure you want to delete this column? This action cannot be undone.")) {
                    return;
                }

                // Make the delete request
                const response = await fetch(`/boards/${boardId}/columns/${columnId}/delete/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                    },
                });

                const data = await response.json();

                if (data.success) {


                    // Re-render the board dynamically
                    const boardColumns = document.getElementById("board-columns");
                    boardColumns.innerHTML = ""; // Clear the current columns

                    // Add the updated columns to the DOM
                    data.columns.forEach((column) => {
                        const columnDiv = document.createElement("div");
                        columnDiv.classList.add("column");
                        columnDiv.dataset.columnId = column.id;
                        columnDiv.innerHTML = `
                            <h3>${column.column_title}</h3>
                            <button class="delete-column-button primary-button" data-column-id="${column.id}">Delete</button>
                        `;
                        boardColumns.appendChild(columnDiv);
                    });
                    // alert(data.message); // Show success message
                } else {
                    alert(data.error); // Display error if tasks exist or another issue occurs
                }
            }
        });
    }

    // Delete Board
    function setupDeleteBoard() {
        document.addEventListener("click", async function (e) {
            if (e.target.classList.contains("delete-board-button")) {
                const boardId = e.target.dataset.boardId;

                if (confirm("Are you sure you want to delete this board? This action cannot be undone.")) {
                    const url = `/boards/${boardId}/delete/`;

                    const data = await fetchWithErrorHandling(url, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": csrfToken,
                        },
                    });

                    if (data?.message) {
                        alert(data.message);
                        e.target.closest("tr").remove();
                    }
                }
            }
        });
    }

    // Drag-and-Drop for Columns
    function setupDragAndDrop() {
        const boardColumns = document.getElementById("board-columns");
        const saveBoardSettingsButton = document.getElementById("save-board-settings-button");

        if (boardColumns && saveBoardSettingsButton) {
            new Sortable(boardColumns, {
                animation: 150,
                onEnd: function () {
                    console.log("Columns reordered temporarily. Click 'Save Board Settings' to persist.");
                    saveBoardSettingsButton.style.display = "block";
                },
            });

            saveBoardSettingsButton.addEventListener("click", async function () {
                const columnIds = Array.from(boardColumns.children).map((column) => column.dataset.columnId);
                const url = `/boards/${boardId}/columns/reorder/`;

                const data = await fetchWithErrorHandling(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                    },
                    body: JSON.stringify({ column_ids: columnIds }),
                });

                if (data?.message) {
                    console.log("Board settings saved successfully.");
                    window.location.href = `/boards/${boardId}/display/`; // Redirect to task display page
                }
            });
        }
    }

    // Initialize all functions
    setupAddColumn();
    setupDeleteColumn();
    setupDeleteBoard();
    setupDragAndDrop();
});

document.addEventListener("DOMContentLoaded", function () {
    const addColumnModal = document.getElementById("add-column-modal");
    const addColumnButton = document.getElementById("add-column-button");

    // Open Modal
    addColumnButton.addEventListener("click", function () {
        addColumnModal.style.display = "flex";
    });

    // Close Modal
    window.closeAddColumnModal = function () {
        addColumnModal.style.display = "none";
    };

    // Close modal when clicking outside the modal content
    window.addEventListener("click", function (e) {
        if (e.target === addColumnModal) {
            addColumnModal.style.display = "none";
        }
    });
});
