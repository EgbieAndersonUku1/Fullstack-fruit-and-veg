const subscribeFormDiv    = document.querySelector(".subscribe__form");
const subscribeInfo       = document.querySelector(".subscribe__information");
const h2Element           = subscribeInfo.querySelector("h2");
const pElement            = subscribeInfo.querySelector("p");
const subscribeContainer  = document.querySelector(".subscribe .container");


function removeSubscriptionForm() {
    if (!(subscribeFormDiv instanceof HTMLElement)) {
        throw new Error("The element is not an HTML element");
    }
    subscribeFormDiv.style.display = "none";
}


function displaySubscribedMessage() {

    if (!(subscribeInfo instanceof HTMLElement)) {
        throw new Error("The element is not an HTML element");
    }
    
    if (!(h2Element instanceof HTMLElement) || !(pElement instanceof HTMLElement)) {
        throw new Error("One or more of the elements is not an HTML element");
    }
    
    h2Element.textContent = "You're All Set!";
    pElement.textContent = "Thank you for subscribing! You've successfully joined our newsletter and received your 30% off. Stay tuned for the latest updates on events, sales, special offers, and promotions!";
}


function centerSubscribeText() {
    if (!(subscribeContainer instanceof HTMLElement) ) {
        throw new Error("The element is not an HTML element");
    }

    subscribeContainer.style.display             = "grid";
    subscribeContainer.style.gridTemplateColumns = 'repeat(1, 1fr)';
    subscribeContainer.style.justifyItems        = 'center';
    subscribeContainer.style.alignItems          = 'center';
    subscribeContainer.style.textAlign           = 'center';

}


export {
    centerSubscribeText,
    displaySubscribedMessage,
    removeSubscriptionForm
} 