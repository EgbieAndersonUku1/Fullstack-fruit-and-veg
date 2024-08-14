/**
 * Creates a table row element with table header cells based on the provided list of header names.
 *
 * @param {string[]} headersList - An array of strings representing the header names for the table.
 * @returns {HTMLTableRowElement} The table row element containing the header cells.
 * @throws {Error} If headersList is not an array of strings.
 *
 * @example
 * // Creates a table header row with specified headers and appends it to an existing table
 * const headers = ["Product ID", "Product Name", "Purchase Date", "Review Status", "Action", "Product Image"];
 * const tableHeaderRow = createTableHeaderRow(headers);
 * document.querySelector("table").appendChild(tableHeaderRow);
 *
 * @example
 * // Creates a table header row for a different set of headers
 * const headers = ["Name", "Age", "Email"];
 * const tableHeaderRow = createTableHeaderRow(headers);
 * document.querySelector("table").appendChild(tableHeaderRow);
 */
function createTableHeaderRow(headersList) {
    if (!Array.isArray(headersList)) {
        throw new Error("The headerList must be a list of strings");
    }

    const tableMainRow = document.createElement("tr");

    headersList.forEach(header => {
        const tableHeader = document.createElement("th");
        tableHeader.textContent = header;
        tableMainRow.appendChild(tableHeader);
    });

    return tableMainRow;
}

/**
 * Creates a table row element with data cells and optionally appends additional elements to specific cells.
 *
 * This function constructs a `<tr>` element where each cell (`<td>`) is populated with data from the `listOfDataColumns` array. 
 * Optional, it supports appending extra elements to specific cells, as specified by the `additionalInformation` object.
 *
 * The `additionalInformation` object maps column indices (0-based) to elements that should be appended to those cells. For example, 
 * if you want to append a link to the cell in column 4 of the row, you would provide an object like `{ 4: document.createElement("a") }`. 
 * If no additional element is specified for a column, the data from `listOfDataColumns` will be used as the cell content.
 *
 * @param {Array<string>} listOfDataColumns - An array of data values for the table cells. Each value corresponds to a cell in the row.
 * @param {Object} [additionalInformation={}] - An optional object where keys are column indices (0-based) and values are elements 
 *                                              to be appended to those specific cells.
 *
 * @returns {HTMLTableRowElement} The constructed table row element containing the data cells.
 *
 * @throws {Error} If `listOfDataColumns` is not an array.
 *
 * @example
 * // Creates a table row where the fifth column has a link element and other columns contain text data
 * const listOfDataColumns = ["Data 1", "Data 2", "Data 3", "Data 4", "Data 5", "Data 6"];
 * const link = document.createElement("a");
 * link.href = "http://example.com";
 * link.textContent = "Add/Edit";
 * 
 * const additionalInformation = { 4: link }; // Append link to column 5 (index 4)
 * const tableRow = createTableRow(listOfDataColumns, additionalInformation);
 * 
 * document.querySelector("table").appendChild(tableRow);
 */
function createTableRow(listOfDataColumns, additionalInformation = {}) {
    const tableMainRow = document.createElement("tr");

    if (!Array.isArray(listOfDataColumns)) {
        throw new Error("The columns must be an array");
    }

    listOfDataColumns.forEach((data, index) => {
        const row = document.createElement("td");

        if (additionalInformation[index]) {
            row.appendChild(additionalInformation[index]);
        } else {
            row.textContent = data;
        }

        tableMainRow.appendChild(row);
    });

    return tableMainRow;
}



export { createTableHeaderRow, createTableRow};