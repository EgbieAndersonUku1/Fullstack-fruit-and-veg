import addNewProductPages from "../pages/pages.js";
import { redirectToNewPage } from "../utils/utils.js";
import { minimumCharactersToUse } from "./characterCounter.js";
import loadFile from "../utils/loader.js";
import { getItemFromLocalStorage, saveToLocalStorage } from "../utils/utils.js";
import { getFormEntries, getMinCharCount } from "../utils/formUtils.js";


const productNameErrorMsg       = document.getElementById("product-name-error-msg");
const selectCategoryErrorMsg    = document.getElementById("select-category-error-msg");
const brandErrorsg              = document.getElementById("brand-error-msg");
const skuErrorMsg               = document.getElementById("sku-error-msg");
const upcErrorMsg               = document.getElementById("upc-error-msg");
const shortDescriptionErrorMsg  = document.getElementById("short-description-error-msg");


// form
const basicForm = document.getElementById("basic-product-information-form");


// field selectors for textArea fields
const detailDescriptionTextAreaSelector   = "#detailed-description";
const shortDescriptionTextAreaSelector    = "#short-description";
const metaDescriptionTextAreaSelector     = "#meta-description";
const warrantyDescriptionTextAreaSelector = "#warranty-description";


// basic category fields
const selectProductCategoryElement  = document.getElementById("select-category");
const addCategoryLabelElement       = document.getElementById("add-category-label");
const addCategoryInputFieldElement  =  document.getElementById("add-category");
const basicFormTextAreaFieldElement = document.getElementById("short-description");




// Text area field inside inside the detail description specs page
minimumCharactersToUse(detailDescriptionTextAreaSelector, {
                        minCharClass: '.minimum-characters',
                        minCharMessage: 'Minimum characters to use: ',
                        maxCharClass: '.maximum-characters',
                        maxCharMessage: 'Number of characters remaining: ',
                        minCharsLimit: 50,
                        maxCharsLimit: 1000
                        });



// Text area field for the basic product information page
minimumCharactersToUse(shortDescriptionTextAreaSelector, {
                                minCharClass: '.minimum-characters',
                                minCharMessage:'Minimum characters to use: ',
                                maxCharClass: '.maximum-characters',
                                maxCharMessage: 'Number of characters remaining: ',
                                minCharsLimit: 50,
                                maxCharsLimit: 255,

})



// Text area field for the meta description page
minimumCharactersToUse(metaDescriptionTextAreaSelector, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 10,
    maxCharsLimit: 500,
    });


// Text area field for the meta description page
minimumCharactersToUse(warrantyDescriptionTextAreaSelector, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 2000,
    });



// handle select category event listener
selectProductCategoryElement?.addEventListener("change", handleSelectClick);


function handleSelectClick(e) {
    const value = selectProductCategoryElement.value.toLowerCase();
    
    if (value === "new-category") {
        addCategoryLabelElement.style.display = "block";
        addCategoryInputFieldElement.style.display = "block";
    } else {
        addCategoryLabelElement.style.display = "none";
        addCategoryInputFieldElement.style.display = "none";
    }
}





function nextPage(event, step) {
    event.preventDefault();

    const pageNumber = parseInt(step);
    const page = addNewProductPages[pageNumber];

   

    // TODO: Handle form data for each page here.
    // For now, just redirect to the next page as part of the Minimum Viable Product (MVP).

    if (!page) {
        throw new Error("Something went wrong and the page number couldn't be found!!!");
    }

    // use the if-statement for now, later switch it to a switch statement
    if (pageNumber - 1 === 1) {
       handleBasicInformationForm(pageNumber)
    }
    if (pageNumber - 1 === 2) {
        // handleBasicInformationForm(pageNumber)
        null;
     }

   
}


function prevPage(event, pageNumber) {
    event.preventDefault();
    const page = addNewProductPages[parseInt(pageNumber)];

    
     // TODO: Handle form data for each page here.
    // For now, just redirect to the previous page as part of the Minimum Viable Product (MVP).

    if (!page) {
        throw new Error("Something went wrong and the page number couldn't be found!!!");
    }

    redirectToNewPage(page);
}


window.nextPage = nextPage;
window.prevPage = prevPage;




// populate field
async function populateCountrySelect() {
    const countriesSelectForm = document.querySelector("#countries");

    if (!countriesSelectForm) {
        console.warn("The countries elements selector wasn't found!!")
        return;
    }
    try {
        const filePath      = "../../../../countries.txt";
        const countriesData = await loadFile(filePath);

        if (countriesData) {
            const countries = countriesData.split('\n');

            countries.forEach((country) => {
                const value = country;
                const text  = country;

                const option = createOption(value, text);
                countriesSelectForm.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function createOption(value, text) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = text;
    return option
}



function handleBasicInformationForm(pageNumber) {
    if (!basicForm) {
        throw new Error("Something went wrong and the form elements couldn't be found!!!");
    }

    const addProductObj = getAddProductDictOrCreate();
    const formEntries = getFormEntries(basicForm);

    const fields = [
        {name: 'product-name', value: formEntries['product-name'], errorMsg: productNameErrorMsg, 
         fieldType: "text", minCharCount: null
        },

        {name: 'select-product-category', value: formEntries['select-a-category'], 
         errorMsg: selectCategoryErrorMsg, fieldType: "select", minCharCount: null
        },

        {name: 'brand', value: formEntries['brand'], errorMsg: brandErrorsg, fieldType: "text", minCharCount: null},

        {name: 'sku', value: formEntries['sku'], errorMsg: skuErrorMsg, fieldType: "text", minCharCount: null},

        {name: 'upc', value: formEntries['upc'], errorMsg: upcErrorMsg, fieldType: "text", minCharCount: null},

        {name: 'short-description', value: formEntries['short-description'], 
         errorMsg: shortDescriptionErrorMsg, fieldType: "textarea", 
         minCharCount: getMinCharCount(basicFormTextAreaFieldElement)}
    ];

    const formComplete = validateAndProcessFields(fields, addProductObj);
    handleFormCompletion(formComplete, addProductObj, pageNumber);
}


function validateAndProcessFields(fields, addProductObj) {
    let formComplete = true;

    fields.forEach((field) => {
      
        if (!field.value) {
            showErrorMsg(field.errorMsg);
            formComplete = false;
        } else {
            addProductObj[field.name]  = field.value;  
            showErrorMsg(field.errorMsg, false);
          
        }

        // Check if the user has entered the minimum number of characters for textarea fields
        if (field.fieldType === "textarea"  && field.value.length < field.minCharCount) {
            formComplete = false;
        } 
           
    });


    return formComplete;
}


function handleFormCompletion(formComplete, addProductObj, pageNumber) {
    
    if (!formComplete) {
        alert("One or more of the form details is incomplete");
    } else {
       
        saveToLocalStorage("addProduct", addProductObj, true);
        redirectToNewPage(addNewProductPages[pageNumber]);
    }
}



function getAddProductDictOrCreate() {
    let addProduct = getItemFromLocalStorage("addProduct", true);

    if (!addProduct) {
        addProduct = {};
    };
    return addProduct;
}




function showErrorMsg(msgElement, show=true) {
    msgElement.style.display = show ? "block": "none"
}


populateCountrySelect();
