import json
from model_loader import setup_model
from intent_classification import classify_question
from hyde import get_ai_tutor_response
from prompt import main_prompt
import os

# Global variable for the model
model = None
chat_history_file = 'chat_history.json'


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

def get_final_answer(content, question):
    """
    Get the final answer by combining content from Hyde and lesson content, and leveraging chat history.
    """
    # Start a new chat session with the model
    chat_session = model.start_chat(history=[])

    # Create the full prompt with content and question
    prompt = f"""
    content: {content}
    question: {question}
    """

    # Send the message to the model
    response = chat_session.send_message(prompt)
    
    return response.text

def load_chat_history():
    """
    Load chat history from the chat_history.json file, or return an empty dictionary if the file doesn't exist.
    """
    if os.path.exists(chat_history_file):
        with open(chat_history_file, 'r', encoding='utf8') as file:
            try:
                chat_history = json.load(file)
                return chat_history
            except json.JSONDecodeError as e:
                print(f"Error loading chat history: {e}")
                return {}
    else:
        return {}

def save_chat_history(chat_id, question, response):
    """
    Save the chat history to the chat_history.json file after every interaction.
    """
    chat_history = load_chat_history()
    
    # If this chat ID doesn't exist in the history, create it
    if chat_id not in chat_history:
        chat_history[chat_id] = []
    
    # Append the current question and response to the chat history
    chat_history[chat_id].append({
        'question': question,
        'parts': response
    })

    # Write the updated history back to the file
    with open(chat_history_file, 'w', encoding='utf8') as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=2)

# def genAnswer(question, chat_id):
#     """
#     Generate the final answer based on the question. No need to pass history as it is stored.
#     """

#     # Load lesson content from output.json
#     lesson_content = load_and_process_json('../data/output.json')

#     #Tìm history của chat_id

#     #Sau đó lấy tất cả các question từ history

#     #Nối các question lại với nhau thành một câu hỏi lớn là 1 list

#     #Nếu không có history thì để history = [] + question

#     #Cộng với history hiện tại để trả lời

#     #Sau đó đưa vào hàm intent_result

#     # Classify the question with Intent Classification
#     intent_result = classify_question(model, question, lesson_content)
    
#     # Check if the intent_result is None
#     if intent_result is None:
#         print("Error: Intent classification returned None.")
#         return "Sorry, I couldn't understand your question."

#     class_intent = intent_result.get('class', 'study')

#     # Handle greeting or toxic responses
#     if class_intent == 'greeting':
#         response = intent_result.get('answer')
#         save_chat_history(chat_id, question, response)
#         return response
#     elif class_intent == 'toxic':
#         response = intent_result.get('answer')
#         save_chat_history(chat_id, question, response)
#         return response

#     # For "study" intent, continue with lesson processing
#     lesson_ids = intent_result.get('id_lesson', '').split(',')
    
#     if not lesson_ids:
#         response = "It seems like no lessons are directly related to your question. Please try asking about a specific topic."
#         save_chat_history(chat_id, question, response)
#         return response

#     # Filter relevant content from output.json based on lesson_ids
#     lesson_content_filtered = [item['summary'] for item in lesson_content if item['id'] in lesson_ids]
#     lesson_content_filtered = "\n---\n".join(lesson_content_filtered)

#     # Get the answer from Hyde
#     hyde_response = get_ai_tutor_response(model, question)

#     # Combine content from Hyde, lesson_content, and the original question
#     content = hyde_response + "\n---\n" + lesson_content_filtered

#     # Get the final answer from the model
#     final_answer = get_final_answer(content, question)

#     # Save the interaction to the chat history
#     save_chat_history(chat_id, question, final_answer)
    
#     return final_answer


def genAnswer(question, chat_id):
    """
    Generate the final answer based on the question. No need to pass history as it is stored.
    """

    # Load lesson content from output.json
    lesson_content = load_and_process_json('../data/output.json')

    # Load chat history
    chat_history = load_chat_history()

    # Get history for the current chat_id
    current_chat_history = chat_history.get(chat_id, [])

    # Extract all questions from the history
    history_questions = [item['question'] for item in current_chat_history]

    # Combine history questions with the current question
    all_questions = history_questions + [question]

    # Classify the combined questions with Intent Classification
    intent_result = classify_question(model, all_questions, lesson_content)
    
    # Check if the intent_result is None
    if intent_result is None:
        print("Error: Intent classification returned None.")
        return "Sorry, I couldn't understand your question."

    class_intent = intent_result.get('class', 'study')

    # Handle greeting or toxic responses
    if class_intent == 'greeting':
        response = intent_result.get('answer')
        save_chat_history(chat_id, question, response)
        return response
    elif class_intent == 'toxic':
        response = intent_result.get('answer')
        save_chat_history(chat_id, question, response)
        return response

    # For "study" intent, continue with lesson processing
    lesson_ids = intent_result.get('id_lesson', '').split(',')
    
    if not lesson_ids:
        response = "It seems like no lessons are directly related to your question. Please try asking about a specific topic."
        save_chat_history(chat_id, question, response)
        return response

    # Filter relevant content from output.json based on lesson_ids
    lesson_content_filtered = [item['summary'] for item in lesson_content if item['id'] in lesson_ids]
    lesson_content_filtered = "\n---\n".join(lesson_content_filtered)

    # Get the answer from Hyde
    hyde_response = get_ai_tutor_response(model, question)

    # Combine content from Hyde, lesson_content, and the original question
    content = hyde_response + "\n---\n" + lesson_content_filtered

    # Get the final answer from the model
    final_answer = get_final_answer(content, question)

    # Save the interaction to the chat history
    save_chat_history(chat_id, question, final_answer)
    
    return final_answer


# def genAnswer(question, chat_id):
#     """
#     Generate the final answer based on the question and chat history.
#     """
#     # Load lesson content from output.json
#     lesson_content = load_and_process_json('../data/output.json')

#     # Load chat history
#     chat_history = load_chat_history()

#     # Get history for the current chat_id
#     current_chat_history = chat_history.get(chat_id, [])

#     # Extract all questions from the history
#     history_questions = [item['question'] for item in current_chat_history]

#     # Combine history questions with the current question
#     all_questions = history_questions + [question]

#     # Join all questions into a single string
#     combined_questions = " ".join(all_questions)

#     # Classify the combined questions with Intent Classification
#     intent_result = classify_question(model, combined_questions, lesson_content)
    
#     # Check if the intent_result is None
#     if intent_result is None:
#         print("Error: Intent classification returned None.")
#         return "Sorry, I couldn't understand your question."

#     class_intent = intent_result.get('class', 'study')

#     # Handle greeting or toxic responses
#     if class_intent == 'greeting':
#         response = intent_result.get('answer')
#         save_chat_history(chat_id, question, response)
#         return response
#     elif class_intent == 'toxic':
#         response = intent_result.get('answer')
#         save_chat_history(chat_id, question, response)
#         return response

#     # For "study" intent, continue with lesson processing
#     lesson_ids = intent_result.get('id_lesson', '').split(',')
    
#     if not lesson_ids:
#         response = "It seems like no lessons are directly related to your question. Please try asking about a specific topic."
#         save_chat_history(chat_id, question, response)
#         return response

#     # Filter relevant content from output.json based on lesson_ids
#     lesson_content_filtered = [item['summary'] for item in lesson_content if item['id'] in lesson_ids]
#     lesson_content_filtered = "\n---\n".join(lesson_content_filtered)

#     # Get the answer from Hyde
#     hyde_response = get_ai_tutor_response(model, combined_questions)

#     # Combine content from Hyde, lesson_content, and the original question
#     content = hyde_response + "\n---\n" + lesson_content_filtered

#     # Get the final answer from the model
#     final_answer = get_final_answer(content, question)

#     # Save the interaction to the chat history
#     save_chat_history(chat_id, question, final_answer)
    
#     return final_answer

def main():
    """
    Main execution function.
    """
    global model  # Access the global model variable
    model = setup_model("gemini-1.5-flash", main_prompt)

    # Example question and chat ID (to simulate unique user or conversation session)
    question = "KNN là gì?"
    chat_id = 'user_1111'

    # Generate the final answer from the question
    final_answer = genAnswer(question, chat_id)

    # Print the final answer
    print("\n--- Final Answer ---")
    print(final_answer)

if __name__ == "__main__":
    main()

