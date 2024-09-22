/**
 * In the `user_profile.html` form, there are two forms: the billing address form and the shipping address form.
 * All fields within these forms are marked as required. However, the billing address form is initially hidden and 
 * thus cannot be marked as required while it is hidden. Doing so would lead to two issues:
 * 
 * 1. JavaScript throws a "non-autofocus" error because a field cannot be both required and hidden.
 * 2. The form cannot be submitted because, even though the billing address fields are hidden, they are still marked 
 *    as required.
 * 
 * To address these issues:
 * - When the billing address form is hidden, its fields are marked as non-required.
 * - When the form is made visible, the required attribute is added back to the fields.
 * 
 * The JavaScript functions below dynamically handle these requirements:
 * - They remove the 'required' attribute from the billing address fields when the form is hidden.
 * - They add the 'required' attribute back when the form is shown.
 */


import { validateElement } from "../errors/customErrors.js";


const billingAddressRadioContainer = document.getElementById("billing-address-radio-buttons");
const shippingAddressContainer       = document.getElementById("shipping-address-container");
const shippingDivElements          = document.querySelectorAll(".shipping-field");


billingAddressRadioContainer?.addEventListener("click", handleRadioButtonClick);


document.addEventListener("DOMContentLoaded", handleSetup);


function handleSetup() {
    toggleRequiredForAllFields(shippingDivElements, false)
}



/**
 * Toggles the `required` attribute for a list of field elements (e.g., input, select, textarea)
 * based on the provided `toggle` parameter.
 * 
 * @param {NodeList} fieldNodeElements - A list of container elements (typically divs) that contain the input fields to toggle.
 * @param {boolean} [toggle=true] - A boolean that controls whether the fields should be required. 
 * If `true`, the fields will be required; if `false`, they will be non-required.
 * 
 * @throws {Error} If the fieldNodeElements list is empty or not provided.
 */
function toggleRequiredForAllFields(fieldNodeElements, toggle=true) {
    if (!fieldNodeElements) {
        throw new Error("The field node elements list cannot be empty");
    }

    fieldNodeElements.forEach((fieldNodeElement) => {
        const inputFieldElement = extractInputFieldFromDiv(fieldNodeElement);
        toggleRequiredField(inputFieldElement, toggle);
    })
}




/**
 * Toggles the `required` attribute of a single field element (e.g., input, select, textarea).
 * 
 * @param {HTMLElement} fieldElement - The field element to modify. The element's `required` attribute 
 * is set based on the value of the `toggle` parameter.
 * @param {boolean} [toggle=false] - A boolean that controls whether the field is required or not.
 * If `true`, the field becomes required; if `false`, it is non-required.
 */
function toggleRequiredField(fieldElement, toggle=false) {
    validateElement(fieldElement, "The fieldElement is not a valid HTMLElement or input field element", false);
    try {
        fieldElement.required = toggle;
    } catch (error) {
        console.warn("Couldn't toggle the 'required' attribute for the field.");
    }
};



/**
 * Extracts an input field element from a given `div` element.
 * If the input field is not found, a warning message is logged.
 * 
 * @param {HTMLElement} divElement - The `div` element containing the input field to extract.
 * @param {string} [fieldSelector="input"] - The type of field to extract (e.g., "input", "select", "textarea").
 * @returns {HTMLElement|undefined} The extracted input field element, or `undefined` if not found.
 */
function extractInputFieldFromDiv(divElement, fieldSelector="input") {
    validateElement(divElement, "The divElement is not a HTMLElement", true);

    try {
        return divElement.querySelector(fieldSelector);
    } catch (error) {
        console.warn("No input field found within the div element.");
        return undefined;
    }
}



/**
 * Handles the click event on the radio button.
 * Depending on whether the selected value is "yes" or "no", 
 * it shows or hides the billing address form and adjusts the required fields accordingly.
 * 
 * If "no" is selected, the billing address is displayed and the fields become required.
 * If "yes" is selected, the billing address is hidden and the fields are no longer required.
 * 
 * @param {Event} e - The event object from the radio button click.
 */
function handleRadioButtonClick(e) {

    validateElement(shippingAddressContainer, "The shipping address container element couldn't be found", true);
    const value  = e.target.value?.toLowerCase();

    console.log(value)
    if (value === "no") {
        shippingAddressContainer.classList.remove("d-none");
       
        toggleRequiredForAllFields(shippingDivElements, true);
    } else {
        shippingAddressContainer.classList.add("d-none");
        toggleRequiredForAllFields(shippingDivElements, false);
    }
}


