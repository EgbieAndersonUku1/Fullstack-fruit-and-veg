import { validateElement } from "../errors/customErrors.js";
import showSpinner from "../utils/spinner.js";
import { StarRating } from "./renderStar.js";
import splitStringByDelimiter from "../utils/parser.js";



const deleteLink           = document.getElementById("delete-testimonial-link");
const moodleAlert          = document.getElementById("moodle-alert");
const spinnerElement       = document.querySelector(".spinner");
const ratingsContainer     = document.querySelector(".testimonial-ratings");
const filledStarsSrc       = "../../../static/img/icons/star-filled.svg";
const unfilledStarsSrc     = "../../../static/img/icons/star-unfilled.svg";
const confirmDelete        = document.querySelector(".confirm-delete");
const cancelDelete         = document.querySelector(".cancel-delete");


// validate the elements
validateElement(deleteLink, "The delete link is not a valid HTML instance");
validateElement(confirmDelete, "The confirm delete link button is not a valid HTML instance");
validateElement(moodleAlert, "The moodle Alert is not a valid html instance");
validateElement(ratingsContainer, "The ratings container couldn't be found");


document.addEventListener("DOMContentLoaded", handleSetUp);


// initialised the rating class
const starRatings = new StarRating(ratingsContainer, {
                                filledStarsSrc: filledStarsSrc,
                                unfilledStarsSrc: unfilledStarsSrc,
                                isInteractive:false,
                                });


deleteLink?.addEventListener("click", handleConfirmDeleteLink);
cancelDelete?.addEventListener("click", handleCancelDelete);
confirmDelete?.addEventListener("click", handleConfirmDelete);


function handleSetUp() {
    let id;

    if (ratingsContainer) {
        id = ratingsContainer.id;
    }
  
    if (!id) {
        console.error("The id for the ratings couldn't be found");
    } else  {
    
        id = splitStringByDelimiter(id, "-")[1];
        starRatings.numOfRatedStars = parseInt(id);
        starRatings.initialise();
       
    }
}






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

