# model_loader.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

def load_api_key():
    """
    Load the API key from the .env file.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API key not found. Make sure it is set in the .env file.")
    
    return api_key

def configure_google_ai(api_key):
    """
    Configure the Google AI SDK with the loaded API key.
    """
    genai.configure(api_key=api_key)

def create_generation_config(temperature=0.45, top_p=0.95, top_k=64, max_output_tokens=8192):
    """
    Create the generation configuration for the GenerativeModel.
    """
    return {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
    }

def initialize_model(generation_config, model_name="gemini-1.5-flash", system_instruction=None):
    """
    Initialize the GenerativeModel with the given configuration and model name.
    """
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=system_instruction,
    )

def setup_model(model_name, system_instruction, temperature=0.45, top_p=0.95, top_k=64, max_output_tokens=8192):
    """
    Complete setup function to load API key, configure the model, and return the initialized model.
    """
    api_key = load_api_key()
    configure_google_ai(api_key)
    generation_config = create_generation_config(temperature, top_p, top_k, max_output_tokens)
    return initialize_model(generation_config, model_name, system_instruction)
