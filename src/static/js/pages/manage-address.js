import fetchData from "../utils/fetch.js";
import AlertUtils from "../utils/alerts.js";
import { validateElement } from "../errors/customErrors.js";



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
  

    if (elementValue.toLowerCase() === MARK_AS_PRIMARY.toLowerCase()) {
        // do something to be added here later

        return;
    } 

    handleAddressDeletion(id, billingAddressType);

  
}

async function mark_as_primary_address(id, billingAddressType) {
    const url  = "profile/mark_as_primary/"
    const body = {is_billing_address: billingAddressType.toLowerCase() === "billing_address", address_id: id};


    try {
        const response = await fetchData({url:url, csrfToken:CSRF_TOKEN, body:body });

        if (response.SUCCESS) {
            const previousAddressDivID    = id;  
            const newPrimaryAddressData   = response.DATA.Address;
            const previousPrimaryAddress  = getPrimaryAddressDisplay()

          
            swapAddressPositions(newPrimaryAddressData, previousPrimaryAddress, previousAddressDivID) 
          
            
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
  
    const url  = "/profile/delete_address/";
    const body = {is_billing_address: billingAddressType.toLowerCase() === "billing_address",
                 address_id: id,
                 _method: "DELETE"  // simulate delete since browser is actually not allowing for a DELETE request
                }
   
    try {

        const response = await fetchData({url:url,
            csrfToken:CSRF_TOKEN, 
            body:body, 
            });

        if (response.SUCCESS) {
            const addressDiv = document.getElementById(id);
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
    // console.log(billingAddressTitle)
};



function hideShippingAddressElements() {
    shippingAddressContainerElement?.classList.add("d-none");
    const shippingAddressTitleElement = document.getElementById("shipping-address-title");
    shippingAddressTitleElement?.classList.add("d-none");
    // console.log(shippingAddressTitleElement);
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
 * @param {Object} newPrimaryAddressData - The data for the new primary billing address.
 * @param {HTMLElement} previousPrimaryAddress - The DOM element representing the previous primary address.
 * @param {HTMLElement} previousAddressDivID - The DOM element representing the id where the previous primary address should be placed.
 *
 * Example:
 * swapAddressPositions(newPrimaryAddressData, previousPrimaryAddress, previousAddressPosition);
 */
function swapAddressPositions(newPrimaryAddressData, previousPrimaryAddress, previousAddressDivID) {
    // Function logic here
    //TODO
    //
}
