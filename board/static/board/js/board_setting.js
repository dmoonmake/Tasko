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

    // Utility: Fetch all columns and render
    async function fetchAndRenderColumns() {
        const url = `/boards/${boardId}/columns/`; // Endpoint to fetch all columns
        const data = await fetchWithErrorHandling(url, { method: "GET" });

        if (data?.columns) {
            const boardColumns = document.getElementById("board-columns");
            boardColumns.innerHTML = ""; // Clear current columns

            // Render all columns dynamically
            data.columns.forEach((column) => {
                addColumnToBoard(column);
            });
        }
    }

    // Utility: Add column dynamically
    function addColumnToBoard(column) {
        const boardColumns = document.getElementById("board-columns");
        const columnDiv = document.createElement("div");
        columnDiv.classList.add("kanban-column"); // Add your column class
        columnDiv.dataset.columnId = column.id; // Set column ID
        // columnDiv.style.border = "1px solid #ccc"; // Add inline styles if needed
        // columnDiv.style.padding = "10px";

        columnDiv.innerHTML = `
            <h3>${column.column_title}</h3>
            <button class="delete-column-button secondary-button" data-column-id="${column.id}">
                -
            </button>
        `;
        boardColumns.appendChild(columnDiv);

        // Reinitialize drag-and-drop after adding the column
        initializeDragAndDrop();

        // Ensure the secondary button styling is applied immediately
        const deleteButton = columnDiv.querySelector(".delete-column-button");
        if (deleteButton) {
            deleteButton.classList.add("secondary-button"); // Ensure class is applied dynamically
        }
    }

    // Save Board Settings and Redirect
    async function saveBoardSettings() {
        const boardColumns = document.getElementById("board-columns");
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
            console.log("Board settings saved successfully. Redirecting...");
            window.location.href = `/boards/${boardId}/display/`; // Redirect after saving
        }
    }

    // Initialize Drag-and-Drop
    function initializeDragAndDrop() {
        const boardColumns = document.getElementById("board-columns");
        const saveBoardSettingsButton = document.getElementById("save-board-settings-button");
        const boardId = boardColumns.dataset.boardId; // Ensure boardId is set

        if (!boardId) {
            console.error("Board ID is missing.");
            return;
        }

        if (boardColumns) {
            new Sortable(boardColumns, {
                animation: 150,
                onEnd: function () {
                    console.log("Columns reordered. Click 'Save Board Settings' to persist.");
                    saveBoardSettingsButton.style.display = "block";
                },
            });

            saveBoardSettingsButton.addEventListener("click", saveBoardSettings);
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
                    await fetchAndRenderColumns(); 
                    addColumnModal.style.display = "none"; // Close the modal
                    addColumnForm.reset(); // Reset the form
                }
            });
        }

        // Close modal functionality
        window.closeAddColumnModal = function () {
            addColumnModal.style.display = "none";
        };

        window.addEventListener("click", (e) => {
            if (e.target === addColumnModal) {
                closeAddColumnModal();
            }
        });
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
                    await fetchAndRenderColumns(); 
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
    // function setupDragAndDrop() {
    //     const boardColumns = document.getElementById("board-columns");
    //     const saveBoardSettingsButton = document.getElementById("save-board-settings-button");

    //     if (boardColumns && saveBoardSettingsButton) {
    //         new Sortable(boardColumns, {
    //             animation: 150,
    //             onEnd: function () {
    //                 console.log("Columns reordered temporarily. Click 'Save Board Settings' to persist.");
    //                 saveBoardSettingsButton.style.display = "block";
    //             },
    //         });

    //         saveBoardSettingsButton.addEventListener("click", async function () {
    //             const columnIds = Array.from(boardColumns.children).map((column) => column.dataset.columnId);
    //             const url = `/boards/${boardId}/columns/reorder/`;

    //             const data = await fetchWithErrorHandling(url, {
    //                 method: "POST",
    //                 headers: {
    //                     "Content-Type": "application/json",
    //                     "X-CSRFToken": csrfToken,
    //                 },
    //                 body: JSON.stringify({ column_ids: columnIds }),
    //             });

    //             if (data?.message) {
    //                 console.log("Board settings saved successfully.");
    //                 window.location.href = `/boards/${boardId}/display/`; // Redirect to task display page
    //             }
    //         });
    //     }
    // }

    // Initialize all functions
    setupAddColumn();
    setupDeleteColumn();
    setupDeleteBoard();
    // setupDragAndDrop();
    initializeDragAndDrop();
    
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
