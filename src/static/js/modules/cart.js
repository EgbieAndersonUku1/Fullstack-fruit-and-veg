const itemCart             = document.querySelector(".item-cart");
const itemCartTotal        = document.querySelector(".cart-item-total");

// For now this will be stored as a mock DB but will be replaced later
// in the local storage when the backend is built. Example of how the cart looks
// const itemCart = [
//     {
//         "id"  : "#id",
//         "name": "some item name",
//         "price": 9.88,
//         "quantity": 4

//     }
// ]


/**
 * The ItemCart class is designed to manage a shopping cart, providing methods to add, update, delete items,
 * and calculate the total quantity and price of items in the cart.
 */
class ItemCart {

    constructor() {
        this._NOT_FOUND = -1;
        this._cart      = [];
    }

    /**
     * Updates the cart display with the number of items and the total price.
     * 
     * @param {number} numOfItems - The number of items in the cart.
     * @param {number} totalPrice - The total price of items in the cart.
     * @param {string} [sign="£"] - The currency sign or other prefix to display with the total price.
     */
    static updateCartDisplay(numOfItems, totalPrice, sign="£") {

        itemCart.textContent      = numOfItems < 10 ? numOfItems : "10+";
        itemCart.style.display    = numOfItems <= 0 ? "none" : "block";   
        itemCartTotal.textContent = (parseInt(totalPrice) <= 0) ? `Items: ${sign}0.00` : `Items: ${sign}${totalPrice}`;
    }

    /**
     * Adds an item to the cart. If the item already exists, its quantity is increased by one.
     * 
     * @param {Object} item - The item to add to the cart.
     */
    add(item) {
        const index = this.findByID(item.id).index;
        if (index === this._NOT_FOUND) {
            item.quantity = 1;
            this._cart.push(item);
        } else {
            this._updateItemQuantityByOne(index);
        }
    }

    /**
     * Updates the quantity of an item in the cart by one.
     * 
     * @param {number} index - The index of the item in the cart.
     * @returns {boolean} - Returns true if the quantity was updated or false if not.
     * @private
     */
    _updateItemQuantityByOne(index) {
        if (index !== this._NOT_FOUND) {
            this._cart[index].quantity += 1;
            return true;
        }
        return false;
    }

    /**
     * Updates the quantity of an item in the cart. If the item does not exist, it is added to the cart.
     * 
     * @param {Object} item - The item to update in the cart.
     */
    updateCartItemQuantity(item) {
        const index = this.findByID(item.id).index;
        if (index === this._NOT_FOUND) {
            this._cart.push(item);
        } else {
            this._cart[index].quantity = item.quantity;
        }
    }

    /**
     * Deletes an item from the cart by its ID.
     * 
     * @param {number} id - The ID of the item to delete.
     * @returns {boolean} - Returns true if the item was deleted, false if the item was not found.
     */
    deleteByID(id) {
        const index = this.findByID(id).index;
        if (index != this._NOT_FOUND) {
            this._cart.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * Gets the total quantity of items in the cart.
     * 
     * @returns {number} - The total quantity of items in the cart.
     */
    getCartQuantity() {
        let itemsCount = 0;
        this._cart.forEach((item) => {
            if (item.quantity > 0) {
                itemsCount += item.quantity;
            }
        });
        return itemsCount;
    }

    /**
     * Gets the total price of items in the cart.
     * 
     * @returns {number} - The total price of items in the cart, rounded to two decimal places.
     */
    getTotalPrice() {
        let totalPrice = 0;
        this._cart.forEach((item) => {
            const itemTotal = item.quantity * item.price; 
            totalPrice += itemTotal;
        });
        return parseFloat(totalPrice.toFixed(2)); 
    }

    /**
     * Clears all items from the cart.
     */
    clearCart() {
        this._cart = [];
    }

    /**
     * Gets all items currently in the cart.
     * 
     * @returns {Object[]} - An array of all items in the cart.
     */
    getAllItems() {
        return this._cart;
    }

    /**
     * Finds an item in the cart by its ID.
     * 
     * @param {number} id - The ID of the item to find.
     * @returns {Object} - An object containing the item and its index. 
     * If the item is not found, returns {item: null, index: -1}.
     */
    findByID(id) {
        const index = this._cart.findIndex(item => parseInt(item.id) === parseInt(id));
        if (index === this._NOT_FOUND) {
            return {item: null, index: this._NOT_FOUND};
        }
        const item = this._cart[index];
        return {item: item, index: index};
    }
}


export default ItemCart;
