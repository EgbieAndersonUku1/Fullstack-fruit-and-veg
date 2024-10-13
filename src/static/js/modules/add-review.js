import renderStar  from "./reviews.js";

import { minimumCharactersToUse } from "../components/characterCounter.js";
import { handleFormFieldElement } from "../handlers/handleTextCharInput.js";

const testimonialTextArea = document.getElementById("id_testimonial_text");
const clearBtnElement     = document.getElementById("clear-btn");
const createReviewForm    = document.getElementById("product-review-form");
const messageDivElement   = document.querySelector(".messages");
const messagePTagElement   = document.querySelector(".messages p");


// Event listeners
createReviewForm.addEventListener("submit", handleCreateReviewFormSubmit);
clearBtnElement.addEventListener("click", handleResetRatings)



function getProductStarRating() {

    const productRatingStars = document.querySelectorAll(".product-ratings a img");
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



function handleCreateReviewFormSubmit(e) {
    e.preventDefault();

    const reviewReport = getProductStarRating();
 
    // Handle rating validation
    if (reviewReport.numOfStarsRated === 0) {
        msg = "You must rate the product before submitting";
        handleMessageDisplay(msg);
    } else {
       

        // functionality will be added later here

       return;
     
    }
}


function handleMessageDisplay(msg, classColor="dark-red-bg", displayInMs=4000) {
   
    messagePTagElement.textContent = msg;
    messageDivElement.classList.add("show", classColor);

    setTimeout(() => {
        messageDivElement.classList.remove("show", classColor);
    }, displayInMs)
}



function handleResetRatings() {
    const totalNumberOfStars = 5;
    const renderEmptyStars   = true;
     renderStar(totalNumberOfStars, renderEmptyStars);
}



// Render the minimum characters to use
minimumCharactersToUse(testimonialTextArea, {minCharClass: ".minimum-characters",
                                                      maxCharClass: ".maximum-characters",              
                                                      minCharMessage: "Minimum characters to use: ",
                                                      maxCharMessage: "Number of characters remaining: ",
                                                      minCharsLimit: 50,
                                                      maxCharsLimit: 1000,
                                                      disablePaste: true,
});



function handleReviewTitleField(titleSelectorID="#product-input-title", iconSelector="#review-title-icon"){
    handleFormFieldElement(titleSelectorID, iconSelector)
}

function handleReviewDescriptionTextArea(textAreaSelectorID = "#review-description-textArea", iconSelector = "#review-description-icon") {
    handleFormFieldElement(textAreaSelectorID, iconSelector);
}





