

/**
 * Populates a select field with options loaded from a file.
 *
 * This function is reusable and can be used to populate any select element
 * with options sourced from a file. The file should contain one option per line.
 * The file path must be valid and accessible; otherwise, an error will be logged.
 *
 * @param {string} cssSelectorID - The CSS selector of the select element (e.g., '#my-select'). e.g "#" for an id "." for a class
 * @param {string} filePath - The path to the file containing the options list (e.g., 'path/to/options.txt').
 *
 * @example
 * // Populate a select element with ID 'countries' from 'path/to/countries.txt'
 * populateSelectField('#countries', 'path/to/countries.txt');
 *
 * @example
 * // Populate a select element with ID 'categories' from 'path/to/categories.txt'
 * populateSelectField('#categories', 'path/to/categories.txt');
 *
 * @async
 * @throws {Error} Throws an error if the file cannot be loaded, if the selector is invalid,
 * or if the file path is not valid or accessible.
 */
async function populateSelectField(cssSelectorID, filePath) {
    const selectElement = document.querySelector(cssSelectorID);

    if (!selectElement) {
        console.warn(`The element with selector '${cssSelectorID}' wasn't found!!`);
        return;
    }
    try {
        const optionsData = await loadFile(filePath);

        if (optionsData) {
            const options = optionsData.split('\n');

            options.forEach((optionText) => {
                const value = optionText.trim();
                const text = optionText.trim();

                const option = createOption(value, text);
                selectElement.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

/**
 * Creates an option element for a select field.
 *
 * @param {string} value - The value attribute of the option element.
 * @param {string} text - The text content of the option element.
 * @returns {HTMLSelectElement} The created option element.
 */
function createOption(value, text) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = text;
    return option;
}




/**
 * Asynchronously loads the content of a file from the specified file path.
 *
 * @param {string} filePath - The path to the file to be loaded.
 * @returns {Promise<string>} A Promise that resolves with the text content of the file.
 * @throws {Error} Throws an error if there is an issue with fetching or reading the file.
 *
 * @example
 * // how to use it example:
 * try {
 *   const fileContent = await loadFile("path/to/file.txt");
 *   console.log(fileContent); // Display the content of the loaded file
 * } catch (error) {
 *   console.error('Error:', error);
 * }
 */
async function loadFile(filePath) {
    try {
        const response = await fetch(filePath);
        const data    = await response.text();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}


export {populateSelectField}