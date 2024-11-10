/**
 * Calculates the Euclidean distance between two points on two different elements.
 * The points are determined based on the top-left or bottom-right corners of the elements,
 * depending on the `useBottomRight` parameter.
 *
 * The distance is calculated using the Euclidean distance formula:
 * 
 *      distance = √((x2 - x1)² + (y2 - y1)²)
 *
 * @param {HTMLElement} element1 - The first DOM element.
 * @param {HTMLElement} element2 - The second DOM element.
 * @param {boolean} [useBottomRight=false] - If true, the calculation uses the bottom-right corners of the elements;
 *                                           otherwise, it uses the top-left corners. Defaults to false.
 * @returns {number} - The Euclidean distance between the two points on the elements.
 */
export function calculateDistanceBetweenTwoPoints(element1, element2, useBottomRight = false) {

    try {
        const rect1 = element1.getBoundingClientRect();
        const rect2 = element2.getBoundingClientRect();

        const x1 = useBottomRight ? rect1.right : rect1.left;
        const y1 = useBottomRight ? rect1.bottom : rect1.top;

        const x2 = useBottomRight ? rect2.right : rect2.left;
        const y2 = useBottomRight ? rect2.bottom : rect2.top;

        const distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
        return distance;

    } catch (error) {
        console.log(`Something went wrong - check the elements provided : ${error.message}`);
        return null;
    }

}
