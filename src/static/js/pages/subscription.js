import { validateElement } from "../errors/customErrors.js";
import fetchData from "../utils/fetch.js";
import handleResponse from "../handlers/handleResponse.js";
import { minimumCharactersToUse } from "../components/characterCounter.js";
import showSpinner from "../utils/spinner.js";

const headers                  = document.querySelectorAll("#subscription-tabs .tab > h4");
const tabSections              = document.querySelectorAll(".tab-section");
const subscriptionTabContainer = document.getElementById("subscription-tabs");
const subscriptionOverview     = document.getElementById("subscription-overview");
const subscriptionHistory      = document.getElementById("subscription-history");
const notificationAlert        = document.getElementById("notification-alerts");
const frequencyForm            = document.getElementById("frequency-update-form");
const csrfTokenField           = document.querySelector("input[name='csrfTokenMiddleware']");
const feedBackFormContainer    = document.querySelector(".feedback-form");
const feedBackFormTextArea     = document.getElementById("id_reason_for_unsubscribing");
const feedbackForm             = document.getElementById("newsletter-form");
const unsubscribeBtn           = document.getElementById("unsubscribe-btn");
const cancelBtn                = document.querySelector(".cancel-btn");
const spinner                  = document.querySelector(".spinner");


// check if the global elements are valid before proceeding
[subscriptionTabContainer, 
    subscriptionOverview, 
    subscriptionHistory, 
    notificationAlert, 
    frequencyForm, 
    feedBackFormContainer,
    cancelBtn,
    feedbackForm,
    csrfTokenField].forEach((element) => {
    validateElement(element, "The html is not a valid element");
});


const CSRF_TOKEN   = csrfTokenField?.value;

document.addEventListener("DOMContentLoaded", setUp);
document.addEventListener(feedbackForm, handleFeedbackForm);
unsubscribeBtn?.addEventListener("click", handleUnsubscribeBtnClick);
cancelBtn?.addEventListener("click", handleCancelButtonClick);

subscriptionTabContainer?.addEventListener("click", handleSubscriptionTabs);
frequencyForm?.addEventListener("submit", handleFormSubmit);



function setUp() {

    hideAllTabSection();
    removeActiveFromTabs();

    showTabSection(subscriptionOverview);
 
    const firstTab = headers[0]
    addActiveStatusToHeaderTab(firstTab);

};


function hideAllTabSection() {
    removeActiveFromTabs();  
    tabSections.forEach((tabSection) => hideTabSection(tabSection));
};


function showTabSection(tab) {   
    tab.classList.remove("d-none");
};


function hideTabSection(tab) {
    tab.classList.add("d-none");
};


function addActiveStatusToHeaderTab(header) {
    if (header && !header.classList.contains("active")) {
        header.classList.add("active", "highlight");
    };
};


function removeActiveFromTabs() {
   
    if (headers) {
        headers.forEach((header) => {
    
           if ( header.classList.contains("active")) {
                header.classList.remove("active", "highlight");
           };
        });
    };
};



function handleSubscriptionTabs(e) {
    e.preventDefault();

    const tabs = {
        OVERVIEW: "subscription overview",
        HISTORY: "subscription history",
        NOTIFICATION: "notifications"
    };

    if (e.target.nodeName === "H4") {
        const innerText = e.target.innerText.toLowerCase();
        removeActiveFromTabs();

        switch (innerText) {
            case tabs.OVERVIEW:
                toggleTabVisibility(subscriptionOverview, [subscriptionHistory, notificationAlert], headers[0]);
                break;
            case tabs.HISTORY:
                toggleTabVisibility(subscriptionHistory, [subscriptionOverview, notificationAlert], headers[1]);
                break;
            case tabs.NOTIFICATION:
                toggleTabVisibility(notificationAlert, [subscriptionOverview, subscriptionHistory], headers[2]);
                break;
        }
    }
};



function toggleTabVisibility(showTab, hideTabs, header) {
    hideTabs.forEach(hideTabSection);
    showTabSection(showTab);
    addActiveStatusToHeaderTab(header);
};



async function handleFormSubmit(event) {

    event.preventDefault();

    if (!confirm("Are you sure you want to save these changes?")) {
        event.preventDefault(); 
    }
    const form      = new FormData(frequencyForm);
    const frequency = form.get("frequency");

    const response  = await fetchData({
        url:"/subscription/update/",
        csrfToken: CSRF_TOKEN,
        body: {frequency: {frequency: frequency}}
    });


    const success = await handleResponse(response);
    if (success) {
       console.log("Successful");
    };

};


// The number of characters left to use on the feedback form
minimumCharactersToUse(feedBackFormTextArea, {
    minCharClass: ".minimum-characters",
    minCharMessage: "Minimum characters: ",
    maxCharClass: ".maximum-characters",
    maxCharMessage: "Characters remaining: ",
    minCharsLimit: 50,
    maxCharsLimit: 255,
    disablePaste: true,
});



function handleFeedbackForm() {
    if (validateFeedbackForm) {
        feedbackForm.submit();
    }
  
};


function validateFeedbackForm() {
    const feedback = feedbackForm?.reason_for_unsubscribing.value.trim();
    return feedback.length >= 50; 
};


function handleUnsubscribeBtnClick(e) {
    e.preventDefault();

    toggleSubscribeBtnState()
    toggleFeedBackContainer()
 
};


function handleCancelButtonClick(e) {
    toggleSubscribeBtnState(false);
    toggleFeedBackContainer(false)
}


function toggleSubscribeBtnState(disable=true) {
    unsubscribeBtn.disabled =  disable ? true : false;
};


function toggleFeedBackContainer(show=true) {
    show ? feedBackFormContainer.classList.add("show") : feedBackFormContainer.classList.remove("show");
};