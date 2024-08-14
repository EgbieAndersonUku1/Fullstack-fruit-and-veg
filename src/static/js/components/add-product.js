import addNewProductPages from "../pages/pages.js";
import { minimumCharactersToUse } from "./characterCounter.js";
import {getItemFromLocalStorage, saveToLocalStorage, getAllCheckBoxElementsValue,
    redirectToNewPage, getCurrentPage
} from "../utils/utils.js";
import { getFormEntries, toggleInputVisibilityBasedOnSelection } from "../utils/formUtils.js";
import { populateSelectField } from "../builders/formBuilder.js";


window.prevPage = prevPage;



// populate the select function
populateSelectField("#countries", "../../../../countries.txt")


// checkboxes error msg selector
const selectColorErrorMsg = document.getElementById("color-error-msg");
const selectSizesErrorMsg = document.getElementById("size-error-msg");
const selectDeliveryErrorMsg = document.getElementById("delivery-error-msg");


// forms
const basicForm = document.getElementById("basic-product-information-form");
const detailedForm = document.getElementById("detailed-description-form");
const pricingInventoryForm = document.getElementById("pricing-inventory-form");
const imageAndMediaForm = document.getElementById("image-media-form");
const shippingAndDeliveryForm = document.getElementById("shipping-and-delivery-form");
const seoAndMetaForm = document.getElementById("seo-and-meta-form");
const additionInformationForm = document.getElementById("additional-information-form");


// AddEventListners for the forms
basicForm?.addEventListener("submit", handleBasicInformationForm);
detailedForm?.addEventListener("submit", handleDetailedInformationForm);
pricingInventoryForm?.addEventListener("submit", handlePriceInventoryForm);
imageAndMediaForm?.addEventListener("submit", handleImageAndMediaForm);
shippingAndDeliveryForm?.addEventListener("submit", handleShippingAndDeliveryForm);
seoAndMetaForm?.addEventListener("submit", handleSeoAndMetaForm);
additionInformationForm?.addEventListener("submit", handleAdditionalFormInfo);






// field selectors for textArea fields
const detailDescriptionTextAreaElement   = document.getElementById("detailed-description");
const shortDescriptionTextAreaElement    = document.getElementById("short-description");
const metaDescriptionTextAreaElement     = document.getElementById("meta-description");
const warrantyDescriptionTextAreaElement = document.getElementById("warranty-description");


// basic category  form fields
const selectProductCategoryElement = document.getElementById("select-category");
const addCategoryLabelElement = document.getElementById("add-category-label");
const addCategoryInputFieldElement = document.getElementById("add-category");

// pricing form fields
const selectDiscountCategoryElement = document.getElementById("select-discount");
const addDiscountLabelElement       = document.getElementById("add-discount-label");
const addDiscountInputFieldElement  = document.getElementById("add-discount");



// Text area field inside inside the detail description specs page
minimumCharactersToUse(detailDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 1000,
    disablePaste: true,
});



// Text area field for the basic product information page
minimumCharactersToUse(shortDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 255,
    disablePaste: true,

})



// Text area field for the meta description page
minimumCharactersToUse(metaDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 10,
    maxCharsLimit: 500,
    disablePaste: true,
});


// Text area field for the meta description page
minimumCharactersToUse(warrantyDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 2000,
    disablePaste: true,
});



// handle select product category located in the 'basic-production-information.html' page
selectProductCategoryElement?.addEventListener("change", () => toggleInputVisibilityBasedOnSelection(selectProductCategoryElement,
    addCategoryLabelElement,
    addCategoryInputFieldElement,
    "new"));



// handle select discount located in the 'pricing-inventor.html' page
selectDiscountCategoryElement?.addEventListener("change", () => toggleInputVisibilityBasedOnSelection(selectDiscountCategoryElement,
    addDiscountLabelElement,
    addDiscountInputFieldElement,
    "yes"
));





/**
 * Navigates to the previous page in the add new product workflow.
 * 
 * This function determines the page to navigate to based on the given page number, and redirects the user to that page.
 * If the page number is invalid, it throws an error.
 *
 * @param {Event} event - The event object that triggered the function.
 * @param {number|string} pageNumber - The page number to navigate to. This value is parsed as an integer.
 * @throws {Error} If the page number is invalid and the corresponding page is not found.
 * @returns {void}
 */
function prevPage(event, pageNumber) {
    event.preventDefault();

    const page = addNewProductPages[parseInt(pageNumber)];

    if (!page) {
        throw new Error("Something went wrong and the page number couldn't be found!!!");
    }

    redirectToNewPage(page);
}





/**
 * Updates form input fields with saved values when a form page loads.
 * 
 * This function determines the current page and retrieves the corresponding form element.
 * It then loads the saved values for that form from local storage and updates the form's input fields.
 * If the user had selected "new" or "yes" as the category in the dropdown menu, it resets the dropdown to the default state.
 * 
 * @returns {void}
 */
function updateFormValue() {
    const currentPage = getCurrentPage();

    const formElements = {
        "basic-product-information.html": basicForm,
        "detailed-description-specs.html": detailedForm,
        "pricing-inventory.html": pricingInventoryForm,
        "images-and-media.html": imageAndMediaForm,
        "shipping-and-delivery.html": shippingAndDeliveryForm,
        "SEO-and-meta-information.html": seoAndMetaForm,
        "additonal-information.html": additionInformationForm,
    };

    if (!currentPage || formElements[currentPage] === undefined) {
        console.warn(`No form element found for current page: ${currentPage}`);
        return;
    }

    const formDetails = formElements[currentPage];
    const productValues = getItemFromLocalStorage(formDetails.id, true);
    const productSelectCategory = basicForm?.querySelector("#select-category");
    const discountSelectCategory = pricingInventoryForm?.querySelector("#select-discount");

    // Iterate over the form elements and update their values using their saved data
    for (let element of formDetails.elements) {

        if (element.name) {
            element.value = productValues[element.name] || '';   // Fallback to empty string if no value
        };

    }

    // If the user had selected "new" or "yes" as the category for the dropdown menu, reset the dropdown to the default state
    // This indicates that the user did not choose a predefined category but entered a custom one instead
    if ( productSelectCategory && productSelectCategory.value === "new") {
         productSelectCategory.value = "";
    };

    if (discountSelectCategory && discountSelectCategory.value === "yes") {
       discountSelectCategory.value = "";
   }
}




// Handles the form submission for basic-product-information.html
function handleBasicInformationForm(e) {
    e.preventDefault();
    const pageNumber = 2;

  
    handleFormSubmission(basicForm, pageNumber);
    
}



// handles detailed-description-specs.html
function handleDetailedInformationForm(e) {

    e.preventDefault();

    const colorsCheckboxes = document.querySelectorAll(".colors .color input[type='checkbox']:checked");
    const sizeCheckBoxes = document.querySelectorAll(".sizes .size input[type='checkbox']:checked");

    let formComplete = true;
    const pageNumber = 3;

    if (colorsCheckboxes.length === 0) {
        selectColorErrorMsg.style.display = "block";
        formComplete = false;

        // replace this later with a more beautiful custom message
        alert("Select at least one color");
    };

    if (sizeCheckBoxes.length === 0) {
        selectSizesErrorMsg.style.display = "block";
        formComplete = false;

        // replace this later with a more beautiful custom message
        alert("Select at least one size");
    };


    if (detailedForm.reportValidity() && formComplete) {

        const colors = getAllCheckBoxElementsValue(colorsCheckboxes, 'data-color');
        const sizes = getAllCheckBoxElementsValue(sizeCheckBoxes, 'data-size');
        const formEntries = getFormEntries(detailedForm);

        formEntries.colorsOptions = colors;
        formEntries.sizesOptions = sizes;

        delete formEntries["color"];
        delete formEntries["size"]


        handleFormComplete(detailedForm, formEntries, pageNumber);

    }
}


// handles pricing-inventory.html
function handlePriceInventoryForm(e) {
    e.preventDefault();
    const pageNumber = 4;
    
    handleFormSubmission(pricingInventoryForm, pageNumber);

};



// handles images-and-media.html
function handleImageAndMediaForm(e) {

    e.preventDefault();
    const pageNumber = 5;
    const formObject = {};
   
    const formEntries = getFormEntries(imageAndMediaForm);

    if (!formEntries) {
        throw new Error("Something went wrong - the form values shouldn't be empty");
    };

    formObject.primaryImageName  = formEntries["primary-image"]["name"];
    formObject.sideImageName     = formEntries["side-image1"]["name"];
    formObject.sideImageName2    = formEntries["side-image2"]["name"];
    formObject.optionalVideo     = formEntries["primary-video"]["name"];

    if (imageAndMediaForm.reportValidity()) {
        handleFormComplete(imageAndMediaForm, formObject, pageNumber);
    }
  

};



// handles shipping-and-delivery.html
function handleShippingAndDeliveryForm(e) {
    e.preventDefault();

    const pageNumber = 6;
    let formComplete = true;

    const deliveryCheckboxes = document.querySelectorAll(".shipping-options label input[name='shipping']:checked");

    if (deliveryCheckboxes.length === 0) {
        selectDeliveryErrorMsg.style.display = "block";
        formComplete = false;

        // replace this later with a more beautiful custom message
        alert("Select at least one delivery option");
    };

    if (shippingAndDeliveryForm.reportValidity() && formComplete) {
        const formEntries = getFormEntries(shippingAndDeliveryForm);
        formEntries.deliveryOptions = getAllCheckBoxElementsValue(deliveryCheckboxes, 'data-delivery-time');
        handleFormComplete(shippingAndDeliveryForm, formEntries, pageNumber);
    }

}


// handles seo-and-meta-information.html
function handleSeoAndMetaForm(e) {
    e.preventDefault();
    const pageNumber = 7;
    handleFormSubmission(seoAndMetaForm, pageNumber);
};


// handles additional-information.html
function handleAdditionalFormInfo(e) {
    e.preventDefault();
    const pageNumber = 8;
    handleFormSubmission(additionInformationForm, pageNumber);
}




function handleFormSubmission(form, pageNumber) {
    if (form.reportValidity()) {
        handleFormComplete(form, getFormEntries(form), pageNumber);
    }
}


function handleFormComplete(form, formEntries, pageNumber) {
    saveToLocalStorage(form.id, formEntries, true);
    redirectToNewPage(addNewProductPages[pageNumber]);
}






window.onload = updateFormValue;



