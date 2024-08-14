import preventNumberInputTyping from "../utils/numberInputRestrictor.js";


const quickViewContainer  = document.querySelector("#quick-view .container");
const quickViewDiv        = document.querySelector("#quick-view");





function buildQuickView(item, id=null, maxQuantity=400) {
    if (!item) {
        throw new Error("Can't find the item");
    }
    
    const imageDiv         = buildItemImageDiv(item);
    const itemBodyInfoDiv  = buildItemInfo(item, id, maxQuantity);
    const closeIcon        = buildCloseIcon();
 
    quickViewContainer.innerHTML = "";
    quickViewContainer.appendChild(closeIcon);
    quickViewContainer.appendChild(imageDiv);
    quickViewContainer.appendChild(itemBodyInfoDiv);
   
}


function buildItemImageDiv(item) {
    if (!item || !item.images.detail) {
        throw new Error("The item or the item.detail couldn't be found!!");
    }

    const mainDiv        = document.createElement("div");
    mainDiv.className    = "quick-view__img";

    const imagesFragment = createImageElements(item.images.detail);
    mainDiv.appendChild(imagesFragment);
    return mainDiv;
}


function createImageElements(images) {

    const fragment       = document.createDocumentFragment();
    const mainImgDiv     = document.createElement("div");
    const sideImgDiv     = document.createElement("div");

    mainImgDiv.className = "quick-view__main-img";
    sideImgDiv.className = "quick-view__side-img";

    for (let image of images) {
        const img   =  document.createElement("img");
        img.src     = image.imgSrc;
        img.alt     = image.alt;
        img.loading = "lazy";

        if (image.main) {
            img.className = "quick-view__main-pic";
            mainImgDiv.appendChild(img);
        } else {
            img.className = "side-img";
            sideImgDiv.appendChild(img);
        }
    }

    fragment.appendChild(mainImgDiv);
    fragment.appendChild(sideImgDiv);
    return fragment;
}


function buildItemInfo(item, id, maxQuantity) {

    const mainDiv        = document.createElement("div");
    mainDiv.className    = "quick-view__image-info";

    const titleDiv       = buildItemHeader(item);
    const colorDiv       = buildItemChoiceDiv(item.color, "Color");
    const sizeDiv        = buildItemChoiceDiv(item.sizes, "Sizes");
    const dimensionsDiv  = buildItemChoiceDiv(item.dimensions, "Dimensions");
    const inStockDiv     = buildIsItemInStockDiv(item);
    const stockRemaining = buildStockRemainingDiv(item);
    const addToCartDiv   = buildAddToCartDiv(item, id, maxQuantity);
    const buildCheckOutDiv = buildCheckOut();

    mainDiv.appendChild(titleDiv);
    mainDiv.appendChild(colorDiv);
    mainDiv.appendChild(sizeDiv);
    mainDiv.appendChild(dimensionsDiv);
    mainDiv.appendChild(inStockDiv);
    mainDiv.appendChild(stockRemaining);
    mainDiv.appendChild(addToCartDiv);
    mainDiv.appendChild(buildCheckOutDiv);
    return mainDiv;
    
}



function buildItemHeader(item) {

    if (!item) {
        throw new Error("The item couldn't be found!!");
    }

    const h2                     = document.createElement("h2");
    const pDescriptionTag        = document.createElement("p");
    const pItemPriceTag          = document.createElement("p");
    const hr                     = document.createElement("hr");
    const pBrandTag              = document.createElement("p");
    const pReferenceTag          = document.createElement("p");
    const mainDiv                = document.createElement("div");

    h2.className                 = "quick-view__image-info__header";
    h2.textContent               = item.name ? item.name.toUpperCase() : "N/A";

    pDescriptionTag.className    = "quick-view__image-info__description";
    pDescriptionTag.textContent  = item.description ? item.description : "No description available.";

    pItemPriceTag.className      = "item-price";
    pItemPriceTag.textContent    = item.price ? `£${item.price}` : "Price not available";


    hr.style.margin              = 0;

    pBrandTag.className          = "brand";
    const brandSpan              = document.createElement("span");
    brandSpan.className          = "light-bold";
    brandSpan.textContent        = "Brand: ";
    pBrandTag.appendChild(brandSpan);
    pBrandTag.appendChild(document.createTextNode(item.brand ? item.brand : "Unknown"));

    pReferenceTag.className      = "reference";
    const referenceSpan          = document.createElement("span");
    referenceSpan.className      = "bold";
    referenceSpan.textContent    = "Reference: ";

    pReferenceTag.appendChild(referenceSpan);
    pReferenceTag.appendChild(document.createTextNode(item.referenceID ? item.referenceID : "N/A"));
    
    mainDiv.appendChild(h2);
    mainDiv.appendChild(pDescriptionTag);
    mainDiv.appendChild(pItemPriceTag);
    mainDiv.appendChild(pBrandTag);
    mainDiv.appendChild(pReferenceTag);
    mainDiv.appendChild(hr);

    return mainDiv;
}


function buildItemChoiceDiv(attributesArray, title) {

    if (!attributesArray || !Array.isArray(attributesArray)) {
        throw new Error("Something went wrong, check the attributesArray");
    }

    if (!title) {
        throw new Error("The title attribute can't be empty!!!");
    }

    const mainDiv      = document.createElement("div");
    mainDiv.className  = "item-choice";

    const titleDiv     = document.createElement("div");
    titleDiv.className = "item-title";

    const pTag         = document.createElement("p");
    const pSpan        = document.createElement("span");
    pSpan.className    = "item-size-title";
    pSpan.textContent  = "Color";

    pTag.classList.add("light-bold", title);
    pTag.appendChild(document.createTextNode(`${title.toUpperCase()} : `));

    titleDiv.appendChild(pTag);

    // the buttons div
    const buttonDiv      = document.createElement("div");
    buttonDiv.className  = "quick-view__choice";

    const buttonsFragment = createButtons(attributesArray, title);
    buttonDiv.appendChild(buttonsFragment);

    mainDiv.appendChild(titleDiv);
    mainDiv.appendChild(buttonDiv);

    return mainDiv;
}


function createButtons(attributesArray, title) {
    const fragment = document.createDocumentFragment();

    for (let attribute of attributesArray) {
        const button = document.createElement("button");
        button.classList.add("link-btn", "text-upper", "quick-view__button-display");

        button.dataset.key = title;
        button.dataset.value = attribute;
        button.textContent = attribute;

        button.addEventListener("click", handleButtonClick);
        fragment.appendChild(button);
    }

    return fragment;
}



function buildIsItemInStockDiv(item) {
    return buildStockHelper(item);
}


function buildStockRemainingDiv(item) {
    return buildStockHelper(item, false);
}


function buildStockHelper(item, showStockStatus = true) {
    const mainDiv         = document.createElement("div"); 
    const pTitleTag       = document.createElement("p"); 
   
    const pStockTag       = document.createElement("p"); 
    pStockTag.className   = "item-size-title";

    pTitleTag.textContent = showStockStatus ? "STOCK" : "STOCK REMAINING";
    pStockTag.textContent = showStockStatus ? (item.remaining > 0 ? "In stock" : "Not in stock") : item.remaining;

    pTitleTag.className   = "light-bold";
    const quantityDiv     = document.createElement("div");
    quantityDiv.className = "quick-view__item_quantity";

    quantityDiv.appendChild(pStockTag);

    mainDiv.appendChild(pTitleTag);
    mainDiv.appendChild(quantityDiv);
    
    return mainDiv;
}


function buildCloseIcon(){

    const img     = document.createElement("img");
    const mainDiv = document.createElement("div");
    mainDiv.id    = "close-icon";

    img.src        = "static/img/icons/window-close.svg";  // shows

    img.alt        = "Window close icon";
    img.className  = "close-icon";

    img.addEventListener("click", handleCloseIconClick);

    mainDiv.appendChild(img);
    return mainDiv;
}


function buildCheckOut() {

    const mainDiv             = document.createElement("div");
    const continueShoppingBtn = document.createElement("button");
    const checkoutBtn         = document.createElement("button");

    mainDiv.classList.add("checkout", "flex-row");

    continueShoppingBtn.classList.add("button-lg", "padding-sm", "text-upper", "continue-shopping-btn");
    checkoutBtn.classList.add("button-lg", "padding-sm", "text-upper", "proceed-to-checkout-btn");

    continueShoppingBtn.textContent = "Continue shopping";
    checkoutBtn.textContent  = "Checkout";

    mainDiv.appendChild(continueShoppingBtn);
    mainDiv.appendChild(checkoutBtn);
    return mainDiv

}


function handleButtonClick(e) {

    // Update the title to reflect the button being clicked e.g. Color, size, dimension, etc
    const key    = e.target.dataset.key;
    const value  = e.target.dataset.value;
    const pTag   = document.querySelector(`.${key}`);

    pTag.textContent = `${key.toUpperCase()}: ${value.toUpperCase()}`;

    removeExistingActiveClass(e);
    e.target.classList.add("active");
   
}


function handleCloseIconClick() {
    quickViewDiv.style.display = "none";
}


function removeExistingActiveClass(e) {
   
   const parentDiv = e.target.parentElement;

   if (parentDiv) {
        const buttons = parentDiv.querySelectorAll("button");
        if (buttons) {
            buttons.forEach((button) => {
                if (button.classList.contains("active")) {
                    button.classList.remove("active");
                }
            })
        }
   }
  
}


function closeItemQuickView() {
    quickViewDiv.style.display = "none";
}


function buildAddToCartDiv(item, id, maxQuantity) {

    if (!item || typeof item.id === 'undefined' || typeof item.name === 'undefined' || typeof item.price === 'undefined') {
        console.error('Invalid item provided');
        return null;
    }

    const mainDiv          = document.createElement("div");
    const inputElement     = createQuantityInputField(item, id, maxQuantity);
    const inputFieldHidden = createHiddenInputField(item);
    const buttonElement    = document.createElement("button");
    const clearCartButton  = document.createElement("button");

    let itemInCart;

    mainDiv.classList.add("quantity", "add-to-cart");

    if (id && item.quantity) {
        clearCartButton.classList.add("button-md", "clear-cart-btn");
        clearCartButton.textContent = `Clear Cart (${item.quantity > 1 ? `${item.quantity} items` : `${item.quantity} item`})`;
        itemInCart = true;
    }

    buttonElement.className = "button-lg add-to-cart-btn";
    buttonElement.textContent = "Add to cart";

    mainDiv.appendChild(inputFieldHidden);
    mainDiv.appendChild(inputElement);
    mainDiv.appendChild(buttonElement);

    if (itemInCart) {
        mainDiv.appendChild(clearCartButton);
    }

    return mainDiv;
}

function createHiddenInputField(item) {

    const inputFieldHidden          = document.createElement("input");
    inputFieldHidden.type           = "hidden";
    inputFieldHidden.id             = "hidden";
    inputFieldHidden.dataset.id     = item.id;
    inputFieldHidden.dataset.title  = item.name;
    inputFieldHidden.dataset.price  = item.price;
    inputFieldHidden.dataset.stock  = item.remaining;
    return inputFieldHidden;
}

function createQuantityInputField(item, id, maxQuantity, min="1", step="1") {

    const inputElement = document.createElement("input");
    inputElement.name  = "quantity";
    inputElement.type  = "number";
    inputElement.id    = "quantity";
    inputElement.min   = min;
    inputElement.max   = maxQuantity.toString();
    inputElement.step  = step;

    if (id === null) {
        inputElement.value = min;
    } else if (parseInt(item.id, 10) === parseInt(id, 10)) {
        inputElement.value = item.quantity || "1";
    }

    inputElement.addEventListener("keydown", preventNumberInputTyping);
    return inputElement;
}


export {
    buildQuickView,
    closeItemQuickView
}