/**
 * Retrieves all form entries from a given form element.
 *
 * This function creates a `FormData` object from the provided form element
 * and converts it into a plain JavaScript object where each key is a form field name
 * and each value is the corresponding field value.
 *
 * @param {HTMLFormElement} form - The form element to extract data from.
 * @returns {Object} An object where each key is a form field name and each value is the field's value.
 */
function getFormEntries(form) {
    const formData = new FormData(form);
    const formEntries = {};

    for (const [key, value] of formData.entries()) {
        formEntries[key] = value;
    }

    return formEntries;
}


/**
 * Toggles the visibility of an input field and its label based on the user's selection from a dropdown.
 * 
 * This function updates the display properties of a label and an input field depending on whether
 * the selected value from the dropdown matches the specified `valueType`. If the selected value
 * matches `valueType`, the input field and its label will be displayed; otherwise, they will be hidden.
 * 
 * How It Works?:
 * 
 * - If the user selects a value from the dropdown that matches the `valueType` parameter, the input
 *   field and its associated label will be shown.
 * - If the selected value does not match the `valueType`, the input field and its label will be hidden.
 * 
 * **Parameters**:
 * - `selectElement` (HTMLElement): The select element whose value determines the visibility of other elements.
 * - `newCategoryLabelElement` (HTMLElement): The label element to be shown or hidden based on the selection.
 * - `newCategoryInputElement` (HTMLElement): The input field element to be shown or hidden based on the selection.
 * - `valueType` (string, optional): The value to compare against the select element's value. Defaults to `"new"`. 
 *    This value should match one of the options in the dropdown, but it can be any valid option.
 * 
 * **Throws**:
 * - Throws an error if any of the elements are missing or if `valueType` is not a string.
 * 
 * **Example**:
 * 
 * To illustrate, consider the following HTML setup with a select dropdown list, an input field, and a label:
 * 
 * ```html
 * 
 * <label for="discount-select">Add Discount:</label>
 * <select id="discount-select">
 *     <option value="">Select an option</option>
 *     <option value="yes">Yes</option>
 *     <option value="no">No</option>
 * </select>
 * 
 * <label id="discount-label" style="display: none;">Enter Discount Amount:</label>
 * <input id="discount-input" style="display: none;" type="text" placeholder="Discount Amount">
 * 
 * ```
 * 
 * When using this function, you need to attach it to a change event listener on the select element to
 * respond to user selections in real-time. For example:
 * 
 * ```javascript
 * const selectElement = document.getElementById('discount-select');
 * const labelElement = document.getElementById('discount-label');
 * const inputElement = document.getElementById('discount-input');
 * 
 * // Function call: The function must be used within an event listener to detect changes in real-time.
 * selectElement.addEventListener('change', () => 
 * 
 *     // 'yes' is used as valueType here howver it can be any valid 'value' option from the dropdown.
 *     toggleInputVisibilityBasedOnSelection(selectElement, labelElement, inputElement, 'yes') 
 * 
 * );
 * ```
 * 
 * - **If "Yes" is selected**: The input field and label will appear.
 * - **If "No" or any other option is selected**: The input field and label will be hidden.
 */
function toggleInputVisibilityBasedOnSelection(selectElement, newCategoryLabelElement, newCategoryInputElement, valueType = "new") {
    if (!selectElement || !newCategoryLabelElement || !newCategoryInputElement) {
        console.error('One or more elements are missing.');
        return;
    }

    if (typeof valueType !== 'string') {
        console.error('Invalid valueType provided. It should be a string.');
        return;
    }

    const value = selectElement.value.toLowerCase();

    try {
       
        if (value.toLowerCase() === valueType.toLowerCase()) {
            newCategoryLabelElement.style.display = "block";
            newCategoryInputElement.style.display = "block";
            newCategoryInputElement.value = "";
            newCategoryInputElement.required = true;
        } else {
            newCategoryLabelElement.style.display = "none";
            newCategoryInputElement.style.display = "none";
            newCategoryInputElement.value = "N/A";
            newCategoryInputElement.required = false;
        }
    } catch (error) {
        console.error('An error occurred while handling the select change:', error);
    }
}



export {
    getFormEntries,
    toggleInputVisibilityBasedOnSelection
}