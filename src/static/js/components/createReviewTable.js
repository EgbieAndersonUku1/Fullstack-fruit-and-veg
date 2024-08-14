import orders from "../../../order.js";
import {createTableHeaderRow, createTableRow} from "../utils/createTableElements.js";
import { getItemFromLocalStorage,  saveToLocalStorage, redirectToNewPage } from "../utils/utils.js";
import { createTableLink } from "../utils/linkUtils.js";


const productReviewTable = document.getElementById("products-review-table");
const pagination          = document.querySelector(".table-pagination");
const notFound            = document.querySelector(".not-found");



function toggleTableVisibility(show, orders) {
    if (!show || orders.length === 0) {
        productReviewTable.style.display = "none";
        pagination.style.display         = "none";
        notFound.style.display           = "block";
    } else {
      
        // Clear the table content before showing the table
        productReviewTable.innerHTML = "";
        productReviewTable.style.display = "table";
        pagination.style.display         = "flex";
        notFound.style.display           = "none";
    }
}

function createProductTable(orders, show=true) {

    if (!productReviewTable) {
        return;
    }

    // Call the new function to handle visibility
    toggleTableVisibility(show, orders);

    if (!show || orders.length === 0) {
        return;
    }

    const headers = ["Product ID", "Product Name", "Purchase Date", "Review Status", "Action", "Product Image"];
        
    const tableHeading = createTableHeaderRow(headers);
    const tableBody    = buildTableBody(orders);

    if (productReviewTable) {
        productReviewTable.appendChild(tableHeading);
        productReviewTable.appendChild(tableBody);
    }
}



function buildTableBody(orders) {
    const fragment = document.createDocumentFragment();

    if (!orders || !Array.isArray(orders)) {
        console.error("Orders data is not available or not an array.");
    };


    orders.forEach((order) => {
        const tableALink = createTableLink({linkText: "Add/Edit", productID: order.id, handleClick: handleLinkClick})
        const tableImg = createTableImage(order);

        const listOfDataColumns = [order.id,
                                   order.name,
                                   order.dateOrderPlaced,
                                   getReviewStatus(order),
                                   "",  // placeholder for the link
                                   "",  // placeholder for the image
                          ]
    
        
        const additionalElements = {
            4: tableALink,
            5: tableImg,
        }
        const tableMainRow = createTableRow(listOfDataColumns, additionalElements);
        fragment.appendChild(tableMainRow);
       

    })

    return fragment;

}


function getReviewStatus(product) {

    let reviews = getItemFromLocalStorage("productReviews", true);
    let reviewsFound = true;
    let status;

    if (!reviews) {
      reviewsFound = false;
      reviews = orders;
    }

    for (let review of reviews) {
        if (!reviewsFound) {
            status = "Not reviewed";
            break
          
        } else if (reviewsFound && review.id === product.id) {
            status = "Pending review";
            break;
         
        } else {
            status = "Not reviewed";
        }
    }

    return status
}


function createTableImage(order, className = "table-img") {
    const tableImg     = document.createElement("img");
    tableImg.src       = order.img;
    tableImg.alt       = `${order.name} icon`;
    tableImg.className = className;
    return tableImg;
}





function handleLinkClick(e) {
    const productID = e.currentTarget.dataset.productID;

    if (productID) {
        saveToLocalStorage("productTableLink", { id: parseInt(productID) }, true);
    }
    const urlPage = "add-review.html";
    redirectToNewPage(urlPage);
}


export default createProductTable