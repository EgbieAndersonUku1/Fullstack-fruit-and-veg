
/**
 * Finds an item in the items list by its ID.
 * 
 * @param {string|number} id - The ID of the item to find.
 * @param {Array} itemsList - The list of items to search through.
 * @returns {Object|undefined} - The item object if found, otherwise undefined.
 * @throws Will throw an error if itemsList parameter is not an array.
 */
function getItemByID(id, itemsList) {
    if (!Array.isArray(itemsList)) {
        throw new Error("The items list must be an array");
    }
    return itemsList.find((item) => item.id === parseInt(id));
}



function getItemIndexAndValueByID(id, itemsList) {
    if (!Array.isArray(itemsList)) {
        throw new Error("The items list must be an array.");
    }

    const parsedId = parseInt(id);
    if (isNaN(parsedId)) {
        throw new Error("The id must be a valid number.");
    }

    for (let [index, item] of itemsList.entries()) {
        if (item.id === parsedId) {
            return [index, item];
        }
    }
    return [null, null];
}





export {
    getItemByID,
    getItemIndexAndValueByID,
}