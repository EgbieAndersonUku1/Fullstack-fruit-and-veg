
import dotenv from 'dotenv';

import { businessData } from "./trainingData.js";
import { MessageHistory, setUPGenModel } from './faq_bot_utils.js';




dotenv.config()


const ENV = process.env.API_KEY;



const API_KEY = "AIzaSyDzkcI_lvUXmhPx-73aKC7-Q5OdYraCTmo";
const model   = setUPGenModel({API_KEY: API_KEY, systemInstruction: businessData});

const messages     = new MessageHistory()
let messageHistory = messages.get_messages();


const chat = model.startChat(messageHistory);

// test 1
let resp = await chat.sendMessage("What are the opening hours");
messages.add_message({role: "user", message: "what are the opening hours?"});
messages.add_message({role: "model", message: resp.response.text()})






