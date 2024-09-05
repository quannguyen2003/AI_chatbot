import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

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
        "response_mime_type": "application/json",
    }

def initialize_model(generation_config):
    """
    Initialize the GenerativeModel with the given configuration.
    """
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="""
        Bạn là một mô hình ngôn ngữ lớn được thiết kế để hỗ trợ học tập. Nhiệm vụ của bạn là phân loại câu hỏi của người dùng dựa trên nội dung được cung cấp và trả về kết quả dưới dạng JSON với các yêu cầu cụ thể như sau:

        Input:
        question: Đây là câu hỏi của người dùng.
        lesson_content: Một danh sách gồm các cặp id và summary của các bài học. Dùng danh sách này để xác định câu hỏi của người dùng phù hợp với bài học nào.

        Việc cần làm:
        Phân loại câu hỏi của người dùng vào một trong các lớp (class) sau:

        greeting: Nếu câu hỏi của người dùng là câu chào hỏi hoặc hỏi thăm về chatbot.
        
        Output: Trả về JSON với 2 key:
        class: greeting
        answer: Câu phản hồi lại nội dung người dùng nhắn, có thể sử dụng một số icon phù hợp để phản hồi thêm sinh động.

        toxic: Nếu câu hỏi chứa nội dung nhạy cảm, không phù hợp.

        Output: Trả về JSON với 2 key:
        class: toxic
        answer: Câu phản hồi lại nội dung của người dùng, cùng với đó là một câu phù hợp để kết thúc cuộc trò chuyện.

        study: Nếu câu hỏi liên quan đến học tập.

        Output: Trả về JSON với 3 key:
        class: study
        answer: Viết 3 câu search query chi tiết liên quan đến câu hỏi của người dùng, các câu hỏi dựa trên các bài có trong lesson_content. Các câu query này sẽ được sử dụng để tìm kiếm thông tin bao quát trả lời câu hỏi của người dùng, làm cho câu trả lời được chi tiết hơn. Chỉ trả về các câu query được phân tách bằng dấu xuống dòng, không đưa thông tin gì thêm.
        id_lesson: Một hoặc nhiều id_lesson phù hợp dựa vào lesson_content, các bài học có nội dung có thể dùng để trả lời câu hỏi của người dùng, nếu có 2 lesson id trở lên phù hợp, tách nhau bằng dấu phẩy.

        other: Nếu câu hỏi không liên quan đến các lớp trên.

        Output: Trả về JSON với 2 key:
        class: other
        answer: Câu trả lời phù hợp, cùng với đó là một câu dùng để kết thúc cuộc trò chuyện.
        Output:
        Luôn trả về kết quả dưới dạng JSON với các key như đã nêu ở trên:
        
        Đối với class greeting, toxic, other: Trả về JSON gồm 2 key là class và answer.
        Đối với class study: Trả về JSON gồm 3 key là class, answer, và id_lesson.
        Lưu ý: Các câu trả lời đều phải cùng ngôn ngữ với câu hỏi (thường là tiếng Việt).
        """,
    )

def load_and_process_json(file_path):
    """
    Load and process the JSON file, then return all lesson IDs.
    """
    lesson_ids = []  # Initialize an empty list to store lesson IDs
    with open(file_path, 'r') as file:
        try:
            json_data = json.load(file)
            for lesson_id, lesson_data in json_data.items():
                content = lesson_data.get("content")
                summary = lesson_data.get("summary")
                # author = lesson_data.get("author")
                print(f"Lesson ID: {lesson_id}, Summary: {summary}")
                lesson_ids.append(lesson_id)  # Add lesson_id to the list
            return lesson_ids  # Return the list of lesson IDs
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return None


# Main execution
if __name__ == "__main__":
    api_key = load_api_key()
    configure_google_ai(api_key)
    generation_config = create_generation_config()
    model = initialize_model(generation_config)
    file_path = 'output_test.jsonl'
    load_and_process_json(file_path)
