
import dotenv from 'dotenv';

import { businessData } from "./trainingData.js";
import { MessageHistory } from './faq_bot_utils.js';
import { setUPGenModel } from './faq_bot_utils.js';

dotenv.config()


const ENV = process.env.API_KEY;



const API_KEY = "Api-key here";
const model   = setUPGenModel({API_KEY: API_KEY, systemInstruction: businessData});

const messages     = new MessageHistory()
let messageHistory = messages.get_messages();


const chat = model.startChat(messageHistory);

// test 1
let resp = await chat.sendMessage("What are the opening hours");
messages.add_message({role:"user", message:"what are the opening hours?"});
messages.add_message({role:"model", message:resp.response.text()})



// test 2
const chat2 = model.startChat(messageHistory);
resp        = await chat2.sendMessage("How do you register?");

messages.add_message({role: "user", message: "How do you register?"});
messages.add_message({role:"model", message:resp.response.text()})

console.log(messageHistory)


// test to see if it added to message history --- remove later

for (let message of messageHistory.history ) {
    const role = message.role;
    const parts = message.parts[0].text;


    if (role === "model") {
        console.log(`Faq bot responses - ${parts}\n\n` );

    } else {
        console.log(`User Question - ${parts}` );
    }
}