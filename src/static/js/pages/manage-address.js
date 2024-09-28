import fetchData from "../utils/fetch.js";
import AlertUtils from "../utils/alerts.js";


const BillingAddressesContainerElement = document.getElementById("billing-addresses");
const addressCardsElements             = document.querySelectorAll(".address-card");

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


    if (elementValue.toLowerCase() === MARK_AS_PRIMARY.toLowerCase()) {
        // do something to be added here
        return;
    } 

    handleAddressDeletion(id, billingAddressType);

  
}


/**
 *  Pusedocode - note to self delete afterwards
 * 1.  The user clicks the delete button
 * 2.  The function calls the addEventLister which be done by eventdelegation
 * 3.  The function calls the backend and deletes it from the model
 * 4.  If the delete is succesful the JS then removes the address DIV
 */


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

        console.log(response)
        if (response.SUCCESS) {
            const addressDiv = document.getElementById(id);
    
            if (addressDiv) {
                addressDiv.remove()
                AlertUtils.showAlert({
                            title: "Deletion successful",
                            text: "Successfully deleted address",
                            icon: "success",
                            confirmButtonText: "Great!!"
                        })

            } else {
                console.error('Error deleting address:', response.message);
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



