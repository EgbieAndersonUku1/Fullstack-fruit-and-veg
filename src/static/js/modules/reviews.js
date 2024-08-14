import orders from "../../../order.js";
import createProductTable from "../components/createReviewTable.js";
import { filterByNotReviewed, 
    } from "../utils/filter.js";

import { getItemFromLocalStorage } from "../utils/utils.js";
import { 
        sortByDateAscending, 
        sortByDateDescending, 
        sortByNameAscending, 
        sortByNameDescending } from "../utils/sort.js";
import { getItemByID } from "../utils/itemUtils.js";


const filledStarsSrc   = "../../../static/img/icons/star-filled.svg";
const unfilledStarsSrc = "../../../static/img/icons/star-unfilled.svg";

const ratingDiv           = document.querySelector(".product-ratings");
const clearBtn            = document.getElementById("clear-btn");
const selectFilterDropdown  = document.getElementById("productFilterSelect");


addEventListenerToStar();


document.addEventListener("DOMContentLoaded", () => {
    createProductTable(orders)
})


selectFilterDropdown?.addEventListener("change", handleDropDown);


/**
 * Retrieves reviewed products from local storage and matches them with orders.
 * 
 * @returns {Array} - An array of reviewed products found in the orders.
 * @throws Will throw an error if productReviews is not an array.
 */
function getReviewed() {
    const productReviews = getItemFromLocalStorage("productReviews", true);

    if (!Array.isArray(productReviews)) {
        return null;
    }
    
    const reviewedItems = [];
    productReviews.forEach((productReview) => {
        const item = getItemByID(productReview.id, orders);
        if (item) {
            reviewedItems.push(item);
        }
    });

    return reviewedItems;
}


/**
 * Filters out reviewed items from the orders.
 * 
 * @returns {Array} - An array of items that have not been reviewed.
 */
function getNotReviewed() {
    const productReviews = getItemFromLocalStorage("productReviews", true);
   
    if (!Array.isArray(productReviews)) {
       return orders;
    }

    const ids = productReviews.map((productReview) => productReview.id);
   
    if (ids.length > 0) {
        return filterByNotReviewed(ids, orders);
    }
    return orders; 
    
}

function handleDropDown(e) {
    const selectTarget = e.target.value;
 
    switch(true) {
        case selectTarget.toLowerCase() === "empty":
            createProductTable(orders);
            break;
        case selectTarget.toLowerCase() === "reviewed":
            const pendingReviews = getReviewed();
            pendingReviews === null ? createProductTable(pendingReviews, false) : createProductTable(pendingReviews, true);
            break;
        case selectTarget.toLowerCase() === "not-reviewed":
            createProductTable(getNotReviewed());
            break;
        case selectTarget.toLowerCase() === "latest":
            const lastestList = sortByDateDescending(orders);
            createProductTable(lastestList);
            break;

        case selectTarget.toLowerCase() === "oldest":
            const oldestList = sortByDateAscending(orders)
            createProductTable(oldestList);
            break;
        
        case selectTarget.toLowerCase() === "ascending":
            const alpheticallyOrder = sortByNameAscending(orders);
            createProductTable(alpheticallyOrder);
            break;
        case selectTarget.toLowerCase() === "descending":
            const descendingOrder = sortByNameDescending(orders);
            createProductTable(descendingOrder);
            break;
        
    }
    
}


function addEventListenerToStar() {

    if (ratingDiv) {
        ratingDiv.addEventListener("click", handleStarClick);
    }
   
}


function handleStarClick(e) {

    if (e.target.tagName === 'A' || e.target.tagName === 'IMG') {
        e.preventDefault();

        
        if (clearBtn.style.display !== "block") {
            clearBtn.style.display = "block";
        }
  
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

        if (clearBtn.style.display === "block") {
            clearBtn.style.display = "none";
        }
     
    }
    ratingDiv.appendChild(stars);
}




function createRatingStars(numOfStarsToCreate, rating, totalNumberOfStars = 5, createEmptyStars=false) {
    const fragment = document.createDocumentFragment();
    
    for (let i = 1; i <= totalNumberOfStars; i++) {
        const aTag = document.createElement("a");
        const imgTag = document.createElement("img");

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








export default renderStar;