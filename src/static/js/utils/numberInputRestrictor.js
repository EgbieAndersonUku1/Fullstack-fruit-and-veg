/**
 * Prevents typing numeric characters into an input field by intercepting key events.
 * Allows specific keys and key combinations that are not numeric.
 * 
 * @param {KeyboardEvent} event - The keyboard event object.
 */
function preventNumberInputTyping(event) {
    console.log("preventNumberInputTyping called with key:", event.key, "code:", event.code);

    const allowedKeys = ["Backspace", "Delete", "Tab", "Escape", "Enter", 
                        "Home", "End", "ArrowLeft", "ArrowUp", "ArrowRight", "ArrowDown"
                        ]; 

    // Allow Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X, and function keys (F1 - F12)
    if (
        allowedKeys.includes(event.key) ||
        (event.code.startsWith("F") && event.code.length === 2 && parseInt(event.code.charAt(1)) >= 1 && parseInt(event.code.charAt(1)) <= 12) || // F1 - F12 keys
        (event.key === "a" && event.ctrlKey === true) || // Ctrl+A
        (event.key === "c" && event.ctrlKey === true) || // Ctrl+C
        (event.key === "v" && event.ctrlKey === true) || // Ctrl+V
        (event.key === "x" && event.ctrlKey === true) || // Ctrl+X
        (event.key === "Home" || event.key === "End")   
    ) {
        return; 
    }

    event.preventDefault(); 
}

export default preventNumberInputTyping