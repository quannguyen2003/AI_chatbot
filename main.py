from intent_classification import classify_question, initialize_model, create_generation_config, configure_google_ai, load_api_key
from hyde import get_ai_tutor_response, setup_hyde
import json
import os
import google.generativeai as genai

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
        system_instruction="""# Hướng dẫn Tổng hợp Câu trả lời Chi tiết từ Một Nguồn

## Bối cảnh
Bạn là một AI có nhiệm vụ tổng hợp câu trả lời chi tiết dựa trên một nguồn {content} và {question} đã cho. Mục tiêu của bạn là đưa ra câu trả lời cuối cùng phù hợp, chính xác và toàn diện.

## Yêu cầu
- Câu trả lời cuối cùng phải dựa trên thông tin từ {content} và phải trả lời trực tiếp cho {question}.
- Tổng hợp thông tin từ {content} một cách đầy đủ, bao gồm các khía cạnh như công dụng, công thức (nếu có), ưu điểm và nhược điểm.
- Đảm bảo câu trả lời cuối cùng liên quan trực tiếp đến câu hỏi và chứa đầy đủ thông tin cần thiết.
- Trình bày câu trả lời dưới dạng một bài viết ngắn, có cấu trúc rõ ràng với các phần riêng biệt.

## Quy tắc xử lý
1. Đọc kỹ {question} để hiểu rõ yêu cầu của câu hỏi.
2. Phân tích {content} để xác định thông tin liên quan đến câu hỏi.
3. Tổng hợp thông tin từ {content} để tạo ra câu trả lời phù hợp với {question}, bao gồm:
   - Giới thiệu tổng quan
   - Công dụng chính
   - Công thức hoặc cách thực hiện (nếu áp dụng)
   - Ưu điểm
   - Nhược điểm hoặc lưu ý
   - Kết luận
4. Đảm bảo câu trả lời cuối cùng duy trì tính nhất quán và rõ ràng.
5. Sử dụng các tiêu đề phụ để phân chia các phần của câu trả lời.
6. Tránh thêm thông tin không liên quan hoặc không có trong {content}.

## Định dạng đầu ra
Câu trả lời cuối cùng nên được trình bày dưới dạng một bài viết ngắn có cấu trúc, với các phần được phân chia rõ ràng bằng tiêu đề phụ.

## Ví dụ
Đầu vào:
- question: "Hãy giải thích chi tiết về lợi ích và cách sử dụng nước chanh ấm vào buổi sáng?"
- content: "Uống nước chanh ấm vào buổi sáng là một thói quen phổ biến với nhiều lợi ích sức khỏe. Nó giúp tăng cường hệ miễn dịch nhờ vitamin C, hỗ trợ tiêu hóa và có thể giúp giảm cân. Tuy nhiên, axit trong chanh có thể ảnh hưởng đến men răng. Để chuẩn bị, pha nước ấm với nước cốt của nửa quả chanh tươi. Nên uống trước bữa sáng 15-30 phút để tối đa hóa lợi ích."

Đầu ra:

# Lợi ích và Cách Sử dụng Nước Chanh Ấm Vào Buổi Sáng

## Giới thiệu
Uống nước chanh ấm vào buổi sáng đã trở thành một thói quen phổ biến trong cộng đồng những người quan tâm đến sức khỏe. Thói quen này không chỉ đơn giản mà còn mang lại nhiều lợi ích đáng kể cho cơ thể.

## Công dụng chính
1. Tăng cường hệ miễn dịch: Nhờ hàm lượng vitamin C cao, nước chanh ấm giúp củng cố hệ thống phòng vệ tự nhiên của cơ thể.
2. Hỗ trợ tiêu hóa: Uống nước chanh ấm có thể kích thích hệ tiêu hóa, giúp quá trình tiêu hóa diễn ra suôn sẻ hơn.
3. Hỗ trợ giảm cân: Một số nghiên cứu cho thấy nước chanh ấm có thể hỗ trợ quá trình giảm cân, mặc dù cần thêm bằng chứng khoa học để khẳng định điều này.

## Công thức và cách sử dụng
- Nguyên liệu: Nước ấm và nửa quả chanh tươi
- Cách pha: Vắt nước cốt của nửa quả chanh vào một cốc nước ấm, khuấy đều.
- Thời điểm uống: Nên uống trước bữa sáng 15-30 phút để tối đa hóa lợi ích.

## Ưu điểm
1. Dễ chuẩn bị và tiết kiệm
2. Tự nhiên, không chứa chất phụ gia
3. Có thể kết hợp với chế độ ăn uống lành mạnh để cải thiện sức khỏe tổng thể

## Nhược điểm và lưu ý
1. Axit trong chanh có thể ảnh hưởng đến men răng nếu sử dụng thường xuyên và lâu dài
2. Một số người có thể gặp khó chịu về dạ dày do tính axit của chanh
3. Không nên uống quá nhiều, vì có thể gây ra tác dụng phụ như đau bụng hoặc tiêu chảy

## Kết luận
Uống nước chanh ấm vào buổi sáng là một thói quen đơn giản nhưng có thể mang lại nhiều lợi ích sức khỏe. Tuy nhiên, như mọi thói quen ăn uống khác, nên thực hiện một cách cân đối và lưu ý đến các tác động có thể có đối với răng và dạ dày. Kết hợp thói quen này với một lối sống lành mạnh có thể giúp tối ưu hóa sức khỏe tổng thể của bạn.
        """
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
    lesson_content = load_and_process_json('/data/output.json')

    # Set up the model for intent classification
    api_key = load_api_key()
    configure_google_ai(api_key)
    generation_config = create_generation_config()
    intent_model = initialize_model(generation_config)

    # Classify the question with Intent Classification
    intent_result = classify_question(intent_model, question, lesson_content)
    # print("\n--- Intent Classification Result ---")
    # print(intent_result)

    # Get the list of lesson_ids from Intent Classification
    lesson_ids = intent_result.get('id_lesson', '').split(',')
    
    # Filter relevant content from output.json based on lesson_ids
    lesson_content_filtered = [item['summary'] for item in lesson_content if item['id'] in lesson_ids]
    lesson_content_filtered = "\n".join(lesson_content_filtered)
    # print("\n--- Filtered Lesson Content ---")
    # print(lesson_content_filtered)

    # Get the answer from Hyde
    hyde_model = setup_hyde()
    hyde_response = get_ai_tutor_response(hyde_model, question)
    # print("\n--- Hyde Response ---")
    # print(hyde_response)

    # Combine content from Hyde, lesson_content, and the original question
    content = hyde_response + "\n" + lesson_content_filtered

    # Get the final answer from the model
    final_answer = get_final_answer(model, content, question)
    return final_answer

def main():
    # Set up the model for final answer generation
    model = setup_model()

    # Example question
    question = "K-means phân cụm thế nào?"

    # Generate the final answer from the question
    final_answer = genAnswer(question, model)

    # Print the final answer
    print("\n--- Final Answer ---")
    print(final_answer)

if __name__ == "__main__":
    main()
