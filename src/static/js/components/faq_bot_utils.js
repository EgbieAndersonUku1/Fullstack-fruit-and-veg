

export class MessageHistory {

    constructor() {
        this._messages = {
            history: []
        };
    }

    /**
     * Adds a message to the message history.
     * 
     * @param {string} role - The role of the message sender (either 'user' or 'model').
     * @param {string} message - The content of the message.
     * @throws {Error} If the role is not 'user' or 'model'.
     * @throws {Error} If the message is empty or undefined.
    */
    addMessage({role, message}) {
        let systemRole = role.toLowerCase();
        if (systemRole && systemRole !== "user" && role !== "model") {
            throw new Error(`The role must either be 'user' or 'model' not <${role}> `);
        };
    
        if (!message) {
            throw new Error("The message cannot be empty");
        };
    
        const messageObject = {
            role: systemRole,
            parts: [{text: message}]
        };
    
        this._messages.history.push(messageObject);
    }
    
    /**
     * Clears the message history by resetting the 'history' property to an empty array.
     */
    clearMessageHistory() {
        this._messages.history = [];
    }

    /**
     * Get the message history and returns the object
     */
    getMessages() {
        return this._messages;
    }

}