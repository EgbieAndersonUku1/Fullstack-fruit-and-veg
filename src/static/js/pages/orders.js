import { saveToLocalStorage, redirectToNewPage } from "../utils/utils.js";

const viewItemButtons = document.querySelectorAll(".order-information .info-btns .view-item-btn");
const viewInvoiceBtns = document.querySelectorAll(".view-invoice-btn");


viewItemButtons.forEach((buttonElement) => {
    buttonElement.addEventListener("click", () => {
        handleBtnClick(buttonElement, "data-order-id", "view-item.html", "itemOrder");
    });
});



viewInvoiceBtns.forEach((buttonElement) => {
    buttonElement.addEventListener("click", () => {
        handleBtnClick(buttonElement, "data-order-id", "invoice.html", "invoice");
    });
});



function handleBtnClick(buttonElement, dataAttribute, urlPage, key) {
    const id = buttonElement.getAttribute(dataAttribute);
    if (id) {
        const objectToSave = {
            key: key,
            value: parseInt(id),
        };
        saveToLocalStorage(objectToSave.key, objectToSave.value, true);
       
        redirectToNewPage(urlPage);
    }
}
