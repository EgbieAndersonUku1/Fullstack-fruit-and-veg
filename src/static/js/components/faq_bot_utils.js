import { GoogleGenerativeAI } from "@google/generative-ai";


/**
 * Sets up and returns a generative AI model using the provided API key, system instruction, and model type.
 * 
 * @param {Object} params - The parameters required to set up the generative model.
 * @param {string} params.API_KEY - The API key required for authentication with the Google Generative AI service.
 * @param {string} params.systemInstruction - The system instruction that defines the behaviour of the model.
 * @param {string} [params.modelType="gemini-1.5-flash"] - The model type to use. Defaults to "gemini-1.5-flash" if not provided.
 * 
 * @returns {Object} The initialized generative model.
 * 
 * @throws {Error} Throws an error if any required parameters are missing or if there's an issue setting up the model.
 */
export function setUPGenModel({API_KEY, systemInstruction, modelType="gemini-1.5-flash"}) {

    if (!API_KEY) {
        throw new Error("The API key wasn't found")
    };

    if (!systemInstruction) {
        throw new Error("The system instruction wasn't found - please add before ")
    };

    if (!modelType) {
        throw new Error("The modelType cannot be empty");
    }

    try {
        const genAI  = new GoogleGenerativeAI(API_KEY);
        const model  = genAI.getGenerativeModel({ model: modelType, systemInstruction:systemInstruction });
        return model
    } catch (error) {
        console.error("Error setting up the generative model:", error.message);
        throw error;
    }
    
}


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
    add_message({role, message}) {
        if (role !== "user" && role !== "model") {
            throw new Error(`The role must either be 'user' or 'model' not <${role}> `);
        };
    
        if (!message) {
            throw new Error("The message cannot be empty");
        };
    
        const messageObject = {
            role: role,
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
    get_messages() {
        return this._messages;
    }

}