import fetchData from "../utils/fetch.js";
import AlertUtils from "../utils/alerts.js";
import { validateElement } from "../errors/customErrors.js";
import handleResponse from "./handleResponse.js";

const csrfTokenFieldElement         = document.querySelector("input[name='csrfmiddlewaretoken']");
const subscribeFormContainerElement = document.querySelector(".subscribe__form");


validateElement(csrfTokenFieldElement, "csrfTokenFieldElement - This is not a valid HTML element", true);


const CSRF_TOKEN = csrfTokenFieldElement.value;


async function handleSubscribeForm(e, subscribeForm) {
    e.preventDefault();
    
    const form         = new FormData(subscribeForm);
    const emailAddress = form.get("email");

    try {
        const response = await fetchData({
            url: "subscription/subscribe/",
            csrfToken: CSRF_TOKEN,
            body:{ subscription: {email: emailAddress} },
    
        });

        const success = await handleResponse(response);
        if (success) {
            createSubscriptionSuccessMessage();
        };
       

    } catch (error) {
        console.log(error);
        handleErrorResponse();
    }
   
}


function handleErrorResponse() {
    AlertUtils.showAlert({
        title: "Subscription Unsuccessful!",
        text: "Something went wrong, please try again later",
        icon: "error",
        confirmButtonText: "Sorry!!"

    })
}


function clearSubscriptionContainer() {
    subscribeFormContainerElement.innerHTML = "";
}


function createParagraph(textContent) {
    const pElement = document.createElement("p");
    pElement.textContent = textContent;
    return pElement;
}


function createSubscriptionSuccessMessage() {
    clearSubscriptionContainer();

    const welcomeMessage = "We're thrilled to have you with us! By subscribing to our newsletter, you'll be the first to know about exclusive events, amazing sales, and special promotions tailored just for you.";
    const offerMessage = "Plus, enjoy an instant 30% off your next purchase as a warm welcome gift. Don't miss out on the latest updates and offers—subscribe today!";
    const thankYouMessage = "Thank you for being a valued member of our community";

    const messages = [welcomeMessage, offerMessage, thankYouMessage];

    messages.forEach(message => {
        subscribeFormContainerElement.appendChild(createParagraph(message));
    });
}



export  {
    handleSubscribeForm
  
}