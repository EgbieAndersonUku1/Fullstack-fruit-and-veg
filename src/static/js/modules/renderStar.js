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
 * This function is responsible for creating rating stars. Based on the flag the function
 * can create a series of empty stars or non-empty stars
 * 
 * @param {*} numOfStarsToCreate The number of stars to create
 * @param {*} rating The rating number for each coloured star e.g a single star has rating of 1, two stars = 2, three star = 3, n stars = n
 * @param {*} totalNumberOfStars The total number of stars to create the default is 5
 * @param {*} createEmptyStars A flag to decide whether to create an empty star or a non-empty star. The default is set to false which means
 *                              it doesn't creates an empty star
 * @returns 
 *     
 */
function createRatingStars(numOfStarsToCreate, rating, totalNumberOfStars = 5, createEmptyStars=false) {
    const fragment = document.createDocumentFragment();

    if (typeof numOfStarsToCreate !== "number" || (typeof rating  !== "number") || (typeof totalNumberOfStars !== "number")) {
        throw new Error("One or more of the parameters entered is not a number");
    }
    
    for (let i = 1; i <= totalNumberOfStars; i++) {
        const aTag   = createElement("a");
        const imgTag = createElement("img");

        aTag.dataset.value   = i;
        imgTag.dataset.value = i;
        aTag.id              = rating;
        aTag.href            = "#";

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

