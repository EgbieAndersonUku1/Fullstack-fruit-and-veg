import orders from "../../../order.js";
import { getItemFromLocalStorage,  saveToLocalStorage, redirectToNewPage } from "../utils/utils.js";


const productReviewTable = document.getElementById("products-review-table");
const pagination          = document.querySelector(".table-pagination");
const notFound            = document.querySelector(".not-found");


function createProductTable(orders, show=true) {

    if (!productReviewTable) {
        return;
    }
    if (!show) {
        productReviewTable.style.display = "none";
        pagination.style.display         = "none";
        notFound.style.display           = "block";
        return;
    } else {
        productReviewTable.style.display = "table";
        pagination.style.display         = "flex";
        notFound.style.display           = "none";
    }


        productReviewTable.innerHTML = "";
    
        const tableHeading = createTableHeading();
        const tableBody = buildTableBody(orders);

        if (productReviewTable) {
            productReviewTable.appendChild(tableHeading);
            productReviewTable.appendChild(tableBody);
        }
    

}

function createTableHeading() {

    const tableMainRow = document.createElement("tr");
    const tableHeader1 = document.createElement("th");
    const tableHeader2 = document.createElement("th");
    const tableHeader3 = document.createElement("th");
    const tableHeader4 = document.createElement("th");
    const tableHeader5 = document.createElement("th");
    const tableHeader6 = document.createElement("th");

    tableHeader1.textContent = "Product ID";
    tableHeader2.textContent = "Product Name";
    tableHeader3.textContent = "Purchase Date";
    tableHeader4.textContent = "Review Status";
    tableHeader5.textContent = "Action";
    tableHeader6.textContent = "Product Image";

    tableMainRow.appendChild(tableHeader1);
    tableMainRow.appendChild(tableHeader2);
    tableMainRow.appendChild(tableHeader3);
    tableMainRow.appendChild(tableHeader4);
    tableMainRow.appendChild(tableHeader5);
    tableMainRow.appendChild(tableHeader6);

    return tableMainRow;

}


function buildTableBody(orders) {
    const fragment = document.createDocumentFragment();

    if (!orders || !Array.isArray(orders)) {
        console.error("Orders data is not available or not an array.");
        return fragment;
    }


    orders.forEach((order) => {

        const tableMainRow = document.createElement("tr");
        const tableALink = createTableLink("Add/Edit", `${order.id}`);
        const tableImg = createTableImage(order)

        let [tableData1, tableData2, tableData3, tableData4, tableData5, tableData6] = [
            document.createElement("td"),
            document.createElement("td"),
            document.createElement("td"),
            document.createElement("td"),
            document.createElement("td"),
            document.createElement("td")
        ]


        tableData1.textContent = `${order.id}`;
        tableData2.textContent = `${order.name}`;
        tableData3.textContent = `${order.dateOrderPlaced}`;
        tableData4 = getReviewStatus(tableData4, order);
        tableData5.appendChild(tableALink);
        tableData6.appendChild(tableImg);

        [tableData1, tableData2, tableData3, tableData4, tableData5, tableData6].forEach((tableData) => {
            tableMainRow.appendChild(tableData);

        })


        fragment.appendChild(tableMainRow);
    })

    return fragment;

}

function getReviewStatus(tableRowToUpdate, product) {

    let reviews = getItemFromLocalStorage("productReviews", true);
    let reviewsFound = true;

    if (!reviews) {
      reviewsFound = false;
      reviews = orders;
    }

    reviews.forEach((review) => {
        
        if (!reviewsFound) {
            tableRowToUpdate.textContent = "Not reviewed";
        } else if (reviewsFound && review.id === product.id && tableRowToUpdate.textContent !== "Pending review") {
            tableRowToUpdate.textContent = "Pending review";
        } else if (tableRowToUpdate.textContent !== "Pending review") {
            tableRowToUpdate.textContent = "Not reviewed";
        }
    })

    return tableRowToUpdate
}


function createTableLink(linkText, productID, hrefTag = "#", className = "table-link") {

    const tableLink = document.createElement("a");
    tableLink.href = hrefTag;
    tableLink.className = className;
    tableLink.textContent = linkText;
    tableLink.dataset.productID = productID;


    tableLink.addEventListener("click", handleLinkClick);

    return tableLink;

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