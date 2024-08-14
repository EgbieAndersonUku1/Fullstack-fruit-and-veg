/**
 * Rotates and switches the display of images based on the event type.
 * 
 * @param {string} type - The event type (e.g., "mouseover" or "mouseout").
 * @param {Array<HTMLElement>} images - An array containing two image elements.
 * @param {boolean} [rotate=true] - Flag to enable or disable image rotation.
 * @throws Will throw an error if the images array has less than two elements or if the 
 * elements are not valid DOM elements.
 */
function rotateImages(type, images, rotate = true) {
    if (images && images.length < 2) {
        throw new Error("The images array must contain at least two elements");
    }

    const [img, img2] = images;

    if (!(img instanceof HTMLElement) || !(img2 instanceof HTMLElement)) {
        throw new Error("Both elements in the images array must be valid DOM elements");
    }

    const DELAY_IN_MILLISECONDS = 400;

    switch (type) {
        case "mouseover":
            if (rotate) {
                img.style.transform = "rotate(180deg)";
            }
            setTimeout(() => {
                img.style.display = "none";
                img2.style.display = "block";
            }, DELAY_IN_MILLISECONDS);
            break;

        case "mouseout":
            if (rotate) {
                img.style.transform = "rotate(360deg)";
            }
            setTimeout(() => {
                img.style.display = "block";
                img2.style.display = "none";
            }, DELAY_IN_MILLISECONDS);
            break;

        default:
            throw new Error("Unsupported event type");
    }
}

export default rotateImages;
