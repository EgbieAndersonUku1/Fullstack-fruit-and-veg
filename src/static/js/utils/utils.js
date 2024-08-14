
function getRandomCharacter(character) {
    return character.charAt(Math.floor((Math.random() * character.length)));
}

// To be used in conjuction to with a JWT in order to generate a secure JWT_TOKEN
function generateSessionKey() {

    const capital     = "ABCDEFGHIJKLMNOPQRSTUVWXYXZ";
    const lower       = "abcdefghijklmnopqrstuvwxyz";
    const punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
    const string      = `${capital}${lower}${punctuation}`;

    const sessionKeyArray = [];
  

    for (let i=0; i < string.length; i++) {
        const char = getRandomCharacter(string);
        sessionKeyArray.push(char);
    }

    const sessionKeyString = sessionKeyArray.join("");
    return `SessionKey$-${sessionKeyString}`;
}


function saveToLocalStorage(name, valueToSave, stringfy = false) {
    if (!stringfy) {
        localStorage.setItem(name, valueToSave); 
    } else {
        localStorage.setItem(name, JSON.stringify(valueToSave)); 
    }
}


function getItemFromLocalStorage(name, parse = false) {
    const item = localStorage.getItem(name);
    return parse ? JSON.parse(item) : item; 
}


function removeItemFromLocalStorage(name) {
    localStorage.removeItem(name);
}

function redirectToNewPage(newPageUrl) {
    window.location.href = newPageUrl;
}


function getCurrentDay() {
    return new Date().getDate();
  }
  
function getFormattedCurrentDate() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1; // months are 0-based
    const day = currentDate.getDate();
    return `${year}-${month}-${day}`;
  }
  

/**
 * Retrieves the values of all checked checkbox elements in the provided collection.
 *
 * This reusable function takes a collection of checkbox elements (either an array or NodeList)
 * and returns an array of their values based on the specified attribute. It checks if the input is 
 * a valid collection of elements and includes only the values of input elements of type "checkbox" 
 * that are currently checked. The attribute must be provided, and it can be any valid attribute 
 * including custom data attributes (e.g., `data-size`). Ensure that the attribute name is consistent 
 * across all relevant elements.
 *
 * @param {Array|NodeList} checkboxElements - The collection of checkbox elements.
 * @param {string} attribute - The attribute to retrieve the value from. Must be provided.
 * @returns {Array} - An array containing the values of the checked checkbox elements based on the specified attribute.
 * @throws {Error} - If the input is not a valid collection of elements or if the attribute is not provided.
 *
 * @example
 * // Example 1: Retrieving values using a consistent data attribute
 * const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
 * const values = getAllCheckBoxElementsValue(checkboxes, 'data-size');
 * console.log(values); // Output: ["medium", "large"]
 * 
 * // Example HTML for Example 1:
 * // <input type="checkbox" name="item" data-size="small">
 * // <input type="checkbox" name="item" data-size="medium" checked>
 * // <input type="checkbox" name="item" data-size="large" checked>
 * 
 * @example
 * // Example 2: Handling an invalid call without the required attribute parameter
 * try {
 *     const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
 *     const values = getAllCheckBoxElementsValue(checkboxes); // Throws an error
 * } catch (error) {
 *     console.error(error.message); // Output: "The attribute must be provided"
 * }
 */
function getAllCheckBoxElementsValue(checkboxElements, attribute) {
    if (!checkboxElements || (!Array.isArray(checkboxElements) && !(checkboxElements instanceof NodeList))) {
        throw new Error("The input is not a valid collection of elements");
    }
    if (!attribute) {
        throw new Error("The attribute must be provided");
    }

    const checkedValues = [];

    checkboxElements.forEach((checkbox) => {
        if (checkbox.checked) {
            const value = checkbox.getAttribute(attribute);
            if (value) {
                checkedValues.push(value);
            }
        }
    });

    return checkedValues;
}



function getCurrentUrl() {
    return window.location.href;
}

function getCurrentPage() {
    return getCurrentUrl()?.split("/")?.pop();
}


function capitalize(str) {
    if (typeof str !== 'string' || str.length === 0) {
        return str;
    }
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}
  


export {
    generateSessionKey,
    saveToLocalStorage,
    getItemFromLocalStorage,
    removeItemFromLocalStorage,
    redirectToNewPage,
    getFormattedCurrentDate,
    getAllCheckBoxElementsValue,
    getCurrentUrl,
    getCurrentPage,
    capitalize,
    
};