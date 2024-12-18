document.addEventListener("DOMContentLoaded", function () {
  // const getCookie = (name) => {
  //   const value = `; ${document.cookie}`;
  //   const parts = value.split(`; ${name}=`);
  //   if (parts.length === 2) return parts.pop().split(';').shift();
  // };

  // const csrfToken = getCookie('csrftoken'); // Extract CSRF token from cookie


  // const boardData = document.getElementById("board-data");
  // const boardId = boardData.dataset.boardId; // Extract the board ID
  // // Add Column Button and Modal
  // const addColumnButton = document.getElementById("add-column-button");
  // const addColumnModal = document.getElementById("add-column-modal");
  // const addColumnForm = document.getElementById("add-column-form");
  const boardData = document.getElementById("board-data");
  const boardId = boardData.dataset.boardId;
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Add Column
  const addColumnButton = document.getElementById("add-column-button");
  const addColumnModal = document.getElementById("add-column-modal");
  const addColumnForm = document.getElementById("add-column-form");

  if (addColumnButton) {
      addColumnButton.addEventListener("click", function () {
          console.log("Add Column button clicked!");
          addColumnModal.style.display = "block"; // Show the modal
      });
   }

  if (addColumnForm) {
      addColumnForm.addEventListener("submit", function (e) {
          e.preventDefault();
          console.log("Form submitted!");
          const columnTitle = addColumnForm.querySelector("input[name='column_title']").value;

          fetch(`/boards/${boardId}/columns/create/`, {
              method: "POST",
              headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                  "X-CSRFToken": csrfToken,
              },
              body: new URLSearchParams({ column_title: columnTitle })
          })
              .then(response => response.json())
              .then(data => {
                  if (data.id) {
                      console.log("Column added successfully:", data);

                      // Dynamically add the new column to the board
                      // const boardColumns = document.getElementById("board-columns");
                      const newColumn = document.createElement("div");
                      newColumn.classList.add("column");
                      newColumn.dataset.columnId = data.id;
                      newColumn.innerHTML = `
                        <h3>${data.name}</h3>
                        <button class="delete-column-button" data-column-id="${data.id}">Delete</button>  
                      `;
                      boardColumns.appendChild(newColumn);

                      // Hide the modal
                      addColumnModal.style.display = "none";
                  } else {
                      alert(data.error);
                  }
              })
              .catch(error => {
                  console.error("Error adding column:", error);
              });
      });
  } else {
      console.error("Add Column form not found!");
  }

    // Delete Column
    document.addEventListener("click", function (e) {
      if (e.target.classList.contains("delete-column-button")) {
          const columnId = e.target.dataset.columnId;

          fetch(`/boards/${boardId}/columns/${columnId}/delete/`, {
              method: "POST",
              headers: {
                  "X-CSRFToken": csrfToken,
              },
          })
              .then((response) => response.json())
              .then((data) => {
                  if (data.success) {
                      e.target.closest(".column").remove();
                  } else {
                      alert(data.error);
                  }
              });
      }
  });

  // Drag-and-Drop for Columns
  const boardColumns = document.getElementById("board-columns");
  const saveBoardSettingsButton = document.getElementById("save-board-settings-button");

  new Sortable(boardColumns, {
      animation: 150,
      onEnd: function () {
          console.log("Columns reordered temporarily. Click 'Save Board Settings' to persist.");
          saveBoardSettingsButton.style.display = "block"; // Show Save Settings button
      },
  });

  // // Save Column Order
  // const saveOrderButton = document.getElementById("save-order-button");
  // if (saveOrderButton) {
  //     saveOrderButton.addEventListener("click", function () {
  //         const columnIds = Array.from(boardColumns.children).map(column => column.dataset.columnId);
  //         fetch(`/boards/${boardId}/columns/reorder/`, {
  //             method: "POST",
  //             headers: {
  //                 "Content-Type": "application/json",
  //                 "X-CSRFToken": "{{ csrf_token }}"
  //             },
  //             body: JSON.stringify({ column_ids: columnIds })
  //         })
  //             .then(response => response.json())
  //             .then(data => {
  //                 if (data.message) {
  //                     saveOrderButton.style.display = "none";
  //                     alert("Column order saved!");
  //                 }
  //             })
  //             .catch(error => console.error("Error saving column order:", error));
  //     });
  // }


  // Save Board Settings and Redirect
  // const saveBoardSettingsButton = document.getElementById("save-board-settings-button");
  if (saveBoardSettingsButton) {
    saveBoardSettingsButton.addEventListener("click", function () {
        const columnIds = Array.from(boardColumns.children).map((column) => column.dataset.columnId);

        fetch(`/boards/${boardId}/columns/reorder/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ column_ids: columnIds }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.message) {
                    console.log("Board settings saved successfully.");
                    window.location.href = `/boards/${boardId}/display/`; // Redirect to task display page
                }
            })
            .catch((error) => console.error("Error saving board settings:", error));
    });
  }   
});
