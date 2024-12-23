import { renderStar } from "../modules/renderStar.js";
import { renderStars } from "../modules/delete-review.js";
import splitStringByDelimiter from "../utils/parser.js";
import { minimumCharactersToUse } from "../components/characterCounter.js";


const detailDescriptionTextAreaElement   = document.getElementById("product-description-area");
const productRatings                     = document.querySelector(".product-ratings");




productRatings.addEventListener("click", (e) => {
    e.preventDefault();
    console.log(e.target)
})



minimumCharactersToUse(detailDescriptionTextAreaElement, {
    minCharClass: '.minimum-characters',
    minCharMessage: 'Minimum characters to use: ',
    maxCharClass: '.maximum-characters',
    maxCharMessage: 'Number of characters remaining: ',
    minCharsLimit: 50,
    maxCharsLimit: 255,
    disablePaste: true,
})


