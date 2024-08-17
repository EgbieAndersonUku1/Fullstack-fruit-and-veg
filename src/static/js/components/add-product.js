
import { minimumCharactersToUse } from "./characterCounter.js";
import {getItemFromLocalStorage, saveToLocalStorage, getAllCheckBoxElementsValue,
    redirectToNewPage, getCurrentPage, disableEmptySelectOptions as handleEmptySelectOptions
} from "../utils/utils.js";

import AlertUtils from "../utils/alerts.js";
import { getFormEntries, toggleInputVisibilityBasedOnSelection } from "../utils/formUtils.js";
import { populateSelectField } from "../builders/formBuilder.js";


const selectFormCategory = document.getElementById("select-category");
document.addEventListener("DOMContentLoaded", (e) => handleEmptySelectOptions(selectFormCategory))



// populate the select function
// populateSelectField("#countries", window.countriesFileUrl)


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
    handleFormSubmission(basicForm);
    
}



// handles detailed-description-specs.html
function handleDetailedInformationForm(e) {

    e.preventDefault();

    const colorsCheckboxes = document.querySelectorAll(".colors .color input[type='checkbox']:checked");
    const sizeCheckBoxes = document.querySelectorAll(".sizes .size input[type='checkbox']:checked");

    let formComplete = true;
  
    if (colorsCheckboxes.length === 0) {
        selectColorErrorMsg.style.display = "block";
        formComplete = false;

        AlertUtils.showAlert({
            "title": "Missing value",
            "icon": "warning",
            "text": "Select at least one color",
            "confirmButtonText": "Ok"
        })
      
    };

    if (sizeCheckBoxes.length === 0) {
        selectSizesErrorMsg.style.display = "block";
        formComplete = false;

        AlertUtils.showAlert({
            "title": "Missing value",
            "icon": "warning",
            "text": "Select at least one size",
            "confirmButtonText": "Ok"
        })
    };


    if (detailedForm.reportValidity() && formComplete) {

        const colors = getAllCheckBoxElementsValue(colorsCheckboxes, 'data-color');
        const sizes = getAllCheckBoxElementsValue(sizeCheckBoxes, 'data-size');
        const formEntries = getFormEntries(detailedForm);

        formEntries.colorsOptions = colors;
        formEntries.sizesOptions = sizes;

        delete formEntries["color"];
        delete formEntries["size"]


        handleFormComplete(detailedForm, formEntries);

    }
}


// handles pricing-inventory.html
function handlePriceInventoryForm(e) {
    e.preventDefault();
    handleFormSubmission(pricingInventoryForm);

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
        handleFormComplete(imageAndMediaForm, formObject);
    }
  

};



// handles shipping-and-delivery.html
function handleShippingAndDeliveryForm(e) {
    e.preventDefault();

    let formComplete = true;

    const deliveryCheckboxes = document.querySelectorAll(".shipping-options label input[name='shipping']:checked");

    if (deliveryCheckboxes.length === 0) {
        selectDeliveryErrorMsg.style.display = "block";
        formComplete = false;

        AlertUtils.showAlert({
            "title": "Missing value",
            "icon": "warning",
            "text": "Select at least one delivery option",
            "confirmButtonText": "Ok"
        })
      
    };

    if (shippingAndDeliveryForm.reportValidity() && formComplete) {
        const formEntries = getFormEntries(shippingAndDeliveryForm);
        formEntries.deliveryOptions = getAllCheckBoxElementsValue(deliveryCheckboxes, 'data-delivery-time');
        handleFormComplete(shippingAndDeliveryForm, formEntries);
    }

}


// handles seo-and-meta-information.html
function handleSeoAndMetaForm(e) {
    e.preventDefault();
    handleFormSubmission(seoAndMetaForm);
};


// handles additional-information.html
function handleAdditionalFormInfo(e) {
    e.preventDefault();
    handleFormSubmission(additionInformationForm);
}




function handleFormSubmission(form) {
    if (form.reportValidity()) {
        handleFormComplete(form, getFormEntries(form));
    }
}


function handleFormComplete(form, formEntries) {
    saveToLocalStorage(form.id, formEntries, true);
    form.submit()

}










