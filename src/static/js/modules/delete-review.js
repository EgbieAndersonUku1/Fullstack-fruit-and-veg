import { validateElement } from "../errors/customErrors.js";
import showSpinner from "../utils/spinner.js";
import { createRatingStars } from "./renderStar.js";
import splitStringByDelimiter from "../utils/parser.js";



const deleteLink           = document.getElementById("delete-testimonial-link");
const moodleAlert          = document.getElementById("moodle-alert");
const spinnerElement       = document.querySelector(".spinner");
const ratingsContainer     = document.querySelector(".testimonial-ratings");
const confirmDelete        = document.querySelector(".confirm-delete");
const cancelDelete         = document.querySelector(".cancel-delete");

validateElement(deleteLink, "The delete link is not a valid HTML instance");
validateElement(confirmDelete, "The confirm delete link button is not a valid HTML instance");
validateElement(moodleAlert, "The moodle Alert is not a valid html instance");
validateElement(ratingsContainer, "The ratings container couldn't be found");


document.addEventListener("DOMContentLoaded", handleSetUp);

deleteLink?.addEventListener("click", handleConfirmDeleteLink);
cancelDelete?.addEventListener("click", handleCancelDelete);
confirmDelete?.addEventListener("click", handleConfirmDelete);


function handleSetUp() {
    let id = ratingsContainer.id;
    if (!id) {
        console.error("The id for the ratings couldn't be found");

    }
   
   id = splitStringByDelimiter(id, "-")[1];

   renderStars(id);
}



/**
 * Renders a specified number of stars into a given container element.
 *
 * The function creates star elements (based on the number provided) and
 * appends them to a specified container. If the container is not found
 * or if the input is invalid, an error will be thrown.
 *
 * @param {number} numOfStarsToRender - The number of stars to render (can be an integer or a float).
 * @param {string} [ratingsContainerSelector=".testimonial-ratings"] - The CSS selector of the container element where the stars will be rendered. 
 *                                                                   Defaults to ".testimonial-ratings".
 * @throws {Error} If the container element cannot be found or if `numOfStarsToRender` is not a valid number.
 */
export function renderStars(numOfStarsToRender, ratingsContainerSelector=".testimonial-ratings") {
    const ratingsContainer     = document.querySelector(ratingsContainerSelector);

    if (!ratingsContainer) {
        throw new Error("The container for the ratings couldn't be found");
    };

    ratingsContainer.innerHTML = ""
    
    if (isNaN(numOfStarsToRender)) {
        throw new Error("The `numOfStarsToRender` must be an integer or a float");
    };

    const starsToRender  = parseInt(numOfStarsToRender);
    const starsElement   = createRatingStars(starsToRender, starsToRender);

    ratingsContainer.appendChild(starsElement);
    

};


function handleConfirmDeleteLink(e) {
    e.preventDefault();
 
    
    showSpinner({spinnerElement:spinnerElement});
    moodleAlert.classList.remove("d-none");
 
};

function handleCancelDelete(e) {
    e.preventDefault();
    
    showSpinner({spinnerElement:spinnerElement});
    moodleAlert.classList.add("d-none");
};



function handleConfirmDelete(e) {
    showSpinner({spinnerElement:spinnerElement});
}

