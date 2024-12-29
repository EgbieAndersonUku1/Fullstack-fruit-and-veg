import splitStringByDelimiter from "../utils/parser.js";
import { StarRating } from "../modules/renderStar.js";

const testimonials = document.querySelectorAll(".testimonial-ratings");

document.addEventListener("DOMContentLoaded", handleSetUp);

const filledStarsSrc     = "../../../static/img/icons/star-filled.svg";
const unfilledStarsSrc   = "../../../static/img/icons/star-unfilled.svg";
const ratingsContainer   = document.querySelector(".product-ratings");


const starRatings = new StarRating(ratingsContainer, {
                                filledStarsSrc: filledStarsSrc,
                                unfilledStarsSrc: unfilledStarsSrc,
                                isInteractive:false,
                                });



function handleSetUp() {

    testimonials.forEach((testimonial) => {
        if (testimonial) {

            const id                    = splitStringByDelimiter(testimonial.id, "-")[1];
            starRatings.numOfRatedStars = parseInt(id);
            starRatings.initialise();

    
        };
       
    })

}



