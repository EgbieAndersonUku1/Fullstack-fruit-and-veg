import { validateElement } from "../errors/customErrors.js";
import showSpinner from "../utils/spinner.js";


const deleteLink           = document.getElementById("delete-testimonial-link");
const moodleAlert          = document.getElementById("moodle-alert");
const spinnerElement       = document.querySelector(".spinner");

const confirmDelete        = document.querySelector(".confirm-delete");
const cancelDelete         = document.querySelector(".cancel-delete");

validateElement(deleteLink, "The delete link is not a valid HTML instance", true);
validateElement(confirmDelete, "The confirm delete link button is not a valid HTML instance", true);
validateElement(moodleAlert, "The moodle Alert is not a valid html instance", true);



deleteLink.addEventListener("click", handleConfirmDeleteLink);
cancelDelete.addEventListener("click", handleCancelDelete);
confirmDelete.addEventListener("click", handleConfirmDelete);

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

