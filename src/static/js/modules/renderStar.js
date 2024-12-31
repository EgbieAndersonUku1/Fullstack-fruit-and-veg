/**
 * Star Rating System for E-commerce
 * ----------------------------------
 * 
 * This script handles star ratings for product reviews in an e-commerce application or anything that wants to display ratings.
 *
 * Required HTML Structure:
 * -------------------------
 * 
    <!-- Ratings Container -->
    <div class="some class name">
        <div class="header">
            <h3>Any name</h3>
        </div>

        <div class="product-ratings"> ---> The class `product-ratings` can be any name or even ID as long as correct selector name
                                           is passed to `StarRatings` class
            <a href="#" id="1" data-value="1">
                <img src="path/to/star-unfilled.svg" alt="star-unfilled" class="star-unfilled star-rating" data-value="1"> 
            </a>
            <a href="#" id="2" data-value="2">
                <img src="path/to/star-unfilled.svg" alt="star-unfilled" class="star-unfilled star-rating" data-value="2">
            </a>

            <a href="#" id="3" data-value="3">
                <img src="path/to/star-unfilled.svg" alt="star-unfilled" class="star-unfilled star-rating" data-value="3">
            </a>
            
            <!-- Repeat for as many stars as needed. The total number of stars should match the value set in 
                the `totalNumberOfStars` parameter of the `StarRating` class. If you include more than 5 stars, 
                make sure to set `this.totalNumberOfStars` accordingly in the `StarRating` class to ensure proper 
                rendering of rated and unfilled stars.
             -->

        </div>
    </div>


 * Star Image Requirements:
 * -------------------------
 * 1. A colored (filled) star image (e.g., `star-filled.svg`).
 * 2. An unfilled (empty) star image (e.g., `star-unfilled.svg`).
 * 
 * 
 * Both images should be placed in the same folder, e.g., `/static/img/icons/`, or any folder 
 * appropriate to your project structure.
 * 
 * 
 * Setup Instructions:
 * --------------------
 * 
 * 1. Include this script in your HTML file.
 * 2. Call the StarRating class with the target container and configuration options.
 * 
 * 
 * Example Usage:
 * ---------------
 * 
 * const ratingsContainer = document.querySelector('.product-ratings');
 * 
 * const starRating  = new StarRating(ratingsContainer, {
 *     numOfRatedStars: 5, // ratings
 *     filledStarsSrc: '/static/img/star-filled.svg',
 *     unfilledStarsSrc: '/static/img/star-unfilled.svg',
 *     isInteractive: true, // true - To enable interactivity meaning it can be clicked and changed dynamically in UI by clicking the stars

 * });
 * 
 * Allows for the stars to be rated when clicked

 * starRating.initialise()
 * 
 */


export class StarRating {

    /**
     * Creates a new instance of the StarRating system.
     *
     * @param {HTMLElement} ratingsContainer - The container element where the star rating will be displayed.
     * @param {Object} [options={}]           - Configuration options for the star rating system.
     * @param {number} [options.numOfRatedStars=5] - The number of rated stars to display (default is 5). Used in both interactive and non-interactive modes.
     * @param {number} [options.totalNumberOfStars] - The total number of unrated stars to be display
     * @param {string} options.filledStarsSrc - The path to the image for filled stars.
     * @param {string} options.unfilledStarsSrc - The path to the image for unfilled stars.
     * @param {boolean} [options.renderEmptyStars=false] - Whether to render unfilled (empty) stars (default is false).
     * @param {boolean} [options.isInteractive=false] - Whether the stars should be interactive for rating (default is false). 
     */
    constructor(ratingsContainer, options = {}) {
        this.ratingsContainer    = ratingsContainer;
        this.numOfRatedStars     = options.numOfRatedStars || 5;
        this.totalNumberOfStars  = options.totalNumberOfStars || 5;
        this.filledStarsSrc      = options.filledStarsSrc;
        this.unfilledStarsSrc    = options.unfilledStarsSrc;
        this.renderEmptyStars    = options.renderEmptyStars || false;
        this._isInitialized      = false;
        this.isInteractive       = options.isInteractive || false;

        this._validateElement(ratingsContainer, "The ratings container is not a valid HTML element");
    
        if (!this.filledStarsSrc) {
            throw new Error("filledStarsSrc path is required.");
        }

        if (!this.unfilledStarsSrc) {
            throw new Error("unfilledStarsSrc path is required.");
        };

        this._handleStarClick = this._handleStarClick.bind(this);
     
    }
    
    /**
     * Validates that a given element is a valid HTML element.
     *
     * @private
     * @param {HTMLElement} element - The element to validate.
     * @param {string} msg - The error message to throw if the element is invalid.
     * @throws {Error} If the provided element is not a valid HTML element.
     */
    _validateElement(element, msg) {
        if (!(element instanceof HTMLElement)) {
            // throw new Error(msg);
            console.warn(msg)
        }
    }

   /**
     * Initialises the star rating system. Sets up event listeners if interactive mode is enabled and updates the star display.
    */
    initialise() {

        this._isInitialized = true;

        console.log("Initialised....");

        if (this.isInteractive) {

            console.log("Starting interactive mode....");

            try {
                this.ratingsContainer.addEventListener("click", this._handleStarClick);
            } catch (error) {
                console.warn("Error - Could not activate the addEventListener ");
            }
            

        } else {
            this._updateStarDisplay(this.numOfRatedStars);
        }
      
    }

    /**
     * Handles the click event for interactive mode. Updates the rating based on the star clicked in UI.
     *
     * @private
     * @param {MouseEvent} e - The click event triggered by the user.
     */
    _handleStarClick(e) {
        e.preventDefault();

        if (e.target.tagName === 'A' || e.target.tagName === 'IMG') {

            const star = e.target.closest('a');

            if (star) {

                const RATED            = "star-filled";
                const numOfRatedStars  = parseInt(star.dataset.value, 10);
                const ZERO_STARS       = 0;

                if (numOfRatedStars === 1 && e.target.alt === RATED) {
                    this._updateStarDisplay(ZERO_STARS);
                } else {
                    this._updateStarDisplay(numOfRatedStars);
                }             
                
            }
        }
    }

    /**
     * Updates the display of stars in the container to reflect the current rating.
     *
     * @private
     * @param {number} numOfStars - The number of stars to display as filled.
     * @throws {Error} If the object has not been initialised.
     */
    _updateStarDisplay(numOfRatedStars) {

        if (!this._isInitialized) {
            console.error("To use the rating stars, you must first initialise the object.");
            return;
        }

        this._clearRatingContainer();

        let stars;
        try {
            if (!this.renderEmptyStars) {
                stars = this._createRatingStars({numOfRatedStarsToCreate: numOfRatedStars, rating: numOfRatedStars});
            } else {
                stars = this._createRatingStars({numOfRatedStarsToCreate: numOfRatedStars, rating: numOfRatedStars, createEmptyStars: true});
            }
            this.ratingsContainer.appendChild(stars);
        } catch (error) {
            throw new Error(error.message);
        }
    }

    /**
     * Creates the rating stars based on the provided configuration.
     *
     * @private
     * @param {Object} params - Parameters for creating the stars.
     * @param {number} params.numOfStarsToCreate - The number of stars to create as filled.
     * @param {number} params.rating - The rating to display.
     * @param {boolean} [params.createEmptyStars=false] - Whether to include unfilled stars in the display.
     * @returns {DocumentFragment} A document fragment containing the generated star elements.
     * @throws {Error} If numOfStarsToCreate or rating is not a number.
     */
    _createRatingStars({numOfRatedStarsToCreate, rating, createEmptyStars = false}) {

        const fragment = document.createDocumentFragment();
        console.log(numOfRatedStarsToCreate)

        if (
            typeof numOfRatedStarsToCreate !== "number" ||
            typeof rating !== "number" 
        ) {
            throw new Error(`One or more parameters are not a number -- numOfRatedStarsToCreate - <${typeof numOfRatedStarsToCreate}>, 
                            ratings - <${typeof rating}>`  );
        }

        for (let i = 1; i <= this.totalNumberOfStars; i++) {
            const aTag = this._createElement("a");
            const imgTag = this._createElement("img");

            aTag.dataset.value = i;
            imgTag.dataset.value = i;

            if (i <= numOfRatedStarsToCreate && !createEmptyStars) {
                imgTag.src = this.filledStarsSrc;
                imgTag.alt = "star-filled";
                imgTag.classList.add("star-filled", "star-rating");
            } else {
                imgTag.src = this.unfilledStarsSrc;
                imgTag.alt = "star-unfilled";
                imgTag.classList.add("star-unfilled", "star-rating");
            }

            aTag.appendChild(imgTag);
            fragment.appendChild(aTag);
        }
        return fragment;
    }

    /**
     * Creates a new DOM element of the specified type.
     *
     * @private
     * @param {string} tagName - The name of the tag to create.
     * @returns {HTMLElement} The created DOM element.
     */
    _createElement(tagName) {
        return document.createElement(tagName);
    }

    /**
     * Clears the star rating container by removing all child elements.
     *
     * @private
    */
    _clearRatingContainer() {
        this.ratingsContainer.innerHTML = ""
    };

    /**
     * Destroys the star rating system. Removes event listeners and clears the container.
     */
    destroy() {
        if (this.ratingsContainer) {
            this.ratingsContainer.removeEventListener("click", this._handleStarClick);
        }

        this._clearRatingContainer();

    }
}


