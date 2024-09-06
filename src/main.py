from model_loader import setup_model
from intent_classification import classify_question
from hyde import get_ai_tutor_response
from prompt import main_prompt
import json

def load_and_process_json(file_path):
    """
    Load and process the JSON file.
    """
    lesson_content = []
    with open(file_path, 'r', encoding='utf8') as file:
        try:
            json_data = json.load(file)
            for lesson_id, lesson_data in json_data.items():
                summary = lesson_data.get("summary")
                lesson_content.append({"id": lesson_id, "summary": summary})
            return lesson_content
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return None

def get_final_answer(model, content, question):
    """
    Get the final answer by combining content from Hyde and lesson content.
    """
    prompt = f"""
    content: {content}
    question: {question}
    """
    response = model.generate_content(prompt)
    return response.text

def genAnswer(question, model):
    """
    Generate the final answer based on the question.
    """
    # Load lesson content from output.json
    lesson_content = load_and_process_json('../data/output.json')

    # Set up the model for intent classification
    intent_model = setup_model("gemini-1.5-flash", main_prompt)

    # Classify the question with Intent Classification
    intent_result = classify_question(intent_model, question, lesson_content)
    
    # Check if the intent_result is None
    if intent_result is None:
        print("Error: Intent classification returned None.")
        return "Sorry, I couldn't understand your question."

    class_intent = intent_result.get('class', 'study')

    # Handle greeting or toxic responses
    if class_intent == 'greeting':
        return intent_result.get('answer')
    elif class_intent == 'toxic':
        return intent_result.get('answer')

    # For "study" intent, continue with lesson processing
    lesson_ids = intent_result.get('id_lesson', '').split(',')
    
    if not lesson_ids:
        return "It seems like no lessons are directly related to your question. Please try asking about a specific topic."

    # Filter relevant content from output.json based on lesson_ids
    lesson_content_filtered = [item['summary'] for item in lesson_content if item['id'] in lesson_ids]
    lesson_content_filtered = "\n---\n".join(lesson_content_filtered)

    # Get the answer from Hyde
    hyde_model = setup_model("gemini-1.5-flash", main_prompt)
    hyde_response = get_ai_tutor_response(hyde_model, question)

    # Combine content from Hyde, lesson_content, and the original question
    content = hyde_response + "\n---\n" + lesson_content_filtered

    # Get the final answer from the model
    final_answer = get_final_answer(model, content, question)
    return final_answer




def main():
    """
    Main execution function.
    """
    model = setup_model("gemini-1.5-flash", main_prompt)

    # Example question
    question = "Viết code KNN bằng for loop trong Python?"

    # Generate the final answer from the question
    final_answer = genAnswer(question, model)

    # Print the final answer
    print("\n--- Final Answer ---")
    print(final_answer)

if __name__ == "__main__":
    main()
