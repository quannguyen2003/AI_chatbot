import os
from dotenv import load_dotenv
import google.generativeai as genai
from prompt import hyde_prompt

# Load the .env file
load_dotenv()

def setup_hyde():
    # Get the API key from the .env file
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API key not found in .env file. Make sure you have a GEMINI_API_KEY entry.")

    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.45,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction = hyde_prompt
    )
    return model

def get_ai_tutor_response(model, classification_answer):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(classification_answer)
    return response.text

if __name__ == "__main__":
    # Set up the model
    model = setup_hyde()
    
    # Your test question
    test_question = "Logistic regression là gì?"
    
    # Get the AI tutor's response
    response = get_ai_tutor_response(model, test_question)
    
    # Print the question and response
    print("Question:", test_question)
    print("\nAI Tutor's Response:")
    print(response)


