import os
import google.generativeai as genai
import json
from dotenv import load_dotenv
from prompt import intent_prompt

def load_api_key():
    """
    Load API key from the .env file.
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

def create_generation_config():
    """
    Create the generation configuration for the GenerativeModel.
    """
    return {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

def initialize_model(generation_config):
    """
    Initialize the GenerativeModel with the given configuration.
    """
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=intent_prompt,
    )

def load_and_process_json(file_path):
    """
    Load and process the JSON file, then return lesson content.
    """
    lesson_content = []
    with open(file_path, 'r') as file:
        try:
            json_data = json.load(file)
            for lesson_id, lesson_data in json_data.items():
                summary = lesson_data.get("summary")
                lesson_content.append({"id": lesson_id, "summary": summary})
            return lesson_content
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return None

def classify_question(model, question, lesson_content):
    """
    Classify the user's question and return the appropriate response.
    """
    prompt = f"""
    Question: {question}
    Lesson Content: {json.dumps(lesson_content)}
    """

    response = model.generate_content(prompt)
    
    # Extract the JSON part from the response
    response_text = response.text
    try:
        # Find the first '{' and the last '}'
        start = response_text.index('{')
        end = response_text.rindex('}') + 1
        json_str = response_text[start:end]
        
        # Parse the JSON string
        result = json.loads(json_str)
        return result
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response_text}")
        return None

# Main execution
if __name__ == "__main__":
    api_key = load_api_key()
    configure_google_ai(api_key)
    generation_config = create_generation_config()
    model = initialize_model(generation_config)
    file_path = 'output.json'
    lesson_content = load_and_process_json(file_path)

    # Example usage
    question = "logistic regression là gì?"
    result = classify_question(model, question, lesson_content)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Failed to classify the question.")
