import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from 'dotenv';

import { businessData } from "./trainingData.js";


dotenv.config()


const ENV = process.env.API_KEY;


// get the API from the env environment

const history = [];


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
function setUPGenModel({API_KEY, systemInstruction, modelType="gemini-1.5-flash"}) {

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
        console.log(error);
    }
    
}


const API_KEY = "API KEY here"
const model = setUPGenModel({API_KEY: API_KEY, systemInstruction: businessData})

const chat = model.startChat({
    history: history,
  });


  // Test
  let result = await chat.sendMessage("What are the opening hours");
  console.log(result.response.text());
  result = await chat.sendMessage("What products do you sell?");
  console.log(result.response.text());