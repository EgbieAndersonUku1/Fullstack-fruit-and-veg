import { minimumCharactersToUse } from "./characterCounter.js";
import {disableEmptySelectOptions as handleEmptySelectOptions} from "../utils/utils.js";
import { saveToLocalStorage, getItemFromLocalStorage, removeItemFromLocalStorage } from "../utils/utils.js";
import { redirectToNewPage } from "../utils/utils.js";
import AlertUtils from "../utils/alerts.js";
import { toggleInputVisibilityBasedOnSelection } from "../utils/formUtils.js";


// selectors
const selectFormCategory      = document.getElementById("select-category");
const selectPriceFormCategory = document.getElementById("select-discount");
const phoneNumber             = document.getElementById("manufacturer-phone-number");
const reviewButton            = document.getElementById("review-submit-btn");



const PRODUCT_SELECT_OPTION_VALUE  = "new";
const DISCOUNT_SELECT_OPTION_VALUE = "yes"
const PAGE_COMPLETE                = "pageCompleted";


let pageCompleted = getItemFromLocalStorage(PAGE_COMPLETE, true) || {
    step1: false,
    step2: false,
    step3: false,
    step4: false,
    step5: false,
    step6: false,
    step7: false,
    step8: false,

};


// handle the empty field in the select option for basic form
document.addEventListener("DOMContentLoaded", (e) => handleEmptySelectOptions(selectFormCategory))

// handle the empty field for the pricing and inventory form
document.addEventListener("DOMContentLoaded", (e) => handleEmptySelectOptions(selectPriceFormCategory))


// handle the phone number entry in real time
phoneNumber?.addEventListener("input", handlePhoneNumOrganisation);


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
const nutritionForm = document.getElementById("nutrition-form");


// AddEventListners for the forms
basicForm?.addEventListener("submit", handleBasicInformationForm);
detailedForm?.addEventListener("submit", handleDetailedInformationForm);
pricingInventoryForm?.addEventListener("submit", handlePriceInventoryForm);
imageAndMediaForm?.addEventListener("submit", handleImageAndMediaForm);
shippingAndDeliveryForm?.addEventListener("submit", handleShippingAndDeliveryForm);
seoAndMetaForm?.addEventListener("submit", handleSeoAndMetaForm);
nutritionForm?.addEventListener("submit", handleNutritionForm);
additionInformationForm?.addEventListener("submit", handleAdditionalFormInfo);
reviewButton?.addEventListener("click", handleReviewSubmit);


// field selectors for textArea fields
const detailDescriptionTextAreaElement   = document.getElementById("detailed-description");
const shortDescriptionTextAreaElement    = document.getElementById("short-description");
const metaDescriptionTextAreaElement     = document.getElementById("meta-description-textarea");
const warrantyDescriptionTextAreaElement = document.getElementById("warranty-description");


// basic category  form fields
const selectProductCategoryElement = document.getElementById("select-category");
const addCategoryLabelElement      = document.getElementById("add-category-label");
const addCategoryInputFieldElement = document.getElementById("add-category");

// pricing form fields
const selectDiscountCategoryElement = document.getElementById("select-discount");
const addDiscountLabelElement       = document.getElementById("add-discount-label");
const addDiscountInputFieldElement  = document.getElementById("add-discount");



// Text area field for the `basic-product-information.html` page
minimumCharactersToUse(shortDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 255,
    disablePaste: true,

})


// Text area field inside the `detail-description-specs.html` page
minimumCharactersToUse(detailDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 1000,
    disablePaste: true,
});


// Text area field  inside the `SEO-and-meta-information.html` 
minimumCharactersToUse(metaDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 10,
    maxCharsLimit: 500,
    disablePaste: true,
});


// Text area field for the warranty description page in additional_information.html
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
    PRODUCT_SELECT_OPTION_VALUE
));



// handle select discount located in the 'pricing-inventor.html' page
selectDiscountCategoryElement?.addEventListener("change", () => toggleInputVisibilityBasedOnSelection(selectDiscountCategoryElement,
    addDiscountLabelElement,
    addDiscountInputFieldElement,
    DISCOUNT_SELECT_OPTION_VALUE,
));



// Handles the form submission for basic-product-information.html
function handleBasicInformationForm(e) {
    e.preventDefault();
    handleFormSubmission(basicForm, "step1");
    
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
        handleFormSubmission(detailedForm, "step2")
    }
}


// handles pricing-inventory.html
function handlePriceInventoryForm(e) {
    e.preventDefault();
    handleFormSubmission(pricingInventoryForm, "step3");

};



// handles images-and-media.html
function handleImageAndMediaForm(e) {

    e.preventDefault();
    handleFormSubmission(imageAndMediaForm, "step4")
  
};



// handles shipping-and-delivery.html
function handleShippingAndDeliveryForm(e) {
    e.preventDefault();

    let formComplete         = true;
    const deliveryCheckboxes = document.querySelectorAll(".shipping-options .options label input[name='delivery_options']:checked");

    if (deliveryCheckboxes.length === 0) {
        selectDeliveryErrorMsg.style.display = "block";
        formComplete = false;

        AlertUtils.showAlert({
            "title": "Missing value",
            "icon": "warning",
            "text": "Select at least one delivery option",
            "confirmButtonText": "Ok"
        })
      
    } 

    if (shippingAndDeliveryForm.reportValidity() && formComplete) {
        handleFormSubmission(shippingAndDeliveryForm, "step5");
    }

}



// handles seo-and-meta-information.html
function handleSeoAndMetaForm(e) {
    e.preventDefault();
    handleFormSubmission(seoAndMetaForm, "step6");
};


// handles additional-information.html
function handleAdditionalFormInfo(e) {
    e.preventDefault();
    handleFormSubmission(additionInformationForm, "step8");
}


function handleFormSubmission(form, step) {
    if (form.reportValidity()) {
        markPageAsComplete(step);
        form.submit()
    }
}


function handleNutritionForm(e) {
    e.preventDefault();
    handleFormSubmission(nutritionForm, "step7")
}


function handleReviewSubmit(e) {
    e.preventDefault();
   
    console.log(reviewButton.href);
    const canSubmit = checkIfCanSubmit();

    if (canSubmit) {
        AlertUtils.showSaveAlert({showDenyButton: true}).then((value) => {
            if (value) {
                const submitUrl = reviewButton.href;
                if (!submitUrl) {
                    throw new Error(`Something went wrong and the submission url was found got ${submitUrl}`);
                };
               
                removeItemFromLocalStorage(PAGE_COMPLETE);
                redirectToNewPage(submitUrl);
              
            }
        });
    }
}


function handlePhoneNumOrganisation(e) {
   
    let phoneNumber          = e.target.value;
    let formattedPhoneNumber = '';

    // Remove any non-numeric characters
    const digitsOnly = phoneNumber.replace(/\D/g, '');

    if (phoneNumber !== digitsOnly) {
        e.target.value = digitsOnly; 
    }

    // Format the phone number by adding dashes after every fourth digit
    for (let i = 0; i < digitsOnly.length; i++) {
       
        if (i > 0 && i % 4 === 0) {

            formattedPhoneNumber += '-';
        }
        formattedPhoneNumber += digitsOnly[i];
    
    }

    e.target.value = formattedPhoneNumber;
}



function markPageAsComplete(step) {

    pageCompleted[step] = true;
    saveToLocalStorage(PAGE_COMPLETE, pageCompleted, true);
  
}


function checkIfCanSubmit() {
    for (let key in pageCompleted) {

        if (!pageCompleted[key]) {
            const stepNo = key.slice(-1);

            AlertUtils.showAlert({
                "title": "Incomplete step",
                "icon": "warning",
                "text": `Step ${stepNo} hasn't been completed!`,
                "confirmButtonText": "Ok",
            })
            return false;
        }
    };
    return true;
}

console.log(pageCompleted);