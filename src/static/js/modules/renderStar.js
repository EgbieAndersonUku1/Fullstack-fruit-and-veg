const filledStarsSrc      = "../../../static/img/icons/star-filled.svg";
const unfilledStarsSrc    = "../../../static/img/icons/star-unfilled.svg";

const ratingDiv            = document.querySelector(".product-ratings");
const clearBtn             = document.getElementById("clear-btn");


addEventListenerToStar();



function addEventListenerToStar() {

    if (ratingDiv) {
        ratingDiv.addEventListener("click", handleStarClick);
    }
   
}


function handleStarClick(e) {

    if (e.target.tagName === 'A' || e.target.tagName === 'IMG') {
        e.preventDefault();
        
        toggleClearBtn();
      
  
        const star = e.target.closest('a');
        renderStar(parseInt(star.dataset.value));

    }
}



/**
 * Renders stars in the ratingDiv element.
 * 
 * This function clears the ratingDiv element and appends a new set of stars to it.
 * By default, it renders colored stars. If the renderEmptyStars flag is set to true,
 * it renders empty, uncoloured stars.
 * 
 * @param {number} numOfStars - The number of stars to render.
 * @param {boolean} [renderEmptyStars=false] - Flag to determine if the stars should be empty (uncoloured).
 *                                             If true, renders empty stars.
 *                                             If false, renders coloured stars.
 */
function renderStar(numOfStars, renderEmptyStars=false) {
    ratingDiv.innerHTML = "";
    let stars;
    if (!renderEmptyStars) {
        stars = createRatingStars(numOfStars, numOfStars);
    } else {
        stars = createRatingStars(numOfStars, numOfStars, numOfStars, true);
        toggleClearBtn(false);
       
    }
    ratingDiv.appendChild(stars);
}



/**
 * Creates a series of star elements (filled or unfilled) based on the provided rating.
 * The function generates a fragment containing anchor (`<a>`) elements with embedded 
 * images (`<img>`) representing stars. You can control the total number of stars, 
 * the number of filled stars, and whether empty stars should be rendered.
 *
 * @param {number} numOfStarsToCreate - The number of filled stars to create.
 * @param {number} rating - The rating number associated with each filled star (e.g., 1 for one star, 2 for two stars).
 * @param {number} [totalNumberOfStars=5] - The total number of stars to create (default is 5).
 * @param {boolean} [createEmptyStars=false] - A flag indicating whether to create empty stars (default is false).
 * 
 * @returns {DocumentFragment} A fragment containing the star elements (`<a>` with `<img>` for each star).
 * 
 * @throws {Error} Throws an error if any of the input parameters (`numOfStarsToCreate`, `rating`, or `totalNumberOfStars`) are not numbers.
 */
function createRatingStars(numOfStarsToCreate, rating, totalNumberOfStars = 5, createEmptyStars=false) {
    const fragment = document.createDocumentFragment();

    if (typeof numOfStarsToCreate !== "number" || (typeof rating  !== "number") || (typeof totalNumberOfStars !== "number")) {
        throw new Error("One or more of the parameters entered is not a number");
    }
    
    for (let i = 1; i <= totalNumberOfStars; i++) {
        const aTag   = createElement("a");
        const imgTag = createElement("img");

        aTag.id              = rating;
        aTag.href            = "#";
        aTag.dataset.value   = i;
        imgTag.dataset.value = i;

        if (i <= numOfStarsToCreate && (!createEmptyStars)) {
            imgTag.src = filledStarsSrc;
            imgTag.alt = "star-filled";
            imgTag.classList.add("star-filled", "star-rating");
          
           
        } else {
            imgTag.src = unfilledStarsSrc;
            imgTag.alt = "star-unfilled";
            imgTag.classList.add("star-unfilled", "star-rating");
         
         
        }

        aTag.appendChild(imgTag);
        fragment.appendChild(aTag);
    }
    return fragment;
}


function createElement(elementTagToCreate) {
    return document.createElement(elementTagToCreate);
}


function toggleClearBtn(show=true) {
     clearBtn.style.display = show ? "block" : "none"
   
}

export {
    renderStar,
    createRatingStars,
}

