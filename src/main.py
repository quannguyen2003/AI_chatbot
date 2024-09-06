from model_loader import setup_model
from intent_classification import classify_question
from hyde import get_ai_tutor_response
from prompt import main_prompt
import json

# Global variable for the model
model = None

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

def get_final_answer(content, question, history):
    """
    Get the final answer by combining content from Hyde and lesson content, and leveraging chat history.
    """
    # Start a new chat session with the model
    chat_session = model.start_chat(history=history)

    # Create the full prompt with content and question
    prompt = f"""
    content: {content}
    question: {question}
    """

    # Send the message to the model
    response = chat_session.send_message(prompt)
    
    return response.text

def genAnswer(question, history):
    """
    Generate the final answer based on the question and history.
    """

    # Load lesson content from output.json
    lesson_content = load_and_process_json('../data/output.json')

    # Classify the question with Intent Classification
    intent_result = classify_question(model, question, lesson_content)
    
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
    hyde_response = get_ai_tutor_response(model, question)

    # Combine content from Hyde, lesson_content, and the original question
    content = hyde_response + "\n---\n" + lesson_content_filtered

    # Get the final answer from the model using history
    final_answer = get_final_answer(content, question, history)
    return final_answer

def main():
    """
    Main execution function.
    """
    global model  # Access the global model variable
    model = setup_model("gemini-1.5-flash", main_prompt)

    # Example question and history
    question = "Viết code KNN bằng for loop trong Python?"
    history = [
        {
      "role": "user",
      "parts": [
        "cho tôi trắc nghiệm về KNN",
      ],
    },
    {
      "role": "model",
      "parts": [
        "## Trắc nghiệm về KNN (K-Nearest Neighbors)\n\n**Hãy chọn đáp án đúng cho mỗi câu hỏi:**\n\n**1. KNN là gì?**\n\na) Một thuật toán phân loại tuyến tính.\nb) Một thuật toán phân cụm.\nc) Một thuật toán phân loại dựa trên khoảng cách.\nd) Một thuật toán hồi quy tuyến tính.\n\n**2. K trong KNN đại diện cho gì?**\n\na) Số lượng thuộc tính của dữ liệu.\nb) Số lượng điểm dữ liệu trong tập huấn luyện.\nc) Số lượng điểm láng giềng gần nhất được sử dụng để dự đoán.\nd) Số lượng lớp trong tập dữ liệu.\n\n**3. KNN sử dụng loại khoảng cách nào để xác định điểm láng giềng gần nhất?**\n\na) Khoảng cách Manhattan.\nb) Khoảng cách Euclidean.\nc) Khoảng cách Minkowski.\nd) Tất cả các phương án trên.\n\n**4. Ưu điểm của KNN là gì?**\n\na) Dễ dàng triển khai và hiểu.\nb) Hiệu quả với dữ liệu có chiều cao.\nc) Không cần huấn luyện mô hình.\nd) Tất cả các phương án trên.\n\n**5. Nhược điểm của KNN là gì?**\n\na) Hiệu suất thấp với tập dữ liệu lớn.\nb) Nhạy cảm với dữ liệu ồn.\nc) Khó xác định giá trị K tối ưu.\nd) Tất cả các phương án trên.\n\n**6. KNN có thể được sử dụng cho các bài toán nào?**\n\na) Phân loại.\nb) Hồi quy.\nc) Phân cụm.\nd) Cả a và b.\n\n**7. Trong KNN, điểm dữ liệu mới được phân loại dựa trên:**\n\na) Lớp của điểm láng giềng gần nhất.\nb) Lớp của đa số điểm láng giềng gần nhất.\nc) Khoảng cách đến điểm láng giềng gần nhất.\nd) Cả a và b.\n\n**8. KNN là một thuật toán:**\n\na) Có giám sát.\nb) Không có giám sát.\nc) Cả hai.\nd) Không có phương án nào đúng.\n\n**9. Giá trị K càng lớn, thì:**\n\na) Mô hình càng phức tạp.\nb) Mô hình càng đơn giản.\nc) Độ chính xác của mô hình càng cao.\nd) Độ chính xác của mô hình càng thấp.\n\n**10. KNN có thể được sử dụng để:**\n\na) Phân loại hình ảnh.\nb) Dự đoán giá nhà.\nc) Phân tích cảm xúc.\nd) Tất cả các phương án trên.\n\n**Đáp án:**\n\n1. c)\n2. c)\n3. d)\n4. d)\n5. d)\n6. d)\n7. b)\n8. a)\n9. b)\n10. d) \n",
      ],
    }
    ]

    # Generate the final answer from the question
    final_answer = genAnswer(question, history)

    # Print the final answer
    print("\n--- Final Answer ---")
    print(final_answer)

if __name__ == "__main__":
    main()
