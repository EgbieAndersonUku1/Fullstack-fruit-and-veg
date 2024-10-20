import { validateElement } from "../errors/customErrors.js";
import showSpinner from "../utils/spinner.js";
import { createRatingStars } from "./renderStar.js";
import splitStringByDelimiter from "../utils/parser.js";


const ratingsContainer     = document.querySelector(".testimonial-ratings");
const deleteLink           = document.getElementById("delete-testimonial-link");
const moodleAlert          = document.getElementById("moodle-alert");
const spinnerElement       = document.querySelector(".spinner");

const confirmDelete        = document.querySelector(".confirm-delete");
const cancelDelete         = document.querySelector(".cancel-delete");

validateElement(deleteLink, "The delete link is not a valid HTML instance", true);
validateElement(confirmDelete, "The confirm delete link button is not a valid HTML instance", true);
validateElement(moodleAlert, "The moodle Alert is not a valid html instance", true);
validateElement(ratingsContainer, "The ratings container couldn't be found", true);


document.addEventListener("DOMContentLoaded", handleSetUp);

deleteLink.addEventListener("click", handleConfirmDeleteLink);
cancelDelete.addEventListener("click", handleCancelDelete);
confirmDelete.addEventListener("click", handleConfirmDelete);


function handleSetUp() {
    let id = ratingsContainer.id;
    if (!id) {
        console.error("The id for the ratings couldn't be found");

    }
   
   id = splitStringByDelimiter(id, "-")[1];

   renderStar(id);
}


function renderStar(numOfStarsToRender) {
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

