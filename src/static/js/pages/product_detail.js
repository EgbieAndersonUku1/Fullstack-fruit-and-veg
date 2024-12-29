import { getTestimonialStarRating } from "../modules/add-review.js";
import { minimumCharactersToUse } from "../components/characterCounter.js";
import { StarRating } from "../modules/renderStar.js";


const detailDescriptionTextAreaElement  = document.getElementById("product-description-area");
const filledStarsSrc                    = "../../../static/img/icons/star-filled.svg";
const unfilledStarsSrc                  = "../../../static/img/icons/star-unfilled.svg";
const ratingsContainer                  = document.querySelector(".product-ratings");

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




minimumCharactersToUse(detailDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 255,
    disablePaste: true,
})



getTestimonialStarRating();