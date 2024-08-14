import { getItemFromLocalStorage, 
         saveToLocalStorage, 
         removeItemFromLocalStorage, 
         getFormattedCurrentDate 
      } from "../utils/utils.js";

import addNewProductPages from "./pages.js";

import mergeObjects from "../utils/mergeObjects.js";
import AlertUtils from "../utils/alerts.js";


const basicProductInformation              = document.getElementById("basic-product-info");
const basicProductInformationPElements     = basicProductInformation?.querySelectorAll(".product-info .info p");
const detailedProductInformation           = document.getElementById("detail-product-info");
const detailedProductInformationPElements  = detailedProductInformation.querySelectorAll(".product-info .info p");
const pricingInventoryInformation          = document.getElementById("product-pricing-info");
const pricingInventoryInformationPElements = pricingInventoryInformation.querySelectorAll(".product-info .info p");
const imageAndMediaInformation             = document.getElementById("image-and-media");
const imageAndMediaPElements               = imageAndMediaInformation.querySelectorAll(".img-preview .info p");
const shippingInformation                  = document.getElementById("shipping-and-delivery");
const shippingInformationPElements         = shippingInformation.querySelectorAll(".product-info .info p");
const seoAndMetaInformationElements        = document.getElementById("seo-and-meta-information");
const seoAndMetaInformationPElements       = seoAndMetaInformationElements.querySelectorAll(".product-info .info p");
const additionalInformationElements        = document.getElementById("additional-information");
const additionalInformationPElements       = additionalInformationElements.querySelectorAll(".product-info .info p");

const reviewButtonElement  = document.getElementById("review-submit-btn");
let formArrayObjects     = [];


reviewButtonElement.addEventListener("click", handleReviewButtonClick);

console.log(reviewButtonElement);


function getBasicInformation() {

    const REQUIRED_ELEMENTS_COUNT = 6;
    validateProductInformation(basicProductInformation, basicProductInformationPElements, REQUIRED_ELEMENTS_COUNT);

    const formInfo    = getItemFromLocalStorage("basic-product-information-form", true);
    const ERR_MESSAGE = "Basic product section is incomplete";

    addToArrayIfValid(validateFormSection, formInfo, ERR_MESSAGE);
    populateProductInfo(basicProductInformationPElements, formInfo, updateProduct);
    return true;

};



/**
 * Updates detailed product information based on the data from local storage.
 * Throws an error if the required elements are not found.
 */
function getDetailedProductInformation() {
    const REQUIRED_ELEMENTS_COUNT = 7;

    validateProductInformation(detailedProductInformation, detailedProductInformationPElements, REQUIRED_ELEMENTS_COUNT)

    const formInfo = getItemFromLocalStorage("detailed-description-form", true);
    const ERR_MESSAGE = "Detailed product section is incomplete";
 
    addToArrayIfValid(validateFormSection, formInfo, ERR_MESSAGE);

    // Destructure the P elements
    const [colors, length, width, height, sizes, weight, description] = detailedProductInformationPElements;

    updateProduct(colors, formInfo.colorsOptions ? formInfo.colorsOptions.join(', ') : '');
    updateProduct(length, formInfo.length || '');
    updateProduct(width, formInfo.width || '');
    updateProduct(height, formInfo.height || '');
    updateProduct(sizes, formInfo.sizesOptions ? formInfo.sizesOptions.join(', ') : '');
    updateProduct(weight, formInfo.weight || '');
    updateProduct(description, formInfo.description || '');
    return true;

}


function getPricingInventoryInformation() {
    const REQUIRED_ELEMENTS_COUNT = 7;
    
    validateProductInformation(pricingInventoryInformation, pricingInventoryInformationPElements, REQUIRED_ELEMENTS_COUNT);
    const formInfo    = getItemFromLocalStorage("pricing-inventory-form", true);
    const ERR_MESSAGE = "Pricing & inventory section is incomplete";

    addToArrayIfValid(validateFormSection, formInfo, ERR_MESSAGE);
    populateProductInfo(pricingInventoryInformationPElements, formInfo, updateProduct);
    return true;

};



function getImageAndMediaInformation() {
    const REQUIRED_ELEMENTS_COUNT = 3;
    validateProductInformation(imageAndMediaInformation, imageAndMediaPElements, REQUIRED_ELEMENTS_COUNT);
    const formInfo  = getItemFromLocalStorage("image-media-form", true);
    const ERR_MESSAGE = "Image & media section is incomplete";

    addToArrayIfValid(validateFormSection, formInfo, ERR_MESSAGE);

    populateProductInfo(imageAndMediaPElements, formInfo, updateProduct);
    return true;
 
};




function getShippingInformation() {

    const REQUIRED_ELEMENTS_COUNT = 3;
    validateProductInformation(shippingInformation, shippingInformationPElements, REQUIRED_ELEMENTS_COUNT);

    // Turn the `shippingInformationPElements` nodeList into an array, so that the shipping 'p' elements and shipping 
    // delivery `select options` elements can be extracted and handled separately
    const pElementsList           = Array.from(shippingInformationPElements);
    const shippingPElements       = pElementsList.slice(0, -1);
    const shippingDeliveryElement = pElementsList.slice(-1)[0];
    const formInfo                = getItemFromLocalStorage("shipping-and-delivery-form", true);

    const ERR_MESSAGE = "Shipping section is incomplete";
    addToArrayIfValid(validateFormSection, formInfo, ERR_MESSAGE);
    populateProductInfo(shippingPElements, formInfo, updateProduct);
    updateProduct(shippingDeliveryElement, formInfo.deliveryOptions ? formInfo.deliveryOptions.join(', ') : '');
    return true;


    
};


function getSEOAndMetaInformation() {
    const REQUIRED_ELEMENTS_COUNT = 3;
    validateProductInformation(seoAndMetaInformationElements, seoAndMetaInformationPElements, REQUIRED_ELEMENTS_COUNT);

    const formInfo    = getItemFromLocalStorage("seo-and-meta-form", true);
    const ERR_MESSAGE = "SEO & meta section is incomplete";

    addToArrayIfValid(validateFormSection, formInfo, ERR_MESSAGE);
    populateProductInfo(seoAndMetaInformationPElements, formInfo, updateProduct);
    return true;

};




function getAdditionalInformation() {

    const REQUIRED_ELEMENTS_COUNT = 4;
    validateProductInformation(additionalInformationElements, additionalInformationPElements, REQUIRED_ELEMENTS_COUNT);

    const formInfo    = getItemFromLocalStorage("additional-information-form", true);
    const ERR_MESSAGE = "Additional information section is incomplete";

    addToArrayIfValid(validateFormSection, formInfo, ERR_MESSAGE);
    populateProductInfo(additionalInformationPElements, formInfo, updateProduct);
    return true;

   
};





function populateProductInfo(pElements, formInfo, updateCallback) {
    let index = 0;
    for (let [_, value] of Object.entries(formInfo)) {
        const pElement = pElements[index];
        if (value && (index < pElements.length) && value.toLowerCase() !== "new" ) {
            updateCallback(pElement, value);
        } else {
            updateCallback(pElement, "N/A");
        }

      index++;


      
    }
}

/**
 * Updates the text content of the given HTML element with the provided description.
 * Logs an error if the element is not found or if the description is invalid.
 * 
 * @param {HTMLElement} pElement - The element whose text content needs to be updated.
 * @param {string} description - The text to set as the element's content.
 */
function updateProduct(pElement, description) {
    if (!(pElement instanceof HTMLElement)) {
        console.error("Invalid pElement: Must be an instance of HTMLElement.");
        return;
    } 

    if (typeof description === 'string') {
        pElement.textContent = description;
    } else {
        console.error("Invalid description: Must be a string.");
    }
}


function validateProductInformation(productInformationElement, productionInformationPElements, requiredLength) {
    if (!productInformationElement || productionInformationPElements.length < requiredLength) {
        throw new Error(`Expected ${requiredLength} elements but found ${productionInformationPElements.length}.`);
    }
}




function addToArrayIfValid(validationFunction, formObject, message) {
    try {
        if (validationFunction(formObject, message)) {
            formArrayObjects.push(formObject);
        }
    } catch (error) {
        console.error(error.message);
       
    }
}


function validateFormSection(formInfo, message) {
    if (!formInfo) {

        AlertUtils.showAlert({ title: "Incomplete Product Information",
            text:message,
            icon: 'error',
            confirmButtonText: 'Incomplete!!'
        })
       return;
    }
    return true;
}



function handleReviewButtonClick(e) {
   
    const EXPECTED_REVIEWS = 7;
    const SAVE_AS          = "products-list";

    if (typeof formArrayObjects === 'undefined') {
        console.error("formArrayObjects is not defined.");
        return;
    }

    if (EXPECTED_REVIEWS !== formArrayObjects.length) {
        const ERR_MESSAGE = "One or more reviews are missing - go back and add them before submitting";

        AlertUtils.showAlert({
            "title": "Incomple form entries",
            text: ERR_MESSAGE,
            icon: "warning",
            confirmButtonText: "Incomplete form entry"
        })
        console.log("There are missing form entries");
        return;
    }

    const item     = mergeObjects(...formArrayObjects);
    const products = getProductsOrCreate();

    if (products) {
        item.id          = products.length + 1;
        item.isLive      = false;
        item.dateCreated = getFormattedCurrentDate();

        products.push(item);
        saveToLocalStorage(SAVE_AS, products, true);
        
        removeStoredProductForms();

        AlertUtils.showAlertWithRedirect({
                title: 'Product Added!',
                text: 'Your product has been successfully added to the store.',
                icon: 'success',
                confirmButtonText: 'Great!',
                redirectUrl: addNewProductPages[1]
        })
       
        
    }
  

};

/**
 * Clears stored product form data from local storage.
 *
 * This function removes various product form data from the local storage,
 * including basic product information, detailed description, pricing and inventory,
 * image and media, shipping and delivery, SEO and meta information, and additional information forms.
 *
 * If an error occurs during the removal process, it will be caught and logged to the console.
 */
function removeStoredProductForms() {
    formArrayObjects = [];

    try {
        removeItemFromLocalStorage("basic-product-information-form");
        removeItemFromLocalStorage("detailed-description-form");
        removeItemFromLocalStorage("pricing-inventory-form");
        removeItemFromLocalStorage("image-media-form");
        removeItemFromLocalStorage("shipping-and-delivery-form");
        removeItemFromLocalStorage("seo-and-meta-form");
        removeItemFromLocalStorage("additional-information-form");
    } catch (error) {
        console.log(error);
    }
}


function getProductsOrCreate() {
    let products = getItemFromLocalStorage("products-list", true);
    if (!products) {
        products = [];
    };
    
    return products;
}


getBasicInformation();
getDetailedProductInformation();
getPricingInventoryInformation();
getImageAndMediaInformation();
getShippingInformation();
getSEOAndMetaInformation();
getAdditionalInformation();


