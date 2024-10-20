import splitStringByDelimiter from "../utils/parser.js";
import { renderStars } from "../modules/delete-review.js";

const testimonials = document.querySelectorAll(".testimonial-ratings");

document.addEventListener("DOMContentLoaded", handleSetUp);


function handleSetUp() {

    testimonials.forEach((testimonial) => {
        if (testimonial) {

            const id       = splitStringByDelimiter(testimonial.id, "-")[1];
            const selector = `#${testimonial.id}`;

            renderStars(id, selector);
            console.log(testimonial);
        };
       
    })

}



