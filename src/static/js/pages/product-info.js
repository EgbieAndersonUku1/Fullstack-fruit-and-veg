import { createTableHeaderRow, createTableRow } from "../utils/createTableElements.js";
import { createTableLink } from "../utils/linkUtils.js";
import { getItemFromLocalStorage, removeItemFromLocalStorage, saveToLocalStorage } from "../utils/utils.js";
import { getItemIndexAndValueByID } from "../utils/itemUtils.js";
import { validateElement } from "../errors/customErrors.js";

import AlertUtils from "../utils/alerts.js";

const allProductsDivElement     = document.getElementById("all-products");
const liveProductDivElement     = document.getElementById("live-products");
const notLiveProductDivElement  = document.getElementById("not-live");

const productMessage            = document.getElementById("product-msg");
const clearProductButtonElement = document.getElementById("clearBtn");


let currentTabName;


// to be assigned later when the `createTable` function is called for `all products`, `live products` and `not live`
let allProductsTable;
let liveProductsTable;
let notLiveProductsTable;


const tabContents                       = document.querySelectorAll(".tab-content");
const tabDivElement                     = document.getElementById("tabs");
const tabsElements                      = document.querySelectorAll(".tab");


const LIVE_TEXT                          = "Go live";
const DEACTIVATE_TEXT                    = "Deactivate";
const SAVE_TABLE_NAME                    = "products-list";

// table anchor link classes
const GO_LIVE_CLASS                      = "go-live";
const ACTION_LINK_CLASS                  = "action-link";


// Constants for Tab IDs
const ALL_PRODUCT_TAB_ID                 = "all-products-tab";
const LIVE_PRODUCT_TAB_ID                = "live-products-tab";
const NOT_LIVE_PRODUCT_TAB_ID            = "not-live-products-tab";


// table class names
const ALL_PRODUCTS_TABLE_CLASS_NAME       = "all-product-table";
const LIVE_PRODUCTS_TABLE_CLASS_NAME      = "live-products-table";
const NOT_LIVE_PRODUCTS_TABLE_CLASS_NAME  = "not-live-produts-table";


// all table entries
const productEntries  = getItemFromLocalStorage(SAVE_TABLE_NAME, true);



document.addEventListener("DOMContentLoaded", setUp);
clearProductButtonElement.addEventListener("click", handleClearButton);

tabDivElement.addEventListener("click", handleTabDelegation);



function showMessage(msg) {
    productMessage.textContent = msg;
    return;
}


/**
 * Creates and populates a table with product entries in the specified tab element.
 * 
 * This function generates an HTML table with headers and rows based on the provided product entries.
 * The table is then appended to the specified `tabElement`, replacing any existing content in that tab.
 * Additionally, the table is assigned a CSS class for styling purposes.
 * 
 * @param {Array} productTableEntries - An array of objects representing product entries. 
 *                                      Each object should have properties such as ID, product name, category, stock quantity, is live status, 
 *                                      and date created.
 * @param {HTMLElement} tabElement - The HTML element (tab) where the table should be inserted. This should be a valid instance of HTMLElement.
 * @param {string} className - The CSS class name to be applied to the created table for styling purposes.
 * 
 * @throws {Error} - Throws an error if `tabElement` is not a valid HTMLElement.
 * 
 * @example
 * // Sample product entries
 * const productEntries = [
 *     { id: 1, name: 'Product A', category: 'Category 1', stock: 10, isLive: true, dateCreated: '2024-01-01' },
 *     { id: 2, name: 'Product B', category: 'Category 2', stock: 5, isLive: false, dateCreated: '2024-02-01' }
 * ];
 * 
 * // Get tab elements
 * const allProductsTab = document.getElementById('allProducts');
 * const liveTab = document.getElementById('live');
 * const notLiveTab = document.getElementById('notLive');
 * 
 * // Create table in the 'live' tab with a specific class name
 * createTable(productEntries, liveTab, 'live-products-table');
 * 
 * // Create table in the 'allProducts' tab with a specific class name
 * createTable(productEntries, allProductsTab, 'all-products-table');
 * 
 * // Handle empty entries
 * createTable([], notLiveTab, 'empty-products-table'); // Will show message "You have not yet added a product"
 */
function createTable(productTableEntries, tabElement, className) {

    const ERR_MESSAGE = "Tab element is not an instance of HTMLElement.";
    
    if (!validateElement(tabElement, ERR_MESSAGE)) return;

    clearTabContent(tabElement);

    if (!productTableEntries || productTableEntries.length === 0) {
        showMessage("There are no products to display");
        return;
    }

    const headers   = ["ID", "Product Name", "Category", "Stock Quantity", "is Live", "Date created", "Action", "Action"];
    const table     = document.createElement("table");
    table.className = className;

    const tHeaders  = createTableHeaderRow(headers);
    const fragment  = document.createDocumentFragment();

    table.appendChild(tHeaders);

    appendTableRows(fragment, productTableEntries);

    table.appendChild(fragment);
    tabElement.appendChild(table);
    
    setProductTableElement(); 
   

}


// This function initializes references to product tables in the DOM. Since the tables are dynamically 
// generated by `createTable`, querying for them before their creation returns null. To ensure accurate 
// references, this function checks if each table variable is uninitialized and assigns it accordingly 
// after the tables exist in the DOM.
function setProductTableElement() {

    if (!allProductsTable) {
        allProductsTable = document.querySelector(`.${ALL_PRODUCTS_TABLE_CLASS_NAME}`);
        console.log("Initialized: All Products Table");
    };

    if (!liveProductsTable) {
        liveProductsTable = document.querySelector(`.${LIVE_PRODUCTS_TABLE_CLASS_NAME}`);
        console.log("Initialized: Live Products Table");
    };

    if (!notLiveProductsTable) {
        notLiveProductsTable = document.querySelector(`.${NOT_LIVE_PRODUCTS_TABLE_CLASS_NAME}`);
        console.log("Initialized: Not Live Products Table");
    }
 

}




function clearTabContent(tableElement) {
    productMessage.textContent = "";
    tableElement.innerHTML     = "";
};


function clearAllTabContents() {
    productMessage.textContent      = "";
    allProductsDivElement.innerHTML = "";
    liveProductDivElement.innerHTML = "";
    notLiveProductsTable.innerHTML  = "";
}


function validateProductData(product) {
    const { id, "product-name": name, "select-a-category": selectedCategory, 
          "add-category": addedCategory, "quantity-stock": stock, isLive, dateCreated } = product;

    const productCategory = selectedCategory === "new" ? addedCategory : selectedCategory;

    if (id && name && productCategory && stock && isLive !== '' && dateCreated) {
        return { id, name, productCategory, stock, isLive, dateCreated };
    } 
    console.error("One or more elements are missing for product ID:", id);
    return null;
    
}


function appendTableRows(fragment, productEntries) {
    productEntries.forEach((product) => {
        const productData = validateProductData(product);
        if (productData) {
            const row = createTableRowData(productData);
            fragment.appendChild(row);
        }
    });
}



function createTableRowData(productData) {
    const { id, name, productCategory, stock, isLive, dateCreated } = productData;
    
    const listOfDataColumns = [
        id, name, productCategory, stock, isLive, dateCreated,
        "", // placeholder for the go live link
        ""  // placeholder for the action link
    ];

    const linkText = isLive ? DEACTIVATE_TEXT : LIVE_TEXT;
    const additionalInformation = {
        6: createTableLink({ linkText: linkText, productID: id, className: GO_LIVE_CLASS }),
        7: createTableLink({ linkText: "Edit/Delete", productID: id, className: ACTION_LINK_CLASS }),
    };

    return createTableRow(listOfDataColumns, additionalInformation);
}



function handleClearButton() {
    const productEntries = getItemFromLocalStorage(SAVE_TABLE_NAME, true);

    if (!productEntries) {
        AlertUtils.showAlert({
            title: "No Items to Delete",
            text: "There are no items available to delete.",
            icon: "info",
            confirmButtonText: "OK",
        });   
        
        clearAllTabContents();
        showMessage("You have not yet added a product");
        return;
    };


    AlertUtils.showConfirmationAlert({
        title:  "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        confirmButtonText: "Yes, delete it",
        colorButtonOptions: {
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
        },
        func: () => {
            removeItemFromLocalStorage(SAVE_TABLE_NAME);
            clearAllTabContents();
            showMessage("You have not yet added a product");
            // console.log("Test")
        }, 
        followUpAlertAttrs: {
            title: "Completed!",
            text: "The action has been successfully completed.",
            icon: "success",
            confirmButtonText: "Great"
        }
        
    });

  
}



function processGoLiveCell(clickedCell, currentTableElement) {
    const productID         = clickedCell.dataset.productID;
    const [index, product]  = getItemIndexAndValueByID(productID, productEntries);


    const row               = clickedCell.closest('tr'); // Find the closest 'tr' element that is the table row element
    const rowIndex          = Array.prototype.indexOf.call(row.parentNode.children, row); 
    const cellIndexToUpdate = 4;

    updateProductElements(index, product, clickedCell); 
    updateProductLiveStatusCell(rowIndex, cellIndexToUpdate, product, currentTableElement);
}


function updateProductLiveStatusCell(rowIndex, cellIndexToUpdate, product, currentTableElement) {
    let rows = currentTableElement?.querySelectorAll('tr');

    if (!rows) {
        return;
    };

    // Check if the rowIndex is within the range of available rows
    if (rowIndex >= 0 && rowIndex < rows.length) {
        let row = rows[rowIndex];
        updateCellInRow(row, cellIndexToUpdate, product);
    } else {
        console.error('Row index is out of range. Available rows:', rows.length);
    }
}


function updateCellInRow(row, cellIndexToUpdate, product) {
    let cells = row.querySelectorAll('td');
    
    // Check if the cellIndexToUpdate is within the range of available cells in the row
    if (cellIndexToUpdate >= 0 && cellIndexToUpdate < cells.length) {

        // Update the content of the specified cell only
        cells[cellIndexToUpdate].textContent = product.isLive;
    } else {
        console.error('Cell index is out of range. Available cells in row:', cells.length);
    }
}


function updateProductElements(index, product, link) {
   
    let text;

    if (!validateIndex(index) || !validateLink(link)) {
        return;
    };

    switch(true) {
        case link.textContent.toUpperCase() === LIVE_TEXT.toUpperCase():

            link.textContent             = DEACTIVATE_TEXT;
            product.isLive               = true;
            text                         = "Your product is now live";
            productEntries[index].isLive = product.isLive;
            break;
        
        case link.textContent.toUpperCase() === DEACTIVATE_TEXT.toUpperCase():
            link.textContent             = LIVE_TEXT;
            product.isLive               = false;
            text                         = "Your product has been deactivated";
            productEntries[index].isLive = product.isLive;           
            break;
    }
    
    AlertUtils.showAlert({"title": "Update successful",
        text:text,
        icon: "success",
        confirmButtonText: "Great!!",
    });

    saveToLocalStorage(SAVE_TABLE_NAME, productEntries, true);
   
}


function validateIndex(index) {
    if (index === undefined || index === null) {
        console.error("Something went wrong and the id couldn't be found");
        return false;
    }
    return true;
}

function validateLink(link) {
    if (!link) {
        console.error("Something went wrong and the link couldn't be found");
        return false;
    }
    return true;
};





/**
 * Retrieves a list of products from the list that match the specified live status.
 *
 * @param {boolean} [live=true] - A boolean indicating the desired status. 
 *                                If true, returns all live products; if false, returns all not-live products.
 * @returns {Object[]} - Returns an array of product objects that match the live status. 
 *                       Returns an empty array if no matching products are found.
 *
 * @example
 * // Get all live products
 * const liveProducts = getProductsByStatus(true);
 *
 * // Get all not-live products
 * const notLiveProducts = getProductsByStatus(false);
 */
function getProductsByStatus(live = true) {
    if (productEntries.length === 0) {
        return [];
    }

    return productEntries.filter((product) => product.isLive === live);
};


// Function to handle tab delegation
function handleTabDelegation(e) {
    e.preventDefault();

    const clickedTab = e.target;
    
    switch(true) {
        case clickedTab.id.toLowerCase() === ALL_PRODUCT_TAB_ID.toLowerCase():
            const firstTab = tabsElements[0];
            configureTableDisplay(productEntries, allProductsDivElement, ALL_PRODUCTS_TABLE_CLASS_NAME, firstTab);
            break;
        case clickedTab.id.toLowerCase() === LIVE_PRODUCT_TAB_ID.toLowerCase():
            const secondTab    = tabsElements[1];
            const liveProducts = getProductsByStatus();
            configureTableDisplay(liveProducts, liveProductDivElement, LIVE_PRODUCTS_TABLE_CLASS_NAME, secondTab);
            break;
        case clickedTab.id.toLowerCase() === NOT_LIVE_PRODUCT_TAB_ID.toLowerCase():
            const thirdTab         = tabsElements[2];
            const notLiveProducts  = getProductsByStatus(false);
            configureTableDisplay(notLiveProducts, notLiveProductDivElement, NOT_LIVE_PRODUCTS_TABLE_CLASS_NAME, thirdTab);
            break;
        default:
            console.warn(`Unhandled tab ID: ${clickedTab.id}`);
            return;
    }

}

// Function to hide all tab content
function hideAllTabContent() {
    tabContents.forEach((tabElement) => {
        if (!tabElement) {
            console.warn(`Element not found: ${tabElement}`);
            return;
        }

        tabElement.classList.add("hide");
    });
}

// Function to remove the 'active' class from all tabs
function removeActiveFromTabs() {
    tabsElements.forEach((tabElement) => {
        if (!tabElement) {
            console.warn(`Tab element not found: ${tabElement}`);
            return;
        }

        tabElement.classList.remove("active");
    });
}

function toggleTabContentVisibility(tabElement) {
    tabElement.classList.toggle("hide");
}

function toggleActiveTabVisibility(tabElement) {
    tabElement.classList.toggle("active");
}


function handleEventDelegation(e) {
    e.preventDefault();
    let clickedCell = e.target;

    switch(true) {
        case clickedCell.className === GO_LIVE_CLASS && currentTabName.toLowerCase() === ALL_PRODUCT_TAB_ID.toLowerCase():
            processGoLiveCell(clickedCell, liveProductsTable);
            break;
        
        case clickedCell.className === GO_LIVE_CLASS && currentTabName.toLowerCase() === LIVE_PRODUCT_TAB_ID.toLowerCase():
            processGoLiveCell(clickedCell, liveProductsTable);

            // In the "All Products" tab, both "live" and "deactivated" products are displayed.
            // Only the specific cell that was clicked needs to be updated,
            // since the product will remain in the table regardless of its status.
            //
            // In the "Live Products" tab, only products that are currently "live" are shown.
            // If a product's status changes to "deactivated," it should no longer be displayed.
            // The entire table needs to be re-rendered to exclude the deactivated product.
            const liveProducts = getProductsByStatus();
            const secondTab    = tabsElements[1];
            configureTableDisplay(liveProducts, liveProductDivElement, LIVE_PRODUCTS_TABLE_CLASS_NAME, secondTab);
            showMessage("There are no live products to display. Please activate products to make them visible to customers.");
            break;
        
        case clickedCell.className === GO_LIVE_CLASS && currentTabName.toLowerCase() === NOT_LIVE_PRODUCT_TAB_ID.toLowerCase():
            processGoLiveCell(clickedCell, liveProductsTable);
            const notLiveProducts = getProductsByStatus(false);
            const thirdTab        = tabsElements[2];
            configureTableDisplay(notLiveProducts, notLiveProductDivElement, NOT_LIVE_PRODUCTS_TABLE_CLASS_NAME, thirdTab);
            showMessage("There are no deactivated products to display. Visit the products page tab to manage product status.");

            break;

    }
};



/**
 * Configures and displays a table within a tab, with optional tab-switching logic.
 *
 * This function sets up a table using the provided product entries, associates it with the specified
 * table element
 *
 * @param {Array} productEntries - The data to populate the table with.
 * @param {HTMLElement} tableElement - The DOM element representing the table container.
 * @param {string} tableClassName - The class name to apply to the table for styling or identification.
 * @param {HTMLElement} tabElement - The tab element that corresponds to the table being set up.
 *
 * @returns {void}
 */
function configureTableDisplay(productEntries, tableElement, tableClassName, tabElement) {
    
    hideAllTabContent();
    removeActiveFromTabs();
    toggleTabContentVisibility(tableElement);
    toggleActiveTabVisibility(tabElement);
    setCurrentTabName(tabElement.id);
    createTable(productEntries, tableElement, tableClassName);
    tableElement.addEventListener("click", handleEventDelegation);
}


function setUp() {
    const firstTab = tabsElements[0];
    configureTableDisplay(productEntries, allProductsDivElement, ALL_PRODUCTS_TABLE_CLASS_NAME, firstTab);
}



/**
 * Sets the current active tab by updating the global or contextual variable.
 *
 * @param {string} tabId - The ID of the tab to set as the current active tab.
 */
function setCurrentTabName(tabId) {
    currentTabName = tabId;
}
