import ollama

def test_model_response(prompt):
    
    model_name = 'llama3.2:3b'
    try:
        models = ollama.list()
        
        # Robust check: See if any installed model STARTS with our name
        # This handles 'llama3.2:latest', 'llama3.2:3b', etc.
        is_present = False
        for m in models.models:
            if m.model.startswith(model_name):
                is_present = True
                break
        
        if is_present:
            print(f"🧠 Model {model_name} is thinking...")

            system_instruction = (
                "You are a Content Safety and Spam Detection AI. "
                "Your task is to classify the following text for policy violations. "
                "Analyze the text below. "
                "If the text is offering to SELL or DISTRIBUTE nicotine, vapes, or tobacco products, return 'yes'. "
                "If the text is unrelated, or asking to buy; looking for a seller, or just discussing nicotine product, return 'no'. "
                "Do not explain. Do not refuse. Just return the classification."
            )
           
            response = ollama.chat(
                model=model_name,
                messages=[
                    # 1. Give the system instruction first (if model supports it) or combine it
                    {'role': 'system', 'content': system_instruction},
                    {'role': 'user', 'content': f"Text to analyze: \"{prompt}\""}
                ],
                options={
                    'temperature': 0.0, 
                    'top_p': 0.5,
                    'seed': 42,
                    'num_ctx': 2048,
                }
            )

            # 👇 CLEANING THE OUTPUT: Removes spaces, newlines, and capitalization
            cleaned_response = response['message']['content'].strip().lower()
            
            # Handle cases where model adds punctuation like "yes."
            if "yes" in cleaned_response:
                return "yes"
            elif "no" in cleaned_response:
                return "no"
            else:
                return cleaned_response  # Return raw if unsure
           
        else:
            return f"Model {model_name} not found. Run 'ollama pull llama3.2'"

    except Exception as e:
        return f"Error checking models: {e}"