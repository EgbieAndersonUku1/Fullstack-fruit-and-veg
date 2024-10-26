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
subscriptionTabContainer.addEventListener("click", handleSubscriptionTabs);


function setUp() {

    hideAllTabSection();
    removeActiveFromTabs();

    showTabSection(subscriptionOverview);
 
    const firstTab = headers[0]
    addActiveStatusToHeaderTab(firstTab);

};


function hideAllTabSection() {
    removeActiveFromTabs();  
    tabSections.forEach((tabSection) => hideTabSection(tabSection))
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
}


