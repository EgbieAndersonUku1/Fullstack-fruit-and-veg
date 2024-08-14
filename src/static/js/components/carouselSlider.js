/**
 * The CarouselSlider component is designed to create a reusable and interactive carousel for projects requiring a carousel element.
 *
 * Note: This component does not include CSS styles. Users need to define their own styles to control how the carousel
 * is displayed within the viewport. This includes deciding whether the viewport should show one card (taking up the entire viewport)
 * or multiple cards. The CSS must be configured to manage the display of cards in the viewport, such as setting widths and overflow properties.
 *
 * Key Updates:
 * - The component now takes into account the number of visible cards within the viewport, not just a single card.
 *   It calculates how many cards can fit within the container and displays that many cards, including partial cards.
 * - Added debouncing to the navigation button handlers to prevent excessive triggering from rapid clicks, improving performance and user experience.
 *
 * HTML Structure:
 * Ensure the following HTML structure for the component to function correctly:
 * 
 * <div id="carousel">
 *     <div class="carousel-cards-wrapper">
 *         <div class="card-carousel">Card 1</div>
 *         <div class="card-carousel">Card 2</div>
 *         <div class="card-carousel">Card 3</div>
 *         <!-- Additional cards as needed -->
 *     </div>
 *     <button class="carousel-button left-button prev-card">&#10094;</button>
 *     <button class="carousel-button right-button next-card">&#10095;</button>
 * </div>
 * 
 * Explanation:
 * 1. The outermost <div> with ID "carousel" wraps the entire carousel structure. This ID is used to uniquely identify
 *    each carousel on the page and can be customized as needed.
 * 
 * 2. Inside this container, the <div> with the class "carousel-cards-wrapper" holds multiple <div> elements with the class "card-carousel".
 *    Each "card-carousel" element represents an individual slide. The "carousel-cards-wrapper" is the container manipulated
 *    to show different cards in the view.
 * 
 * 3. Navigation buttons are placed outside the "carousel-cards-wrapper" <div> but within the "carousel" container.
 *    These buttons have classes "prev-card" and "next-card" and are used to navigate through the cards.
 *    They are referenced in the JavaScript code using the outer container's ID combined with the button classes (e.g., `#carousel .prev-card`).
 * 
 * Usage:
 * 
 * The CarouselSlider class handles the initialization and functionality of the carousel.
 * It provides methods to set the main carousel card container, previous and next buttons, and the carousel cards.
 * Call the 'init' method after setting the selectors to initialize the event listeners.
 * 
 * Example Usage with Default Selectors:
 * If your HTML structure uses the default parameter names (.carousel-cards-wrapper, .prev-card, .next-card, .card-carousel),
 * initialize as follows:
 * 
 * const carousel = new CarouselSlider();
 * carousel.setCardsContainer();
 * carousel.setPrevButton();
 * carousel.setNextButton();
 * carousel.setCardSelector();
 * carousel.init();
 * 
 * If your HTML structure has different class names or IDs, specify them using set methods before calling 'init':
 * 
 * const carousel = new CarouselSlider();
 * carousel.setCardsContainer('#custom-carousel .custom-carousel-cards-wrapper');
 * carousel.setPrevButton('#custom-carousel .custom-prev-button');
 * carousel.setNextButton('#custom-carousel .custom-next-button');
 * carousel.setCardSelector('#custom-carousel .custom-card-carousel');
 * carousel.init();
 * 
 * Example with Multiple Carousels on the Same Page:
 * If you have multiple carousels on the same page, use unique IDs or direct paths for each carousel.
 * 
 * HTML:
 * 
 * <div id="carousel1">
 *     <div class="carousel-cards-wrapper">
 *         <div class="card-carousel">Card 1</div>
 *         <div class="card-carousel">Card 2</div>
 *         <!-- Additional cards as needed -->
 *     </div>
 *     <button class="carousel-button left-button prev-card">&#10094;</button>
 *     <button class="carousel-button right-button next-card">&#10095;</button>
 * </div>
 * 
 * <div id="carousel2">
 *     <div class="carousel-cards-wrapper">
 *         <div class="card-carousel">Card A</div>
 *         <div class="card-carousel">Card B</div>
 *         <!-- Additional cards as needed -->
 *     </div>
 *     <button class="carousel-button left-button prev-card">&#10094;</button>
 *     <button class="carousel-button right-button next-card">&#10095;</button>
 * </div>
 * 
 * JavaScript:
 * 
 * const carousel1 = new CarouselSlider();
 * carousel1.setCardsContainer('#carousel1 .carousel-cards-wrapper');
 * carousel1.setPrevButton('#carousel1 .prev-card');
 * carousel1.setNextButton('#carousel1 .next-card');
 * carousel1.setCardSelector('#carousel1 .card-carousel');
 * carousel1.init();
 * 
 * const carousel2 = new CarouselSlider();
 * carousel2.setCardsContainer('#carousel2 .carousel-cards-wrapper');
 * carousel2.setPrevButton('#carousel2 .prev-card');
 * carousel2.setNextButton('#carousel2 .next-card');
 * carousel2.setCardSelector('#carousel2 .card-carousel');
 * carousel2.init();
 */


class CarouselSlider {
    constructor() {
        this._currentIndex         = 0; 
        this._cardsContainer       = null; 
        this._prevCardButton       = null; 
        this._nextCardButton       = null; 
        this._carouselCardElements = null; 
        this._visibleCardsCount    = 1; 

        // Initialize debounce delay (200ms)
        this._debounceDelay = 200;
        
        // Create debounced versions of navigation handlers
        this._debouncedPrev = this._debounce(this._handlePrevCard.bind(this), this._debounceDelay);
        this._debouncedNext = this._debounce(this._handleNextCard.bind(this), this._debounceDelay);
    }

    /**
     * Sets the container element that holds the carousel cards.
     * @param {string} selector - The CSS selector for the carousel cards container.
     */
    setCardsContainer(selector = '#carousel .carousel-cards-wrapper') {
        this._cardsContainer = document.querySelector(selector);
        this._isElementValid({ element: this._cardsContainer, errorMsg: `Cards container "${selector}" not found!` });
    }

    /**
     * Sets the card elements for the carousel and calculates the number of visible cards.
     * @param {string} selector - The CSS selector for the individual carousel cards.
     */
    setCardSelector(selector = '#carousel .card-carousel') {
        
        this._carouselCardElements = document.querySelectorAll(selector);

        if (this._carouselCardElements.length === 0) {
            throw new Error(`No cards found with selector "${selector}"!`);
        }

        const containerWidth     = this._cardsContainer.offsetWidth;
        const cardWidth          = this._carouselCardElements[0].offsetWidth;
        const numOfCarouselCards = containerWidth / cardWidth;
        this._visibleCardsCount  = Math.floor(numOfCarouselCards);
    }

    /**
     * Sets the previous button element that will trigger navigation to the previous card.
     * @param {string} selector - The CSS selector for the previous card button.
     */
    setPrevButton(selector = '#carousel .prev-card') {
        this._prevCardButton = document.querySelector(selector);
        this._isElementValid({ element: this._prevCardButton, errorMsg: `Previous button "${selector}" not found!` });
    }

    /**
     * Sets the next button element that will trigger navigation to the next card.
     * @param {string} selector - The CSS selector for the next card button.
     */
    setNextButton(selector = '#carousel .next-card') {
        this._nextCardButton = document.querySelector(selector);
        this._isElementValid({ element: this._nextCardButton, errorMsg: `Next button "${selector}" not found!` });
    }

    /**
     * Checks if an element is valid (exists in the DOM) and throws an error if not.
     * @param {Object} param - Object containing the element and error message.
     * @param {HTMLElement} param.element - The DOM element to check.
     * @param {string} param.errorMsg - The error message to throw if the element is not valid.
     */
    _isElementValid({ element, errorMsg }) {
        if (!(element instanceof HTMLElement)) {
            throw new Error(errorMsg);
        }
    }

    /**
     * Updates the carousel's transform property to display the current set of visible cards.
     */
    _updateCarousel() {
        const cardWidth = this._carouselCardElements[0].offsetWidth;
        const newTransformValue = -this._currentIndex * cardWidth;
        this._cardsContainer.style.transform = `translateX(${newTransformValue}px)`;
    }

    /**
     * Handles navigation to the previous card in the carousel.
     * If at the first card, it loops to the last set of visible cards.
     */
    _handlePrevCard() {
        if (this._currentIndex > 0) {
            this._currentIndex--;
        } else {
            // Move to the last set of visible cards if we're at the start
            this._currentIndex = Math.max(0, this._carouselCardElements.length - this._visibleCardsCount);
        }
        this._updateCarousel();
    }

    /**
     * Handles navigation to the next card in the carousel.
     * If at the last card, it loops back to the first card.
     */
    _handleNextCard() {
        if (this._currentIndex < (this._carouselCardElements.length - this._visibleCardsCount)) {
            this._currentIndex++;
        } else {
            // Loop back to the first card
            this._currentIndex = 0;
        }
        this._updateCarousel();
    }

    /**
     * Creates a debounced version of a function to delay its execution.
     * @param {Function} func - The function to debounce.
     * @param {number} delay - The delay in milliseconds for the debounce.
     * @returns {Function} - The debounced function.
     */
    _debounce(func, delay) {
        let timer;
        return function() {
            clearTimeout(timer);
            timer = setTimeout(() => {
                func.apply(this, arguments);
            }, delay);
        };
    }

    /**
     * Initializes the carousel by attaching event listeners to the navigation buttons.
     * Throws an error if any required element is not set.
     */
    init() {
        if (!this._cardsContainer || !this._prevCardButton || !this._nextCardButton || !this._carouselCardElements) {
            throw new Error("CarouselSlider is not fully initialized. Ensure all selectors are set.");
        }

        // Attach debounced event listeners to buttons
        this._prevCardButton.addEventListener("click", this._debouncedPrev);
        this._nextCardButton.addEventListener("click", this._debouncedNext);
    }
}

export default CarouselSlider;
