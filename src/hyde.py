from model_loader import setup_model
from prompt import hyde_prompt

def get_ai_tutor_response(model, classification_answer):
    """
    Get the AI tutor's response to the classification answer.
    """
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(classification_answer)
    return response.text

# Main execution
if __name__ == "__main__":
    model = setup_model("gemini-1.5-flash", hyde_prompt)
    
    # Example question
    test_question = "Logistic regression là gì?"
    
    # Get the AI tutor's response
    response = get_ai_tutor_response(model, test_question)
    
    # Print the question and response
    print("Question:", test_question)
    print("\nAI Tutor's Response:")
    print(response)
