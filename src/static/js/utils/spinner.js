import { validateElement } from "../errors/customErrors.js";

/**
 * Displays a spinner element for a specified duration and then hides it.
 *
 * @param {Object} options - The options for the spinner display.
 * @param {HTMLElement} options.spinnerElement - The HTML element representing the spinner.
 * @param {number} [options.duration=3000] - The duration (in milliseconds) for which the spinner will be shown. Defaults to 3000ms (3 seconds).
 * @throws {Error} Will throw an error if the spinnerElement is not a valid HTML element.
 */
function showSpinner({spinnerElement, duration = 3000}) {
 
    validateElement(spinnerElement, "This spinner is not a valid HTML element", true);

    spinnerElement.style.display = "block";

    setTimeout(() => {
        spinnerElement.style.display = "none";
    }, duration);
}


export default showSpinner;