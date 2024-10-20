
import { addCardEventListeners, addImageRotationListeners } from "../handlers/itemCardInteractions.js";
import { handleSubscribeForm, setupEventListeners } from "../handlers/subscribeFormHandler.js";


import { closeAddToCartMsg as handleAddToCartCloseMsg, closeWishlistMessage as handleCloseWishlistMsg} from "../messages/messages.js";
import CarouselSlider from "../components/carouselSlider.js";
import dealCountDown from "../components/countdown.js";

// import {BakedItems, DrinksMenu, DairyProducts, 
//        FeaturedItems,  GrainProducts, IceCreams, 
//        NewItems, Sauces, Snacks} from "../../../data.js";

const boxes                        = document.querySelectorAll(".box");
const addToItemCloseIcon           = document.getElementById("addToItem-close-icon");
const subscribeForm                = document.getElementById("subscribe-form");
const wishListCloseIcon            = document.getElementById("wishlist-close-icon");

const drinkProudctsMenuSelector    = ".head .juice-and-drinks__container__cards__product_menu";
const featuredProductsMenuSelector = ".head .featured-products__container__cards__product_menu";
const newProductsMenuSelector      = ".head .new-products__container__cards__product_menu";

const drinkProductsCards           = document.querySelectorAll("#carousel2 .carousel-cards-wrapper .card-carousel");
const featuredProductCards         = document.querySelectorAll(".featured-products__container__cards .card");
const newProductCards              = document.querySelectorAll(".new-products__container__cards .card");

const iceCreamCardsMenuSelector    = ".head .organic-ice-creams__container__cards__product_menu";
const snackCardMenuSelector        = ".head .organic-snacks__container__cards__product_menu";
const bakedCardsMenuSelector       = ".head .organic-baked-goods__container__cards__product_menu";
const sauceCardMenuSelector        = ".head .organic-condiments-and-sauces__container__cards__product_menu";
const dairyCardMenuSelector        = ".head .organic-dairy-products__container__cards__product_menu";
const grainCardMenuSelector        = ".head .organic-grains-and-legumes__container__cards__product_menu";

const iceCreamCards                = document.querySelectorAll("#carousel3 .carousel-cards-wrapper .card-carousel");
const snacksCards                  = document.querySelectorAll("#carousel4 .carousel-cards-wrapper .card-carousel");
const bakedCards                   = document.querySelectorAll("#carousel5 .carousel-cards-wrapper .card-carousel");
const sauceCards                   = document.querySelectorAll("#carousel6 .carousel-cards-wrapper .card-carousel");
const dairyProductsCards           = document.querySelectorAll("#carousel7 .carousel-cards-wrapper .card-carousel");
const grainProductCards            = document.querySelectorAll("#carousel8 .carousel-cards-wrapper .card-carousel");

// This SECRET KEY will be stored her for now, later it will be stored in .env file and used to create JWT_TOKEN
const SECRET_KEY = "SessionKey$-`jrj]n~h~}XFRCY,`%kv*tX);AS+U_&jwr;FJy'iZHTq~o;%&r>x)h>[+\"<E=G+`%bAa\"y'N\"ct-])Ry\"^}au";


// setup eventlistListener
setupEventListeners();


// initialization of classes
const testimonialCarousel = new CarouselSlider();


// start the carousel
try {
    testimonialCarousel.setCardsContainer(); 
    testimonialCarousel.setPrevButton();
    testimonialCarousel.setNextButton();
    testimonialCarousel.setCardSelector();
    testimonialCarousel.init();
} catch (error) {
    console.warn(`The carousel for the testimonial wasn't found - ${error}`);
}


// carousel 2 for the juice
const carousel2 = new CarouselSlider();
carousel2.setCardsContainer('#carousel2 .carousel-cards-wrapper');
carousel2.setCardSelector('#carousel2 .carousel-cards-wrapper .card-carousel');
carousel2.setPrevButton('#carousel2 .prev-card');
carousel2.setNextButton('#carousel2 .next-card');

carousel2.init();


// carousel 3 for the juice
const carousel3 = new CarouselSlider();
carousel3.setCardsContainer('#carousel3 .carousel-cards-wrapper');
carousel3.setCardSelector('#carousel3 .carousel-cards-wrapper .card-carousel');
carousel3.setPrevButton('#carousel3 .prev-card');
carousel3.setNextButton('#carousel3 .next-card');

carousel3.init();


// carousel 4 for the juice
const carousel4 = new CarouselSlider();
carousel4.setCardsContainer('#carousel4 .carousel-cards-wrapper');
carousel4.setCardSelector('#carousel4 .carousel-cards-wrapper .card-carousel');
carousel4.setPrevButton('#carousel4 .prev-card');
carousel4.setNextButton('#carousel4 .next-card');

carousel4.init();


// carousel 4 for the juice
const carousel5 = new CarouselSlider();
carousel5.setCardsContainer('#carousel5 .carousel-cards-wrapper');
carousel5.setCardSelector('#carousel5 .carousel-cards-wrapper .card-carousel');
carousel5.setPrevButton('#carousel5 .prev-card');
carousel5.setNextButton('#carousel5 .next-card');

carousel5.init();


// carousel 6 for the juice
const carousel6 = new CarouselSlider();
carousel6.setCardsContainer('#carousel6 .carousel-cards-wrapper');
carousel6.setCardSelector('#carousel6 .carousel-cards-wrapper .card-carousel');
carousel6.setPrevButton('#carousel6 .prev-card');
carousel6.setNextButton('#carousel6 .next-card');

carousel6.init();

// carousel 7 for the juice
const carousel7 = new CarouselSlider();
carousel7.setCardsContainer('#carousel7 .carousel-cards-wrapper');
carousel7.setCardSelector('#carousel7 .carousel-cards-wrapper .card-carousel');
carousel7.setPrevButton('#carousel7 .prev-card');
carousel7.setNextButton('#carousel7 .next-card');

carousel7.init();

// carousel 8 for the juice
const carousel8 = new CarouselSlider();
carousel8.setCardsContainer('#carousel8 .carousel-cards-wrapper');
carousel8.setCardSelector('#carousel8 .carousel-cards-wrapper .card-carousel');
carousel8.setPrevButton('#carousel8 .prev-card');
carousel8.setNextButton('#carousel8 .next-card');

carousel8.init();



// icon addEventlistners
wishListCloseIcon.addEventListener("click", handleCloseWishlistMsg);
addToItemCloseIcon.addEventListener("click", handleAddToCartCloseMsg)


// subscribe form event iistener
subscribeForm.addEventListener("submit", async (event) => {await handleSubscribeForm(event, subscribeForm, SECRET_KEY);});
  
// runs the countdown
dealCountDown();


// boxes.forEach((box) => {
//     const imgContainer = box.querySelector(".img-box");
//     const images = imgContainer ? imgContainer.querySelectorAll("img") : [];
//     addImageRotationListeners(box, images);
// });


// drinkProductsCards.forEach((card) => {
//     addCardEventListeners(card, drinkProudctsMenuSelector, DrinksMenu)
// })

// featuredProductCards.forEach((card) => {
//     addCardEventListeners(card, featuredProductsMenuSelector, FeaturedItems);

// });

// iceCreamCards.forEach((card) => {
//     addCardEventListeners(card, iceCreamCardsMenuSelector, IceCreams)
// })


// snacksCards.forEach((card) => {
//     addCardEventListeners(card, snackCardMenuSelector, Snacks);
// })

// bakedCards.forEach((card) => {
//     addCardEventListeners(card, bakedCardsMenuSelector, BakedItems);
// });


// sauceCards.forEach((card) => {
//     addCardEventListeners(card, sauceCardMenuSelector, Sauces);
// })

// dairyProductsCards.forEach((card) => {
//     addCardEventListeners(card, dairyCardMenuSelector, DairyProducts)
// })


// grainProductCards.forEach((card) => {
//     addCardEventListeners(card, grainCardMenuSelector, GrainProducts)
// })



// newProductCards.forEach((card) => {
//     addCardEventListeners(card, newProductsMenuSelector, NewItems);
// })



