import google.generativeai as genai


def setup_generative_model(api_key, system_instruction="", model_type="gemini-1.5-flash"):
    
    if not api_key:
        raise ValueError("The api key cannot be empty")
    if not model_type:
        raise ValueError("Thhe model cannot be empty")
    
    genai.configure(api_key=api_key)
    
    if system_instruction:
        model = genai.GenerativeModel(system_instruction=system_instruction, model_name=model_type)
    else:
         model = genai.GenerativeModel(model_name=model_type)
    return model
        