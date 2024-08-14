/**
 * Validates whether the provided element is a valid HTML element.
 *
 * @param {HTMLElement} element - The element to validate.
 * @param {string} errorMsg - The error message to display or throw if validation fails.
 * @param {boolean} [shouldThrow=false] - If true, an error is thrown when the element is not valid; 
 *                                        otherwise, a warning is logged.
 * @returns {boolean} - Returns true if the element is a valid HTMLElement, otherwise false.
 *
 * @throws {Error} - Throws an error if the element is not valid and shouldThrow is set to true.
 *
 * @example
 * const myElement = document.getElementById("my-element");
 * validateElement(myElement, "Invalid element!", true); // Throws error if myElement is not valid
 */
function validateElement(element, errorMsg, shouldThrow=false) {
    if (!(element instanceof HTMLElement) && !shouldThrow) {
        console.warn(errorMsg);
        return false;
    }

    if (!(element instanceof HTMLElement) && shouldThrow) {
        throw new Error(errorMsg);
    }

    return true;
}



export {
    validateElement,
}