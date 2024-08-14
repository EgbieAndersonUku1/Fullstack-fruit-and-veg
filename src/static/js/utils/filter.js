/**
 * Filters out reviewed items from a list based on their IDs.
 * 
 * @param {Array} itemIDs - The list of reviewed item IDs.
 * @param {Array} items - The list of items to filter.
 * @returns {Array} - An array of items that have not been reviewed.
 * @throws Will throw an error if itemIDs or items are not arrays.
 */
function filterByNotReviewed(itemIDs, items) {
    if (!Array.isArray(items) || !Array.isArray(itemIDs)) {
        throw new Error("Both itemIDs and items must be arrays.");
    }

    const notReviewed = items.filter(item => !itemIDs.includes(item.id));   
    return notReviewed;
}



export  {
    filterByNotReviewed,
}