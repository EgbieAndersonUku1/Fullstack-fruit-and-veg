/**
 * Sets up input handlers for the specified form field and icon.
 * @param {string} fieldSelector - CSS selector for the input field.
 * @param {string} iconSelector - CSS selector for the icon.
 */
function handleFormFieldElement(fieldSelector, iconSelector) {
    const inputFieldElement = document.querySelector(fieldSelector);
    const iconElement = document.querySelector(iconSelector);

    if (!inputFieldElement || !iconElement) {
        console.error("Error: Input field or icon element not found.");
        return;
    }
    setupInputHandlers(inputFieldElement, iconElement);
}

/**
 * Adds event listeners for keydown and blur events to the specified elements.
 * @param {HTMLElement} element - The input field element.
 * @param {HTMLElement} elementIcon - The icon element.
 */
function setupInputHandlers(element, elementIcon) {
    if (!isElementValid(element) || !isElementValid(elementIcon)) {
       console.error("Error: Invalid element or icon element.");
       return;
    } 

    element.addEventListener("keydown", (e) => handleInputEvent(e, elementIcon, element));
    element.addEventListener("blur", (e) => handleInputEvent(e, elementIcon, element));
}

/**
 * Handles input events and toggles the display of the icon element.
 * @param {Event} e - The event object.
 * @param {HTMLElement} elementIcon - The icon element.
 * @param {HTMLElement} element - The input field element.
 */
function handleInputEvent(e, elementIcon, element) {
    if (e.key === "Enter" || (e.type === "blur" && element.value)) {
        elementIcon.style.display = "flex";
    } else {
        elementIcon.style.display = "none";
    }
}





/**
 * Validates if the element is a valid DOM element.
 * @param {any} element - The element to validate.
 * @returns {boolean} True if the element is valid, false otherwise.
 */
function isElementValid(element) {
    return !!element && element instanceof Element;
}

export {
    handleFormFieldElement,

};

