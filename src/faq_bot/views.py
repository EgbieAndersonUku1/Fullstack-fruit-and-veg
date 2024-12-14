from django.shortcuts import render
from django.conf import settings

import json
from django.http import JsonResponse

from faq_bot.utils.gen_bot import setup_generative_model
from faq_bot.utils.training_data import business_instruction


# Create your views here.

def ask_question(request):
    
    if request.method == "POST":
        try:
            # Decode the JSON request body
            data = json.loads(request.body.decode('utf-8'))
        
            question        = data.get("question")
            message_history = data.get("messageHistory")
           
            if (not question):
                raise ValueError("Expect a question but recieved and empty string")
            
            
            model = setup_generative_model(settings.API_KEY, business_instruction)
            
            if not ("history" in message_history):
                raise ValueError("Expected the key 'history' inside message history dictionary but it wasn't found")
            
            messages = message_history["history"]
            if not isinstance(messages, list):
                raise TypeError(f"The messages within the message history must be a list -- not type {type(messages)}")
            
           
            chat  = model.start_chat(history=messages)
            query = chat.send_message(question)
            
            response = {
                "question": question,
                "history": message_history,
                "resp": query.text if query else query
            }
                     
        except json.JSONDecodeError:
            return JsonResponse({"SUCCESS": False, "MESSAGE": "Invalid request format", "DATA": {}}, status=400)
        
        return JsonResponse({"SUCCESS": True, "MESSAGE": "Successfully received and sent message", "DATA": response}, status=201)
    
    return JsonResponse(False, message="Invalid request method", status=405)
      