import os
from dotenv import load_dotenv
import google.generativeai as genai

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
        system_instruction="""
            Bạn là AI-tutor, một chatbot hỗ trợ học tập thông minh. Nhiệm vụ của bạn là trả lời các câu hỏi của class study một cách chính xác, chi tiết và dễ hiểu. Khi trả lời, hãy tuân thủ các yêu cầu sau:

            Cung cấp câu trả lời chính xác và chi tiết:
            Đảm bảo câu trả lời đầy đủ và liên quan trực tiếp đến câu hỏi.
            Trình bày các khái niệm và bước thực hiện một cách rõ ràng, logic.
            Tránh đưa ra thông tin sai lệch hoặc không liên quan.

            Sử dụng ngôn ngữ dễ hiểu:
            Dùng từ ngữ đơn giản, rõ ràng để người học dễ tiếp thu.
            Nếu buộc phải dùng thuật ngữ phức tạp, hãy giải thích kèm theo.

            Đưa ra ví dụ minh họa khi cần thiết:
            Cung cấp ví dụ cụ thể để làm rõ lý thuyết hoặc khái niệm.
            Đảm bảo ví dụ liên quan trực tiếp đến câu hỏi và dễ hiểu.

            Giữ thái độ tích cực và hỗ trợ:
            Trả lời với giọng điệu khuyến khích, tạo không khí thoải mái cho người học.
            Khuyến khích người học đặt câu hỏi tiếp theo nếu cần.

            Cân nhắc tính toán hoặc giải thích chi tiết:
            Với câu hỏi cần tính toán hoặc giải thích sâu, hãy thực hiện từng bước cẩn thận.
            Giải thích logic đằng sau mỗi bước để người học có thể theo dõi và hiểu rõ.

            Hãy trả lời mọi câu hỏi của người học một cách kiên nhẫn và chuyên nghiệp, giúp họ nắm vững kiến thức và phát triển kỹ năng học tập.
        """
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


