/**
 * Creates an HTML anchor element (<a>) with customizable properties for use in a table or other UI elements.
 * 
 * This function allows you to create a link with various options, including setting its text content, URL, CSS class,
 * and a click event handler. Parameters not provided will use their default values.
 * 
 * @param {Object} options - An object containing the properties for the anchor element.
 * @param {string} options.linkText - The text content for the link. This is a required parameter.
 * @param {number|string} options.productID - The ID associated with the product, used as a data attribute. This is a required parameter.
 * @param {string} [options.hrefTag="#"] - The URL or path the link should point to. Defaults to "#" if not provided.
 * @param {string} [options.className="table-link"] - The CSS class to be applied to the link. Defaults to "table-link".
 * @param {function|null} [options.handleClick=null] - An optional click event handler for the link. Defaults to null if not provided.
 * @param {string} [options.dataAttrName="productID"] - The name of the data attribute to store the product ID. Defaults to "productID".
 * @returns {HTMLAnchorElement|null} - The created anchor element, or null if the `productID` is invalid.
 * 
 * @example
 * // Create a link with all options specified
 * const viewLink = createTableLink({
 *     linkText: "View Product",
 *     productID: 123,
 *     hrefTag: "/product/123",
 *     className: "view-link",
 *     handleClick: () => { console.log("Link clicked!"); },
 *     dataAttrName: "data-id"
 * });
 * 
 * // Create a link with only required parameters and defaults for the rest
 * const simpleLink = createTableLink({
 *     linkText: "Home",
 *     productID: 1
 * });
 * 
 * // Create a link with a custom click handler and default values for other parameters
 * const clickableLink = createTableLink({
 *     linkText: "Click Me",
 *     productID: 456,
 *     handleClick: () => { console.log("Clickable link clicked!"); }
 * });
 */
function createTableLink({ linkText, productID, hrefTag = "#", className = "table-link", handleClick = null, dataAttrName = "productID" }) {
    if (!productID) {
        console.warn("Invalid productID:", productID);
        return null;
    }

    const tableLink = document.createElement("a");
    tableLink.href = hrefTag;
    tableLink.className = className;
    tableLink.textContent = linkText;
    tableLink.dataset[dataAttrName] = productID;

    if (typeof handleClick === 'function') {
        tableLink.addEventListener("click", handleClick);
    }

    return tableLink;
}


export { createTableLink};

