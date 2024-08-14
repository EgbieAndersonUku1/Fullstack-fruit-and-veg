import { 
    centerSubscribeText, 
    displaySubscribedMessage, 
    removeSubscriptionForm }  from "../builders/subscribeElements.js";

import AlertUtils from "../utils/alerts.js";

import { JWT } from "../services/jwtToken.js";

    
import { getItemFromLocalStorage as getJWtToken,
    saveToLocalStorage      as setJWtToken
   } from "../utils/utils.js";


async function handleSubscribeForm(e, subscribeForm, secret_key) {
    e.preventDefault();
    
    const form         = new FormData(subscribeForm);
    const emailAddress = form.get("email");

    // Not built yet but a fetch method will be here that will subscribe to the backend
    // by passing in the email address
    
    // Example fetch call (commented out until implemented):
    // const response = await fetch('backend-endpoint', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'Authorization': `Bearer ${secret_key}`
    //     },
    //     body: JSON.stringify({ email: emailAddress })
    // });

  
    AlertUtils.showAlert({
        title: "Subscription Successful!",
        text: "Thank you for subscribing to our site. Stay tuned for updates!",
        icon: "success",
        confirmButtonText: "Great!!"

    })

    const jwt       = new JWT();
    const milliseconds = 1000;
    const payload   = {
        email: emailAddress,
        role: "subcribed",
        lat:  Math.floor(Date.now() / milliseconds),  // Current UNIX timestamp
        exp: 2145916800                               // Expires on January 1, 2038 (UNIX timestamp)

    }
    const JWT_TOKEN = await jwt.createJWTToken(payload, secret_key);
    
    if (JWT_TOKEN) {
        setJWtToken("subscribed", JWT_TOKEN);
        centerSubscribeText();
        removeSubscriptionForm();
        displaySubscribedMessage();
    }


}



function setupEventListeners() {
    document.addEventListener("DOMContentLoaded", () => {
        const token = getJWtToken("subscribed");
        if (token) {
            removeSubscriptionForm();
            displaySubscribedMessage();
            centerSubscribeText();
        }
    });

}



export  {
    handleSubscribeForm,
    setupEventListeners 
}