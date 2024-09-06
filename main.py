from intent_classification import classify_question, initialize_model, create_generation_config, configure_google_ai, load_api_key
from hyde import get_ai_tutor_response, setup_hyde
import json
import os
import google.generativeai as genai
from prompt import *

def load_and_process_json(file_path):
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
            
def setup_model():
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
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=main_prompt
    )

def get_final_answer(model, content, question):
    prompt = f"""
    content: {content}
    question: {question}
    """
    response = model.generate_content(prompt)
    return response.text

def genAnswer(question, model):
    # Load lesson content from output.json
    lesson_content = load_and_process_json('output.json')

    # Set up the model for intent classification
    api_key = load_api_key()
    configure_google_ai(api_key)
    generation_config = create_generation_config()
    intent_model = initialize_model(generation_config)

    # Classify the question with Intent Classification
    intent_result = classify_question(intent_model, question, lesson_content)
    # print(type(intent_result))
    # print("\n--- Intent Classification Result ---")
    # print(intent_result)
    
    class_intent = intent_result.get('class', 'study')
    if class_intent == 'toxic' or class_intent == 'greeting':
        return intent_result.get('answer')
    


    # Get the list of lesson_ids from Intent Classification
    lesson_ids = intent_result.get('id_lesson', '').split(',')
    
    # Filter relevant content from output.json based on lesson_ids
    lesson_content_filtered = [item['summary'] for item in lesson_content if item['id'] in lesson_ids]
    lesson_content_filtered = "\n---\n".join(lesson_content_filtered)
    # print("\n--- Filtered Lesson Content ---")
    # print(lesson_content_filtered)

    # Get the answer from Hyde
    hyde_model = setup_hyde()
    hyde_response = get_ai_tutor_response(hyde_model, question)
    # print("\n--- Hyde Response ---")
    # print(hyde_response)

    # Combine content from Hyde, lesson_content, and the original question
    content = hyde_response + "\n---\n" + lesson_content_filtered

    # Get the final answer from the model
    final_answer = get_final_answer(model, content, question)
    return final_answer

def main():
    # Set up the model for final answer generation
    model = setup_model()

    # Example question
    question = "chào"

    # Generate the final answer from the question
    final_answer = genAnswer(question, model)

    # Print the final answer
    print("\n--- Final Answer ---")
    print(final_answer)

if __name__ == "__main__":
    main()

