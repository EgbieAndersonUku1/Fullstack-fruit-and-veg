import { validateElement } from "../errors/customErrors.js";

const headers                  = document.querySelectorAll("#subscription-tabs .tab > h4");
const tabSections              = document.querySelectorAll(".tab-section");
const subscriptionTabContainer = document.getElementById("subscription-tabs");
const subscriptionOverview     = document.getElementById("subscription-overview");
const subscriptionHistory      = document.getElementById("subscription-history");
const notificationAlert        = document.getElementById("notification-alerts");


// check if the global elements are valid before proceeding
[subscriptionTabContainer, subscriptionOverview, subscriptionHistory, notificationAlert].forEach((element) => {
    validateElement(element, "The html is not a valid element", true);
});


document.addEventListener("DOMContentLoaded", setUp);


function setUp() {

    hideAllTabSection();
    removeActiveFromTabs();

    showTabSection(subscriptionOverview);
 
    const firstTab = headers[0]
    addActiveStatusToHeaderTab(firstTab);

};


function hideAllTabSection() {
    tabSections.forEach((tabSection) => {
        hideTabSection(tabSection);
        removeActiveFromTabs();  
    })
};


function showTabSection(tab) {   
    tab.classList.remove("d-none");
};


function hideTabSection(tab) {
    tab.classList.add("d-none");
};


function addActiveStatusToHeaderTab(header) {
    if (header && !header.classList.contains("active")) {
        header.classList.add("active");
        header.classList.add("highlight");
    };
};


function removeActiveFromTabs() {
   
    if (headers) {
        headers.forEach((header) => {
    
           if (header && header.classList.contains("active")) {
                header.classList.remove("active");
                header.classList.remove("highlight");
           };
        });
    };
};



subscriptionTabContainer.addEventListener("click", (e) => {
    e.preventDefault();

    const SUBSCRIPTION_OVERVIEW = "subscription overview";
    const SUBSCRIPTION_HISTORY  = "subscription history";
    const NOTIFICATION          = "notifications"

    if (e.target.nodeName == "H4") {

        const innerText = e.target.innerText.toLowerCase();

        removeActiveFromTabs();
       
        if (innerText === SUBSCRIPTION_OVERVIEW) {

            showTabSection(subscriptionOverview);
            hideTabSection(subscriptionHistory);
            hideTabSection(notificationAlert);

            const firstTab = headers[0];
            addActiveStatusToHeaderTab(firstTab);


        } else if (innerText === SUBSCRIPTION_HISTORY) {

            showTabSection(subscriptionHistory);
            hideTabSection(subscriptionOverview);
            hideTabSection(notificationAlert);

            const secondTab = headers[1];
            addActiveStatusToHeaderTab(secondTab);

        } else if (innerText === NOTIFICATION) {

            showTabSection(notificationAlert);
            hideTabSection(subscriptionOverview);
            hideTabSection(subscriptionHistory);

            const thirdTab = headers[2]
            addActiveStatusToHeaderTab(thirdTab);

        }  
    }
   
});



