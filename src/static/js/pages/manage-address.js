import fetchData from "../utils/fetch.js";
import AlertUtils from "../utils/alerts.js";
import { validateElement } from "../errors/customErrors.js";
import splitStringByDelimiter from "../utils/parser.js";


const billingAddressesContainerElement = document.getElementById("billing-addresses");
const shippingAddressContainerElement  = document.getElementById("shipping_addresses");
const primaryAddressTitleElement       = document.getElementById("primary-address-title");
const emptyAddressMessageElement       = document.querySelector(".empty-address-message");

const addressCardsElements             = document.querySelectorAll(".address-card");
const primaryAddressElement            = document.getElementById("primary-address");

const CSRF_TOKEN = window.csrfToken;


addressCardsElements?.forEach((cardElement) => {
    cardElement?.addEventListener("click", handleLinkClick);
})


function handleLinkClick(e) {
    e.preventDefault();

    const billingAddressType = document.querySelector("input[type='hidden']").name
    const id               = e.target.id;
    const elementValue     = e.target.textContent.trim();
    const MARK_AS_PRIMARY  = "mark as primary";
    const DELETE           = "delete";
  
 
    if (elementValue.toLowerCase() === MARK_AS_PRIMARY) {
        mark_as_primary_address(id);
        return;
    } else if (elementValue.toLowerCase() === DELETE) {
          handleAddressDeletion(id, billingAddressType);
    }

  

  
}

async function mark_as_primary_address(id) {
    const url              = "/profile/mark_as_primary/"
    const billingAddressID = splitStringByDelimiter(id)?.pop()
    const body             = {address_id: billingAddressID};

    try {
        const response = await fetchData({url:url, csrfToken:CSRF_TOKEN, body:body });

        if (response.SUCCESS) {
            const billingAddressDivContainer   = document.getElementById(billingAddressID);
            const AddresessData                = response.DATA;
            const primaryAddressDiv            = getPrimaryAddressDisplay();
          
            swapAddressPositions(AddresessData, primaryAddressDiv, billingAddressDivContainer); 
          
            AlertUtils.showAlert({
                title: "Successful",
                text: "Successfully marked address as primary",
                icon: "success",
                confirmButtonText: "Great!!"
            })


        } else {
            console.error('Error marking address as primary:', response.MESSAGE);

            AlertUtils.showAlert({
                title: "unsuccessful",
                text: "Failed to mark address as primary. Please try again",
                icon: "error",
                confirmButtonText: "sorry!"
            })
        }

    } catch (error) {
        console.error('Error marking address as primary:', error);
        AlertUtils.showAlert({
            title: "Error occurred",
            text: "An error occurred. Please try again later.",
            icon: "error",
            confirmButtonText: "ok!"
        })
    }
}


async function handleAddressDeletion(id, billingAddressType) {
  
    const url        = "/profile/delete_address/";
    const addressID  = splitStringByDelimiter(id)?.pop() // Default delimiter ("-") id is "billing-address-`id-number-here`>"
    const body       = {is_billing_address: billingAddressType.toLowerCase() === "billing_address",
                        address_id: addressID,
                        _method: "DELETE"  // simulate delete since browser is actually not allowing for a DELETE request
                        }
   
    try {

        const response = await fetchData({url:url,
            csrfToken:CSRF_TOKEN, 
            body:body, 
            });

        if (response.SUCCESS) {
            const addressDiv = document.getElementById(addressID);
           
            if (addressDiv) {
                addressDiv.remove()
                handleAddressDisplay(response);
                AlertUtils.showAlert({
                            title: "Deletion successful",
                            text: "Successfully deleted address",
                            icon: "success",
                            confirmButtonText: "Great!!"
                        })

            } else {
                console.error('Error deleting address:', response.MESSAGE);
                AlertUtils.showAlert({
                    title: "Deletion unsuccessful",
                    text: "Failed to delete address. Please try again",
                    icon: "error",
                    confirmButtonText: "sorry!"
                })
            }
        }
    } catch (error) {
        console.error('Error deleting address:', error);
        AlertUtils.showAlert({
            title: "Error occurred",
            text: "An error occurred. Please try again later.",
            icon: "error",
            confirmButtonText: "ok!"
        })
    
    }
  
}


function handleAddressDisplay(response) {
 
    if (!response) {
        return;
    };

    if (response.REMAINING_SHIPPING_COUNT === 0 && response.REMAINING_BILLING_COUNT === 0) {
       hideAllAddressElements();
       handleEmptyAddressMessage();
    } else if (response.REMAINING_SHIPPING_COUNT > 0 && response.REMAINING_BILLING_COUNT === 0 ) {
        hideBillingAddressElements()
    } else if (response.REMAINING_SHIPPING_COUNT === 0 && response.REMAINING_BILLING_COUNT > 0  ){
        hideShippingAddressElements();
    } 
 
}


function handleEmptyAddressMessage(show = true) {
    validateElement(emptyAddressMessageElement, "The empty address element couldn't be found", true);
    if (show) {
        emptyAddressMessageElement.classList.remove("d-none");
    } else {
        emptyAddressMessageElement.classList.add("d-none");   
    }
   
}


function hideBillingAddressElements() {
    billingAddressesContainerElement?.classList.add("d-none");   
    const billingAddressTitleElement = document.getElementById("billing-address-title")
    billingAddressTitleElement?.classList.add("d-none");
  
};



function hideShippingAddressElements() {
    shippingAddressContainerElement?.classList.add("d-none");
    const shippingAddressTitleElement = document.getElementById("shipping-address-title");
    shippingAddressTitleElement?.classList.add("d-none");
}


function hideAllAddressElements() {
    billingAddressesContainerElement?.classList.add("d-none")
    shippingAddressContainerElement?.classList.add("d-none");

    const billingAddressTitle = document.getElementById("billing-address-title")
    const shippingAddressTitle = document.getElementById("shipping-address-title");

    billingAddressTitle?.classList.add("d-none");
    primaryAddressTitleElement?.classList.add("d-none");
    shippingAddressTitle?.classList.add("d-none");
    primaryAddressElement.classList?.add("d-none");
}




function getPrimaryAddressDisplay() {
    return document.querySelector(".primary_address");
}




/**
 * Swaps the position of the new primary address with the previous primary address.
 *
 * This function updates the DOM to reflect a change in the primary address.
 * It swaps the display of the new primary billing address with the previously 
 * designated primary address, and moves the previous primary to its original 
 * position in the list of billing addresses.
 *
 * @param {Object} AddressesData - The data for the new primary billing address.
 * @param {HTMLElement} primaryAddressDiv - The DOM element representing the previous primary address.
 * @param {HTMLElement} previousAddressDivID - The DOM element representing the id where the previous primary address should be placed.
 *
 * Example:
 * swapAddressPositions(AddressesData, primaryAddressDiv, previousAddressPosition);
 */
function swapAddressPositions(AddressesData, primaryAddressDiv, billingAddressDiv) {

   if (!(AddressesData && primaryAddressDiv && billingAddressDiv)) {
     console.log(`Address data -  ${AddressesData}`);
     console.log(`Billing address - ${billingAddressDiv}`);
     console.log(`Primary address - ${primaryAddressDiv}`);
     throw new Error("One or more of the parameter needed for the swap is missing");
   };

   validateElement(primaryAddressDiv, "The primary address element wasn't found", true);
   validateElement(billingAddressDiv, "The previous address element wasn't found", true);

   const addressCardId = `billing-address-${billingAddressDiv.id}`;
   const addressCard   = extractAddressCard(billingAddressDiv, addressCardId);

   fillInAddress(primaryAddressDiv, AddressesData.NewPrimaryAddress);
   fillInAddress(addressCard, AddressesData.BillingAddress);

  
   // change the parend div id to new billing address id
   billingAddressDiv.id = AddressesData.BillingAddress.id;


}




/**
 * Extracts an address card element from a container based on the provided id.
 * 
 * @param {HTMLElement} addressContainer - The HTML container element that holds the address cards.
 * @param {string} id - The id of the address card to be extracted.
 * @returns {HTMLElement|null} - The address card element if found, or null if not found.
 */
function extractAddressCard(addressContainer, id) {
    validateElement(addressContainer, "The field is not html element", true);

    if (!id) {
        console.warn("No id provided.");
        return null;
    }

    let addressId     = id.startsWith("#") ? id : `#${id}`;
    const addressCard = addressContainer.querySelector(addressId);

    if (!addressCard) {
        console.warn(`There was no address card associated with this id ${id}`);
        return null;
    }
    
    return addressCard;
   
}



/**
 * Fills in an address div with provided address data.
 * 
 * This function updates an HTML element that displays an address by populating 
 * its fields based on the given address data. 
 * 
 * @param {HTMLElement} addressDivToFill - The HTML element that represents the address card.
 * @param {Object} addressData - The address data to fill in the div. Expected fields:
 *                               Address_1 (string),
 *                               city (string), postcode (string), id (number or string).
 * 
 * @throws {Error} If the address div is not a valid HTML element or address data is empty.
 */
function fillInAddress(addressDivToFill, addressData) {

    validateElement(addressDivToFill, "The address div is not a valid HTML element", true);

    if (!addressData) {
        throw new Error("The address data cannot be empty");
    }

    // Validate addressData.id before proceeding
    if (!addressData.id) {
        throw new Error("The address data must have a valid id");
    }

    const fields             = extractAddressFields(addressDivToFill);
    const addressActionLinks = extractAddressFields(addressDivToFill, "a");

    if (fields) {
        try {

            addressDivToFill.id    = `billing-address-${addressData.id}`;
          
            fields.forEach((field) => {
               
                if (addressData.Address_1 && field.className === "address_1") {
                    field.textContent = addressData.Address_1;
                } else if (addressData.city && field.className === "city") {
                    field.textContent = addressData.city;
                } else if (addressData.postcode && field.className === "postcode") {
                    field.textContent = addressData.postcode;
                }
                
            })

           updateAddressActionLinks(addressActionLinks, addressData);
   
        } catch (error) {
            console.error("Couldn't parse the fields!")
        }
    }
};




/**
 * Extracts address fields from a given address container element based on the specified selector.
 *
 * @param {HTMLElement} addressDiv - The container element that holds the address fields.
 * @param {string} [selector="p"] - The CSS selector used to identify the address fields to extract.
 *                                   Defaults to "p" if no selector is provided.
 * @returns {NodeList} A NodeList of elements that match the specified selector within the address container.
 *                     If no matching elements are found, an empty NodeList is returned.
 * 
 * Raise an error if the address is not a valid HTML Element
 */
function extractAddressFields(addressDiv, selector="p") {
    validateElement(addressDiv, "The address div is not a valid HTML element", true);
    return addressDiv.querySelectorAll(selector);
}




/**
 * Updates the action links for address elements with unique IDs based on the provided address data.
 *
 * This function loops over a NodeList of action link elements (anchors) and assigns
 * unique IDs to the links based on their class names and the provided address data. 
 * Specifically, it updates the ID for links marked as 'mark-as-primary' and 'delete-address'.
 *
 * @param {NodeList} addressActionLinks - A NodeList of anchor elements representing action links for addresses.
 * @param {Object} addressData - An object containing data related to the address, including an `id` property
 *                               that is used to construct unique IDs for the action links.
 * @throws {Error} Throws an error if addressActionLinks is not a NodeList
 */
function updateAddressActionLinks(addressActionLinks, addressData) {
    try {
        addressActionLinks.forEach(anchor => {
            if (anchor.classList.contains('mark-as-primary')) {
                anchor.id = `mark_as_primary-${addressData.id}`;
            } else if (anchor.classList.contains('delete-address')) {
                anchor.id = `delete-billing-address-${addressData.id}`;
            }
        });
    } catch (error) {
        console.error(`The addressActionLinks must a NodeList not type ${typeof addressActionLinks}`)
    }
}
