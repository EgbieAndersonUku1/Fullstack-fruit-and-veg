/**
 * Initializes character count tracking and validation for a specified textarea element.
 * Optionally disables pasting into the textarea based on the provided flag.
 * 
 * **HTML Structure Requirements:**
 * 1. The `<textarea>` element should be passed directly to the function.
 * 2. The first `<p>` tag, which displays the minimum character count, must have a class name specified in the 
 *    `params.minCharClass`.
 * 3. The second `<p>` tag, which displays the maximum character count and remaining characters, must have a class 
 *    name specified in the `params.maxCharClass`.
 * 4. Both `<p>` tags must include a message ending with a colon, as the function appends the character count 
 *    to the message. For example:
 *    - If the message is "Number of characters remaining: " and the remaining characters are 50, 
 *      the display will be "Number of characters remaining: 50".
 * 
 * **Parameters for the Function:**
 * The following parameters must be included in the parameter object:
 * - minCharClass: {string} - CSS selector for the minimum characters count element.
 * - minCharMessage: {string} - Message to display for minimum characters.
 * - maxCharClass: {string} - CSS selector for the maximum characters count element.
 * - maxCharMessage: {string} - Message to display for maximum characters.
 * - minCharsLimit: {number} - Minimum number of characters allowed.
 * - maxCharsLimit: {number} - Maximum number of characters allowed.
 * - disablePaste: {boolean} - Flag to enable or disable pasting in the textarea.
 * 
 * **Example Parameter Object:**
 * const params = {
 *   minCharClass: '.minimum-characters',
 *   minCharMessage: 'Minimum characters to use: ',
 *   maxCharClass: '.maximum-characters',
 *   maxCharMessage: 'Number of characters remaining: ',
 *   minCharsLimit: 50,
 *   maxCharsLimit: 1000,
 *   disablePaste: true // Set to false to allow pasting
 * };
 * 
 * **Example Usage:**
 * const textAreaElement = document.querySelector(".textArea"); // Obtain the textarea element directly
 * minimumCharactersToUse(textAreaElement, params);
 * 
 * **Note:**
 * The CSS for the color changes is mandatory. To enable the color changes, the following CSS classes must be defined:
 * 
 * .light-red {
 *   color: red;
 * }
 * 
 * .black-color {
 *   color: black;
 * }
 * 
 * .dark-green {
 *   color: var(--dark-green); // This is a specific color variable stored in root, but you can use "green" instead
 * }
 * 
 * Styling the `<textarea>` box and its related elements is optional but must follow the above CSS for character count displays.
 * 
 * @param {HTMLTextAreaElement} textAreaElement - The textarea element to track character counts for.
 * @param {Object} params - Object containing various parameters for character limits and messages.
 * @param {string} params.minCharClass - CSS selector for the minimum characters element.
 * @param {string} params.minCharMessage - Message to display for minimum characters.
 * @param {string} params.maxCharClass - CSS selector for the maximum characters element.
 * @param {string} params.maxCharMessage - Message to display for maximum characters.
 * @param {number} params.minCharsLimit - Minimum characters limit.
 * @param {number} params.maxCharsLimit - Maximum characters limit.
 * @param {boolean} params.disablePaste - Flag to enable or disable pasting in the textarea.
 * @throws {Error} If the parameter object is not valid or does not contain the required keys, or if the maxCharsLimit is less than minCharsLimit.
 */
function minimumCharactersToUse(textAreaElement, params) {
    if (!textAreaElement || !(textAreaElement instanceof HTMLTextAreaElement)) {
        console.error("Error: Invalid textarea element provided.");
        return;
    }

    if (typeof params !== "object") {
        throw new Error("The parameter must be an object.");
    }

    const requiredKeys = [
        "minCharClass",
        "minCharMessage",
        "maxCharClass",
        "maxCharMessage",
        "minCharsLimit",
        "maxCharsLimit",
        "disablePaste"
    ];

    for (const key of requiredKeys) {
        if (!params.hasOwnProperty(key)) {
            throw new Error(`Missing required parameter: ${key}`);
        }
    }

    if (params.maxCharsLimit < params.minCharsLimit) {
        throw new Error("The maximum character value cannot be less than the minimum character value");
    }

    // Set the minlength and maxlength attributes dynamically
    textAreaElement.setAttribute('minlength', params.minCharsLimit.toString());
    textAreaElement.setAttribute('maxlength', params.maxCharsLimit.toString());

    if (params.disablePaste) {
        disableTextAreaBoxPaste(textAreaElement);
    }

    textAreaElement.addEventListener("input", (e) => handleCharacterCountEvent(e, params));
}


/**
 * Handles the input event to check both minimum and maximum character limits.
 * @param {Event} e - The event object.
 * @param {object} params - Object containing various parameters for character limits and messages.
 */
function handleCharacterCountEvent(e, params) {
    handleCharCount(e, params.minCharsLimit, params.minCharClass, params.minCharMessage);
    handleCharCount(e, params.maxCharsLimit, params.maxCharClass, params.maxCharMessage);
}

/**
 * Handles the character count for the specified limit.
 * @param {Event} e - The event object.
 * @param {number} limit - The character limit.
 * @param {string} classSelector - CSS selector for the output element.
 * @param {string} message - The message to display..
 */
function handleCharCount(e, limit, classSelector, message) {
    const charsUsed = e.target.value.length;
    const charsRemaining = limit - charsUsed;
    const outputElement = document.querySelector(classSelector);
    updateTextString(outputElement, charsRemaining, limit, message)
}



/**
 * Updates the text content and styles of the string element.
 * @param {HTMLElement} stringElement - The element displaying the character count.
 * @param {number} charsRemaining - The number of remaining characters.
 * @param {number} limit - The character limit.
 * @param {string} msg - The message to display.
 */
function updateTextString(stringElement, charsRemaining, limit, msg) {
    const EMPTY_VALUE = 0;
    if (!stringElement || !(stringElement instanceof HTMLElement)) {
        throw new Error("The stringElement is either empty or is not a HTML element")
    }
  
    stringElement.classList.remove("light-red", "black-color", "dark-green");
    
    if (charsRemaining >= 0) {
        stringElement.textContent = `${msg} ${charsRemaining}`;
    }

    switch (true) {
        case charsRemaining === EMPTY_VALUE:
            stringElement.classList.add("black-color");
            break;
        case charsRemaining < EMPTY_VALUE:
            stringElement.classList.add("dark-green");
            break;
        case charsRemaining < limit:
            stringElement.classList.add("light-red");
            break;
    }
}


/**
 * Disables the paste functionality for a specified textarea element to prevent issues with character counting functionality.
 * 
 * When pasting into the textarea, the following actions are performed:
 * - The default paste action is prevented.
 * - An alert is displayed to inform the user that pasting is not allowed.
 * - The content of the textarea is cleared.
 * - The character counter associated with the textarea is reset.
 * 
 * This function is useful to maintain accurate character counts in scenarios where pasting might otherwise disrupt the count.
 * 
 * @param {HTMLTextAreaElement} textAreaElement - The textarea element where paste functionality should be disabled.
 * 
 * @example
 * // Assuming `myTextArea` is a valid HTMLTextAreaElement
 * disableTextAreaBoxPaste(myTextArea);
 */
/**
 * Disables the paste functionality for a specified textarea element to prevent issues with character counting.
 * 
 * When pasting into the textarea, the following actions are performed:
 * - The default paste action is prevented.
 * - An alert is displayed to inform the user that pasting is not allowed.
 * - The content of the textarea is cleared.
 * - The character counter associated with the textarea is reset.
 * 
 * This function is useful to maintain accurate character counts in scenarios where pasting might otherwise disrupt the count.
 * 
 * @param {HTMLTextAreaElement} textAreaElement - The textarea element where paste functionality should be disabled.
 */
function disableTextAreaBoxPaste(textAreaElement) {
    if (textAreaElement instanceof HTMLTextAreaElement) {
        textAreaElement.addEventListener("paste", (e) => {
            e.preventDefault();
            alert("You cannot paste in text!!");
            textAreaElement.value = "";
            resetCharacterTextBoxString(); 
        });
    } else {
        console.warn("Provided element is not a valid HTMLTextAreaElement.");
    }
}


export {
    minimumCharactersToUse,
    disableTextAreaBoxPaste
}