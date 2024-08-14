
/**
 * Sorts an array of objects based on the date property in ascending order.
 * 
 * @param {Array} arrayToSort - The array to sort.
 * @returns {Array} - The sorted array.
 * @throws {Error} - If the input is not an array or if any object in the array does not have a 'date' property.
 */
function sortByDateAscending(arrayToSort) {
    return sortByDateHelper(arrayToSort, 'ascending');
}


/**
 * Sorts an array of objects based on the date property in descending order.
 * 
 * @param {Array} arrayToSort - The array to sort.
 * @returns {Array} - The sorted array.
 * @throws {Error} - If the input is not an array or if any object in the array does not have a 'date' property.
 */
function sortByDateDescending(arrayToSort) {
    return sortByDateHelper(arrayToSort, 'descending');
}

/**
 * Helper function to sort an array of objects based on the date property.
 * 
 * @param {Array} arrayToSort - The array to sort.
 * @param {string} order - The order to sort ('ascending' or 'descending').
 * @returns {Array} - The sorted array.
 * @throws {Error} - If the input is not an array or if any object in the array does not have a 'date' property.
 */
function sortByDateHelper(arrayToSort, order) {
    if (!Array.isArray(arrayToSort)) {
        throw new Error(`The input must be an array, not type: ${typeof arrayToSort}`);
    }

    return arrayToSort.sort((a, b) => {
        if (!a.hasOwnProperty('date') || !b.hasOwnProperty('date')) {
            throw new Error('All objects in the array must have a "date" property');
        }

        const dateA = new Date(a.date);
        const dateB = new Date(b.date);

        if (order === 'ascending') {
            return dateA - dateB;
        } else if (order === 'descending') {
            return dateB - dateA;
        } else {
            throw new Error('Invalid sort order. Use "ascending" or "descending".');
        }
    });
}



/**
 * Sorts an array of objects in ascending order by the 'name' property.
 * 
 * @param {Array} arrayToSort - The array of objects to be sorted.
 * @returns {Array} - The sorted array.
 * @throws {Error} - If the input is not an array or if any object in the array does not have a 'name' property.
 */
function sortByNameAscending(arrayToSort) {
    return sortByHelper(arrayToSort, (a, b) => (a.name > b.name) ? 1 : (a.name < b.name) ? -1 : 0);
}


/**
 * Sorts an array of objects in descending order by the 'name' property.
 * 
 * @param {Array} arrayToSort - The array of objects to be sorted.
 * @returns {Array} - The sorted array.
 * @throws {Error} - If the input is not an array or if any object in the array does not have a 'name' property.
 */
function sortByNameDescending(arrayToSort) {
    return sortByHelper(arrayToSort, (a, b) => (a.name < b.name) ? 1 : (a.name > b.name) ? -1 : 0);
}


/**
 * Helper function to sort an array of objects based on a provided comparison function.
 * 
 * @param {Array} arrayToSort - The array of objects to be sorted.
 * @param {Function} compareFunction - The comparison function to determine the order of elements.
 * @returns {Array} - The sorted array.
 * @throws {Error} - If the input is not an array or if any object in the array does not have a 'name' property.
 */
function sortByHelper(arrayToSort, compareFunction) {
    if (!Array.isArray(arrayToSort)) {
        throw new Error(`The input must be an array, not type: ${typeof arrayToSort}`);
    }

    arrayToSort.sort((a, b) => {
        if (!a.name || !b.name) {
            throw new Error('All objects in the array must have a "name" property');
        }

        return compareFunction(a, b);
    });

    return arrayToSort;
}


export {
    sortByNameAscending,
    sortByNameDescending,
    sortByDateAscending,
    sortByDateDescending,
}