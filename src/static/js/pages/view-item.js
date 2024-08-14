const breadCrumbLiNameLiElement = document.querySelector(".breadcrumb .item-name");
const dateOrderedPElement       = document.querySelector(".view-item__date-ordered");
const deliverDateMsgPElement    = document.querySelector(".view-item__deliver-msg");
const deliverDateSpanElement    = document.querySelector(".view-item__delivered-date");
const h3Element                 = document.querySelector(".view-item__title .view-item_title__wrapper h3");
const orderByElement            = document.querySelector(".view-item__ordered_by");
const orderIDElement            = document.querySelector(".view-item__order-id");
const orderTotalElement         = document.querySelector(".view-item__order-total");
const pageRedirectLinkElement   = document.querySelector(".view-item__title .view-item_title__wrapper a");
const returnMsgPElement         = document.querySelector(".view-item__return-msg");
const viewItemImageElement      = document.querySelector(".view-item__img img");

import { getItemFromLocalStorage } from "../utils/utils.js";
import {getItemByID} from "../utils/itemUtils.js";
import orders from "../../../order.js";


function updateViewItemPage() {


    if (!(h3Element instanceof HTMLElement) || !(pageRedirectLinkElement instanceof HTMLElement) ||
        !(deliverDateSpanElement instanceof HTMLElement) || !(deliverDateMsgPElement instanceof HTMLElement) ||
        !(returnMsgPElement instanceof HTMLElement) || !(dateOrderedPElement instanceof HTMLElement) || !(viewItemImageElement)
        || !(breadCrumbLiNameLiElement) || !(orderByElement) || !(orderIDElement) || !(orderTotalElement)) {
        throw new Error("One or more elements are not HTML elements");
    }


    const order = getItemByID(getItemFromLocalStorage("itemOrder"), orders, true);

    if (!order) {
        throw new Error("The order returned cannot be empty");
    }

    breadCrumbLiNameLiElement.textContent  = order.name;
    dateOrderedPElement.textContent        = `Order placed on: ${order.dateOrderPlaced}`;
    deliverDateMsgPElement.textContent     = order.deliverMsg;
    deliverDateSpanElement.textContent     = order.dateToDeliver;
    h3Element.textContent                  = order.name;
    orderByElement.textContent             = `Ordered by: ${order.orderBy}`;
    orderIDElement.textContent             = `Order ID: ${order.orderID}`;
    orderTotalElement.textContent          = `Order total: £${order.total}`;
    pageRedirectLinkElement.href           = order.pageRedirectLink;
    returnMsgPElement.textContent          = order.returnMsg;
    viewItemImageElement.alt               = order.name;
    viewItemImageElement.className         = "view-item__img";
    viewItemImageElement.src               = order.img;
   
}

document.addEventListener("DOMContentLoaded", () => {
    updateViewItemPage();
});
