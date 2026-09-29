import ollama

model_name = 'qwen3-vl:8b'
try:
    models = ollama.list()
    model_names = [m.model for m in models.models]
    if model_name in model_names:
        # Stream the response to see thinking process
        response = ollama.chat(
            model=model_name,
            messages=[{
                'role': 'user',
                'content': 'Randomly say ONLY yes or no'
            }],
           # stream=True  # Enable streaming
        )
        
        # Save the response
        with open('response.txt', 'w') as f:
            f.write(response)
    else:
        print(f"Model {model_name} not found")

except Exception as e:
    print(f"Error checking models: {e}")




