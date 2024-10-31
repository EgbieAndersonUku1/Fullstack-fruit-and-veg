import { validateElement } from "../errors/customErrors.js";


/**
 * Handles the clicking of the cells in the UI. This function 
 * manages two main functionalities: 
 * 
 * 1. Highlights the entire row when any cell in that row is clicked.
 * 2. Deletes the column when the corresponding header cell is clicked.
 * 
 * The highlighting is achieved by adding or removing a CSS class 
 * from the targeted row. The deletion of the column affects all rows 
 * in the specified column. For this functionality to work, ensure that you 
 * have the following CSS selectors in your CSS file: 
 * 
 * #<the id of your HTML table here> tr.yellow-bg {
 *   background: yellow;
 *   color: black;
 * }
 *
 * This function should only be used as part of an event listener for a table, 
 * because it specifically designed for highlighting rows and deleting columns. 
 * To use it, ensure that you have a table element with an event listener 
 * that listens for `click` events, and attach this function to that listener.
 * 
 * @param {Event} e - The click event object triggered by the user's action.
 * @returns {void} - This function does not return a value.
 * 
 * Example usage:
 * 
 * 1. Import the function `handleTableInteractions` from the utils file or 
 *    wherever it is located.
 * 
 * 2. Get the table you wish to manipulate:
 *    ```javascript
 *    const table = document.getElementById("someTableId");
 *    ```
 * 
 * 3. Create the event listener for the specified table and attach the function:
 *    ```javascript
 *    table.addEventListener("click", handleTableInteractions);
 *    ```
 * 
 * After refreshing the HTML page, clicking on any cell will highlight that 
 * entire row, and clicking the header of the table will delete the corresponding 
 * column.
 * 
 * /**
 * Note: The changes made by this function are not permanent. Once the page is refreshed,
 * any modifications will be reverted. The primary purpose of this function is to allow 
 * users to highlight rows or delete columns, enabling them to focus on specific rows 
 * or compare columns more effectively without altering the original table.
 */
export default function handleTableInteractions(e) {

    const cellTarget     = e.target;
    const cellBodyType   = "TD";
    const cellHeaderType = "TH";

    if (cellTarget.nodeName === cellBodyType ) {
        const row = cellTarget.closest("tr");
        highlightRow(row);
    } else if (cellTarget.nodeName === cellHeaderType) {
        deleteColumn(cellTarget);
    }
   
};


/**
 * Takes a given row and highlights that row
 * @param {*} row : The row that will be highlighted
 */
function highlightRow(row) {
    validateElement(row, "This not a valid row html element", true);

    if (row.classList.contains("yellow-bg")) {
        row.classList.remove("yellow-bg");
        console.log("removing yellow background");
    } else {
        row.classList.add("yellow-bg");
        console.log("Adding yellow background");
    }
}


/**
 * Takes the header for a given table and deletes the entire column 
 * 
 * @param {*} th The header which will be used to delete that entire column
 */
function deleteColumn(th) {

    validateElement(th, "This not a valid column html element", true);
    
    const columnIndex = th.cellIndex;
    const table       = th.closest("table");
  
  
    for (let row of table.rows) {
        if (row.cells.length > columnIndex) {
            row.deleteCell(columnIndex);
        };
      
    };
};

