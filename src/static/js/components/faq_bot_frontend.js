import { validateElement } from "../errors/customErrors.js";
import { MessageHistory } from "./faq_bot_utils.js";
import fetchData from "../utils/fetch.js";


let CSRF_TOKEN;
const sendForm               = document.getElementById("send-chat-form");
const chatBodyContainer      = document.getElementById("body-chat");
const customerSupportImage   = document.getElementById("customer-support-img");
const faqSection             = document.getElementById("faq-help");
const closeLink              = document.getElementById("close-faq");


const loader = createLoader();
const messages = new MessageHistory();

validateElement(sendForm, "The send form couldn't be located", true);
validateElement(chatBodyContainer, "The chat body couldn't be located", true);
validateElement(customerSupportImage, "The customer service image couldn't be found", true);
validateElement(faqSection, "The faq section  element couldn't be found", true);
validateElement(closeLink, "The close link element couldn't be found ", true);




sendForm.addEventListener("submit", handleSendForm);
customerSupportImage.addEventListener("click", handleCustomerSupportClick);
closeLink.addEventListener("click", handleCloseLink);



/**
 * Retrieves the CSRF token value from the page if it's not already set.
 * 
 * The function checks if the CSRF token is already stored in the global `CSRF_TOKEN` variable.
 * If the token is not set, it fetches the value from an input field with the name `csrfmiddlewaretoken`
 * and stores it in the global variable. It then returns the CSRF token value.
 * 
 * @returns {string} The CSRF token value.
 */
function getCsrfToken() {
    if (!CSRF_TOKEN) {
        CSRF_TOKEN = document.querySelector("input[name='csrfmiddlewaretoken']").value; 
    }
    return CSRF_TOKEN
}


/**
 * Handles the form submission for sending a question to the FAQ bot.
 * This extracts the user's input text, and sends the question to the backend via fetch. 
 * It then processes the response from the bot and updates the chat with the appropriate messages.
 * 
 * If the response is successful, the bot's reply is displayed. Otherwise, 
 * an error message is shown. 
 * 
 * @param {Event} e - The submit event triggered by the user submitting the form.
 */
async function handleSendForm(e) {

    e.preventDefault();
    const question = getSendInputText();

    if (question) {

        addMessageToChat({role: "user", text: question});

        const resp  = await sendMessage(question, messages.getMessages());
        const query = resp.resp;
    
        if (query) {
           
            addMessageToChat({role: "model", text: query});
            removeLoader();

            messages.addMessage({role:"user", message:question});
            messages.addMessage({role:"model", message:query});

        } else {
            addErrorMessage();
            removeLoader();
        }
    }

}


/**
 * Retrieves the text input from the user and clears the input field afterwards to prepare for the next input. 
 * @returns {string} The current value of the input field, representing the user's question or message.
 */
function getSendInputText() {
    const sendInputElement     = document.getElementById("send-input-field");
    const text                 = sendInputElement.value;
    sendInputElement.value     = "";
    return text;
};



/**
 * Adds a new message to the chat body and displays the loader.
 * This function creates a message container, appends it to the chat body, 
 * and ensures that the chat scrolls to the latest message.
 *
 * @param {Object} params - The parameters for the message.
 * @param {string} params.role - The role of the sender ("user" or "model").
 * @param {string} params.text - The text of the message.
 */
function addMessageToChat({role, text}) {
   
    const messageContainer = createMessageContainer({role:role, message:text});
 
    if (!messageContainer) {
        throw new Error("Expected a message div container but received an empty value");
    };

    chatBodyContainer.appendChild(messageContainer);

    showLoader();
    scrollToBottom();

};





/**
 * Displays a loader in the chat body while waiting for a response.
 */
function showLoader() {
    chatBodyContainer.appendChild(loader);
}

/**
 * Automatically scrolls to the bottom of the chat, so that any new chat is displayed
 */
function scrollToBottom() {
    chatBodyContainer.scrollTop = chatBodyContainer.scrollHeight;
};


/**
 * Removes the loader from the chat body 
 */
function removeLoader() {
    loader.remove();
}





/**
 * Sends a question to the server and retrieves the response.
 * This function sends the user's question along with the message history
 * to the server via an API call, and waits for the server's response. The response 
 * is then returned to the calling function to be processed.
 *
 * @param {string} text - The question or message to be sent to the server.
 * @param {Array} messageHistory - The history of previous messages, used to provide context to the server.
 * @returns {Object|null} The response data from the server if successful, or null if the request fails.
 * @throws {Error} If the CSRF token is missing or invalid.
 */
async function sendMessage(text, messageHistory) {

    const csrfToken = getCsrfToken();
    if (!csrfToken) {
        addErrorMessage("CSRF Token missing. Please refresh the page and try again.");
        return;
    };

    const url  = "/faq/ask_question/";
    const body = {
                question: text,
                messageHistory: messageHistory
    };

    try {
        const response = await fetchData({url:url, csrfToken:CSRF_TOKEN, body:body });
        return response.SUCCESS ? response.DATA : null;
      
    } catch (error) {
        console.error('Something went wrong:', error);

        
    }
}




/**
 * Displays an error message in the chat container.
 * *
 * @param {string} [message="Couldn't send message please try again later"] - The error message to be displayed. Defaults to a predefined error message if not provided.
 */
function addErrorMessage(message="Couldn't send message please try again later") {
    
    const pTag               = document.createElement("p");
    pTag.style.color         = "red";
    pTag.style.textAlign     = "center";
    pTag.style.textTransform = "none";
    pTag.textContent         = message;
    
    chatBodyContainer.appendChild(pTag);
};




/**
 * Creates a message container with the appropriate role and message content.
 * This function generates an HTML `div` element that contains a label and 
 * a paragraph element. The label indicates whether the message is from the 
 * user or the FAQ bot. The paragraph contains the message text.
 * 
 * @param {Object} params - The parameters for creating the message container.
 * @param {string} params.role - The role of the message sender, either "user" or "model" (FAQ bot).
 * @param {string} params.message - The message content to be displayed.
 * 
 * @throws {Error} If the `message` is empty or not provided.
 * 
 * @returns {HTMLElement} The `div` container element containing the formatted message.
 */
function createMessageContainer({ role, message }) {

    const messageDivContainer = document.createElement("div");
    const smallTag            = document.createElement("small");
    const pTag                = document.createElement("p");

    smallTag.className = "chat-label";
    
    smallTag.textContent = role.toLowerCase() === "user" ? "User" : "FAQ Bot";
    messageDivContainer.className = role === "user" ? "user" : "system";

    if (!message) {
        throw new Error("The message cannot be empty");
    }

    messageDivContainer.appendChild(smallTag);
    pTag.textContent = message;
    messageDivContainer.appendChild(pTag);
    
    return messageDivContainer;
}


/**
 * Creates a loader element with a specified class name.
 * @param {string} [className="loader"] - The class name to be assigned to the loader element.
 * 
 * @throws {Error} If the `className` parameter is empty.
 * 
 * @returns {HTMLElement} The `div` element representing the loader with the specified class name.
 */
function createLoader(className="loader") {
    const loader = document.createElement("div");

    if (!className) {
        throw new Error("The classname cannot be empty")
    }
    loader.className = className;
    return loader;
}


function handleCustomerSupportClick(e) {
    e.preventDefault();
    showFaqSupport();
    
};


function showFaqSupport() {
    customerSupportImage.style.display = "none";
    faqSection.style.display           = "block";
};


function handleCloseLink(e) {

    if (e) {

        e.preventDefault();
        customerSupportImage.style.display = "block";
        faqSection.style.display           = "none";
    
    };
   
};