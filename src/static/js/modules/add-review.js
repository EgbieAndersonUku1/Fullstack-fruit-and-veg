import { StarRating } from "./renderStar.js";
import { validateElement } from "../errors/customErrors.js";
import { minimumCharactersToUse } from "../components/characterCounter.js";

const testimonialTextArea  = document.getElementById("id_testimonial_text");
const testimonialForm      = document.getElementById("testimonial-form");
const messageDivElement    = document.querySelector(".messages");
const messagePTagElement   = document.querySelector(".messages p");


// Event listeners
testimonialForm?.addEventListener("submit", handleTestimonialFormSubmit);


const filledStarsSrc     = "../../../static/img/icons/star-filled.svg";
const unfilledStarsSrc   = "../../../static/img/icons/star-unfilled.svg";
const ratingsContainer   = document.querySelector(".product-ratings");

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


// Render the minimum characters to use
minimumCharactersToUse(testimonialTextArea, {minCharClass: ".minimum-characters",
    maxCharClass: ".maximum-characters",              
    minCharMessage: "Minimum characters to use: ",
    maxCharMessage: "Number of characters remaining: ",
    minCharsLimit: 50,
    maxCharsLimit: 1000,
    disablePaste: true,
});





export function getTestimonialStarRating(imgClass=".product-ratings a img") {

    const productRatingStars = document.querySelectorAll(imgClass);
    const reviewedReport = {
        isRated: false,
        numOfStarsRated: 0
    };
    const [EMPTY_STARS, COLORED_STARS] = ["star-unfilled", "star-filled"];

    if (productRatingStars.length === 0) {
        throw new Error("The product star rating couldn't be found");
    }
   
    for (let i = 0; i < productRatingStars.length; i++) {
        const ratingStar = productRatingStars[i];
        
        if (i === 0 && ratingStar.alt === EMPTY_STARS) {
            reviewedReport.numOfStarsRated = 0;
            reviewedReport.isRated = false;
            break;
        } else if (ratingStar.alt === COLORED_STARS) {
            reviewedReport.numOfStarsRated += 1;
        }
    }

    if (reviewedReport.numOfStarsRated > 0) {
        reviewedReport.isRated = true;
    }
   
    return reviewedReport;
}



function handleTestimonialFormSubmit(e) {
    e.preventDefault();

    const reviewReport = getTestimonialStarRating();
 
    // Handle rating validation
    if (reviewReport.numOfStarsRated === 0) {
        const msg = "You must rate the product before submitting";
        handleMessageDisplay(msg);
    } else {
       
        const starHiddenInputField = document.getElementById("starInputHiddenField");
        validateElement(starHiddenInputField, "The input field is not a valid element field", true);
        starHiddenInputField.value = reviewReport.numOfStarsRated;
        
        testimonialForm.submit();
       return true;
     
    };
}


function handleMessageDisplay(msg, classColor="dark-red-bg", displayInMs=4000) {
   
    messagePTagElement.textContent = msg;
    messageDivElement.classList.add("show", classColor);

    setTimeout(() => {
        messageDivElement.classList.remove("show", classColor);
    }, displayInMs)
}









