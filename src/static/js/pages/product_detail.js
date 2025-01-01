import { minimumCharactersToUse } from "../components/characterCounter.js";
import { StarRating }             from "../modules/renderStar.js";
import { validateElement }        from "../errors/customErrors.js";


const detailDescriptionTextAreaElement  = document.getElementById("product-description-area");
const filledStarsSrc                    = "../../../static/img/icons/star-filled.svg";
const unfilledStarsSrc                  = "../../../static/img/icons/star-unfilled.svg";
const ratingsContainer                  = document.querySelector(".product-ratings");
const sizes                             = document.querySelector(".sizes");
const productColors                     = document.querySelector(".product-colors");
const mainImageContainer                = document.querySelector(".product-main-image");
const detailsPageContainer              = document.querySelector("#details-page .container");


// validate elements
validateElement(detailsPageContainer, "The main container HTML is not a valid HTML instance", true);
validateElement(mainImageContainer, "The main container HTML is not a valid HTML instance", true);



// handle event listener
detailsPageContainer.addEventListener("click", handleClick);



// Enables the star ratings in the UI to be interactive, allowing users to rate items
const starRatings = new StarRating(ratingsContainer, {
                                filledStarsSrc: filledStarsSrc,
                                unfilledStarsSrc: unfilledStarsSrc,
                                isInteractive:true,
                                });
                         
starRatings.initialise();


// Listen for visibility changes (when the page becomes hidden or visible)
document.addEventListener("visibilitychange", function() {
    if (document.hidden) {
        starRatings.destroy();
    }
});


// Listen for page unload (reload or navigation away from the page)
window.addEventListener("beforeunload", function() {
    starRatings.destroy();
});


// Listen for SPA-like navigation events (e.g., history navigation)
window.addEventListener("popstate", function() {
    starRatings.destroy();
});



// Displays the remaining character count and minimum character requirement for a text area
minimumCharactersToUse(detailDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 255,
    disablePaste: true,
})


/**
 * Handles click events within the #details-page .container element.
 * Delegates event handling to specific functions based on the class of the clicked div element.
 *
 * @param {Event} e - The click event object.
 *
 * Behaviour:
 * - If the clicked or nearest parent `div` element has the class "size",
 *   calls `handleSelectSize` with the event.
 * - If the clicked or nearest parent `div` element has the class "color",
 *   calls `handleProductColorSelect` with the event.
 * - If the clicked or nearest parent `div` element has the class "product-side-images",
 *   calls `swapImages` with the event.
 * - If no matching class is found, logs a warning with the unhandled class.
 */
function handleClick(e) {

    const divElement = e.target.closest("div");

    if (!divElement) return; 
    
    const classList = divElement.classList;

    switch (true) {
        case classList.contains("size"):
            handleSelectSize(e);
            break;
        case classList.contains("color"):
            handleProductColorSelect(e);
            break;
        case classList.contains("product-side-images"):
            const sideImage = e.target.closest("img");
            swapImages(mainImageContainer, sideImage);
            break;
        default:
            console.warn("Unhandled class:", divElement.className);
    }

  
}


/**
 * Handles the click event for selecting a size by deselects all size elements, 
 * and highlights the selected size.
 * 
 * @param {Event} e - The click event.
 */
function handleSelectSize(e) {
    handleElementHelper(e, sizes);
}



/**
 * Handles the click event for selecting a product color by deselects all color elements, 
 * and highlights the selected color.
 * 
 * @param {Event} e - The click event.
 */
function handleProductColorSelect(e) {
    handleElementHelper(e, productColors);
}



/**
 * A helper function to handle selecting an element by deselecting all elements in the container
 * and highlighting the clicked element.
 * 
 * @param {Event} e - The click event.
 * @param {HTMLElement} container - The container holding the elements to be deselected and selected.
 */
function handleElementHelper(e, elementsContainer) {

    e.preventDefault();
    deselectAllElements(elementsContainer);

    const element = e.target.closest("div");
    highlightSelectedElement(element);
}



/**
 * Highlights the given element by changing its background color.
 * Throws an error if the element is not valid.
 * 
 * @param {HTMLElement} element - The HTML element to highlight.
 * @throws {Error} If the element is not valid.
 */
function highlightSelectedElement(element) {
    if (!element) {
        throw new Error("Something went wrong and the element couldn't be selected");
    }
    element.style.background = "grey";
}



/**
 * Deselects all child elements (divs) of the provided container by resetting 
 * their background color. Validates the container before proceeding.
 * 
 * @param {HTMLElement} container - The container element that holds the divs to be deselected.
 * @throws {Error} If the container or its child elements are not valid.
 */
function deselectAllElements(container) {
    validateElement(container, "The HTML element is not valid", true);

    const elements = container.querySelectorAll("div");

    if (!elements) {
        throw new Error("Something went wrong and the containment elements couldn't be deselected");
    }

    const dodgerBlue = "#1E90FF";
    elements.forEach((element) => {
        element.style.background = dodgerBlue;
    });
}



/**
 * Swaps the source of the main image with the provided image.
 *
 * @param {HTMLElement} mainImageContainer - The container element holding the main image.
 * @param {HTMLElement} imageToSwapWith - The image element to swap with the main image.
 * @throws Will throw an error if one or more of the image elements is not found.
 */
function swapImages(mainImageContainer, imageToSwapWith) {

    if (!mainImageContainer || !imageToSwapWith) {
        throw new Error("One or more of the image containers wasn't found");
    };

    const mainImage     = mainImageContainer.querySelector("img");
    const mainImageCopy = mainImage.src;
    
    mainImage.src       = imageToSwapWith.src;
    imageToSwapWith.src = mainImageCopy;
}
