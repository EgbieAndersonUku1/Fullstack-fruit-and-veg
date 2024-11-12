/**
 * Hides all tab sections by removing their active status and applying the "d-none" class.
 * 
 * @param {NodeList} tabSections - A collection of tab section elements to be hidden.
 */
export function hideAllTabSection(tabSections) {
    removeActiveFromTabs();  
    tabSections.forEach((tabSection) => hideTabSection(tabSection));
};


/**
 * Shows a specific tab section by removing the "d-none" class.
 * 
 * @param {HTMLElement} tab - The tab section element to be displayed.
 */
export function showTabSection(tab) {   
    tab.classList.remove("d-none");
};


/**
 * Hides a specific tab section by adding the "d-none" class.
 * 
 * @param {HTMLElement} tab - The tab section element to be hidden.
 */
export function hideTabSection(tab) {
    tab.classList.add("d-none");
};


/**
 * Adds an "active" class and a "highlight" class to a header, marking it as the active tab.
 * 
 * @param {HTMLElement} header - The tab header element to be marked as active.
 * @param {string} activeClassName - The class name to be used to mark the tab as active. Defaults to "active".
 */
export function addActiveStatusToHeaderTab(header, activeClassName) {
    if (header && !header.classList.contains(activeClassName)) {
        header.classList.add(activeClassName, "highlight");
    };
};


/**
 * Removes the active status (removes "active" and "highlight" classes) from all tab headers.
 * 
 * @param {NodeList} headers - A collection of tab header elements to remove the active status from.
 * @param {string} activeClassName - The class name used to mark a tab as active. Defaults to "active".
 */
export function removeActiveFromTabs(headers, activeClassName="active") {
    if (headers) {
        headers.forEach((header) => {
            if (header.classList.contains(activeClassName)) {
                header.classList.remove(activeClassName, "highlight");
            };
        });
    };
};


/**
 * Toggles the visibility of tabs. Hides all tabs except the one to be shown and marks its header as active.
 * 
 * @param {HTMLElement} showTab - The tab to be displayed.
 * @param {Array<HTMLElement>} hideTabs - A list of tabs to be hidden.
 * @param {HTMLElement} header - The header element to be marked as active.
 * @param {string} headerClassName - The class name to be applied to the active tab header. Defaults to "active".
 */
export function toggleTabVisibility(showTab, hideTabs, header, headerClassName="active") {
    hideTabs.forEach(hideTabSection);
    showTabSection(showTab);
    addActiveStatusToHeaderTab(header, headerClassName);
};
