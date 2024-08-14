const addToCartMsg         = document.querySelector(".addToItem-logged-msg");
const dimBackgroundElement = document.querySelector(".dim-overlay");
const wishlistMsg          = document.querySelector(".wishlist-logged-msg");

/**
 * Closes the add-to-cart message and hides the dim background.
 */
function closeAddToCartMsg() {
    dimBackgroundElement.style.display = "none";
    addToCartMsg.style.display = "none";
}


/**
 * Closes the wishlist message and hides the dim background.
 */
function closeWishlistMessage() {
    dimBackgroundElement.style.display = "none";
    wishlistMsg.style.display = "none";
}


/**
 * Displays the add-to-cart message for a certain duration and dims the background.
 * After the specified time, hides both the message and the dim background.
 */
function displayAddToCartMessage() {
   
    addToCartMsg.style.display         = "flex";
    dimBackgroundElement.style.display = "block";
    
    const DISPLAY_TIME_MS = 3000; 

    setTimeout(() => {
        addToCartMsg.style.display = "none";
        dimBackgroundElement.style.display = "none";
    }, DISPLAY_TIME_MS);
}


/**
 * Displays the wishlist message and dims the background.
 * Prevents the default action of the event (e.g., navigation).
 * Note: This function is currently set to always display as "not logged in".
 * Changes are planned after backend integration.
 * 
 * @param {Event} e - The event object (e.g., click event) that triggered the display.
 */
function displayWishListMessage(e) {
    e.preventDefault();

    dimBackgroundElement.style.display = "block";
    wishlistMsg.style.display = "flex";
}


export {
  
    closeAddToCartMsg,
    closeWishlistMessage,
    displayAddToCartMessage,
    displayWishListMessage,
}