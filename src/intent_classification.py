from model_loader import setup_model
import json
from prompt import intent_prompt

def load_and_process_json(file_path):
    """
    Load and process the JSON file, then return lesson content as a formatted string.
    """
    lesson_content = ""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            json_data = json.load(file)
            # print(json_data)
            for lesson in json_data:
                lesson_id = lesson.get("id")
                summary = lesson.get("summary")
                if lesson_id and summary:
                    lesson_content += f"{lesson_id} - {summary}\n"
            print(lesson_content)
            return lesson_content
        
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return None


def classify_question(model, questions, lesson_content):
    """
    Classify the user's question and return the appropriate response.
    """
    # Use the formatted string of lesson content
    lesson_content_str = lesson_content
    
    # Format the question history (excluding the last question)
    q_his = [f'{i+1}. {q}' for i, q in enumerate(questions[:-1])]

    # Construct the prompt with the question history and the current question
    prompt = """
    Lesson Content: {lesson_content_str}

    ### Question history:
    {question_history}

    ### Current question:
    {current_question}

    Please classify the question and return the answer in the following JSON format:
    {{
        "class": "<classification>",
        "id_lesson": "<relevant_lesson_ids>",
        "answer": "<the appropriate answer if greeting or toxic>"
    }}
    """.format(
        lesson_content_str=lesson_content_str,
        question_history='\n'.join(q_his),
        current_question=questions[-1]
    )
    
    print(f"Prompt: {prompt}")

    # Generate content using the model
    response = model.generate_content(prompt)
    response_text = response.text

    # Try to extract JSON response if possible
    try:
        start = response_text.index('{')
        end = response_text.rindex('}') + 1
        json_str = response_text[start:end]
        result = json.loads(json_str)
        return result
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response_text}")
        return None



# Main execution
if __name__ == "__main__":
    model = setup_model("gemini-1.5-flash", intent_prompt)
    file_path = '../data/output.json'
    lesson_content = load_and_process_json(file_path)
    print(lesson_content)

    if lesson_content:
        # Example usage with multiple questions (including history)
        questions = [
            "KNN là gì?",
            "KNN là gì?",
            "KNN là gì?"  # Current question
        ]
        result = classify_question(model, questions, lesson_content)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("Failed to classify the question.")
    else:
        print("Failed to load lesson content.")


# import os
# import google.generativeai as genai
# import json
# from dotenv import load_dotenv

# def load_api_key():
#     """
#     Load API key from the .env file.
#     """
#     load_dotenv()
#     api_key = os.getenv("GEMINI_API_KEY")
    
#     if not api_key:
#         raise ValueError("API key not found. Make sure it is set in the .env file.")
    
#     return api_key

# def configure_google_ai(api_key):
#     """
#     Configure the Google AI SDK with the loaded API key.
#     """
#     genai.configure(api_key=api_key)

# def create_generation_config():
#     """
#     Create the generation configuration for the GenerativeModel.
#     """
#     return {
#         "temperature": 1,
#         "top_p": 0.95,
#         "top_k": 64,
#         "max_output_tokens": 8192,
#     }

# def initialize_model(generation_config):
#     """
#     Initialize the GenerativeModel with the given configuration.
#     """
#     return genai.GenerativeModel(
#         model_name="gemini-1.5-flash",
#         generation_config=generation_config,
#         system_instruction="""
#         Bạn là một mô hình ngôn ngữ lớn được thiết kế để hỗ trợ học tập. Nhiệm vụ của bạn là phân loại câu hỏi của người dùng dựa trên nội dung được cung cấp và trả về kết quả dưới dạng JSON với các yêu cầu cụ thể như sau:

#         Input:
#         question: Đây là câu hỏi của người dùng.
#         lesson_content: Một danh sách gồm các cặp id và summary của các bài học. Dùng danh sách này để xác định câu hỏi của người dùng phù hợp với bài học nào.

#         Việc cần làm:
#         Phân loại câu hỏi của người dùng vào một trong các lớp (class) sau:

#         greeting: Nếu câu hỏi của người dùng là câu chào hỏi hoặc hỏi thăm về chatbot.
        
#         Output: Trả về JSON với 2 key:
#         class: greeting
#         answer: Câu phản hồi lại nội dung người dùng nhắn, có thể sử dụng một số icon phù hợp để phản hồi thêm sinh động.

#         toxic: Nếu câu hỏi chứa nội dung nhạy cảm, không phù hợp.

#         Output: Trả về JSON với 2 key:
#         class: toxic
#         answer: Câu phản hồi lại nội dung của người dùng, cùng với đó là một câu phù hợp để kết thúc cuộc trò chuyện.

#         study: Nếu câu hỏi liên quan đến học tập.

#         Output: Trả về JSON với 3 key:
#         class: study
#         answer: Viết 3 câu search query chi tiết liên quan đến câu hỏi của người dùng, các câu hỏi dựa trên các bài có trong lesson_content. Các câu query này sẽ được sử dụng để tìm kiếm thông tin bao quát trả lời câu hỏi của người dùng, làm cho câu trả lời được chi tiết hơn. Chỉ trả về các câu query được phân tách bằng dấu xuống dòng, không đưa thông tin gì thêm.
#         id_lesson: Một hoặc nhiều id_lesson phù hợp dựa vào lesson_content, các bài học có nội dung có thể dùng để trả lời câu hỏi của người dùng, nếu có 2 lesson id trở lên phù hợp, tách nhau bằng dấu phẩy.

#         other: Nếu câu hỏi không liên quan đến các lớp trên.

#         Output: Trả về JSON với 2 key:
#         class: other
#         answer: Câu trả lời phù hợp, cùng với đó là một câu dùng để kết thúc cuộc trò chuyện.
#         Output:
#         Luôn trả về kết quả dưới dạng JSON với các key như đã nêu ở trên:
        
#         Đối với class greeting, toxic, other: Trả về JSON gồm 2 key là class và answer.
#         Đối với class study: Trả về JSON gồm 3 key là class, answer, và id_lesson.
#         Lưu ý: Các câu trả lời đều phải cùng ngôn ngữ với câu hỏi (thường là tiếng Việt).
#         """,
#     )

# def load_and_process_json(file_path):
#     """
#     Load and process the JSON file, then return lesson content.
#     """
#     lesson_content = []
#     with open(file_path, 'r') as file:
#         try:
#             json_data = json.load(file)
#             for lesson_id, lesson_data in json_data.items():
#                 summary = lesson_data.get("summary")
#                 lesson_content.append({"id": lesson_id, "summary": summary})
#             return lesson_content
#         except json.JSONDecodeError as e:
#             print(f"JSONDecodeError: {e}")
#             return None

# def classify_question(model, question, lesson_content):
#     """
#     Classify the user's question and return the appropriate response.
#     """
#     prompt = f"""
#     Question: {question}
#     Lesson Content: {json.dumps(lesson_content)}
#     """

#     response = model.generate_content(prompt)
    
#     # Extract the JSON part from the response
#     response_text = response.text
#     try:
#         # Find the first '{' and the last '}'
#         start = response_text.index('{')
#         end = response_text.rindex('}') + 1
#         json_str = response_text[start:end]
        
#         # Parse the JSON string
#         result = json.loads(json_str)
#         return result
#     except (ValueError, json.JSONDecodeError) as e:
#         print(f"Error parsing response: {e}")
#         print(f"Raw response: {response_text}")
#         return None

# # Main execution
# if __name__ == "__main__":
#     api_key = load_api_key()
#     configure_google_ai(api_key)
#     generation_config = create_generation_config()
#     model = initialize_model(generation_config)
#     file_path = '../data/output.json'
#     lesson_content = load_and_process_json(file_path)

#     # Example usage
#     question = "logistic regression là gì?"
#     result = classify_question(model, question, lesson_content)
#     if result:
#         print(json.dumps(result, ensure_ascii=False, indent=2))
#     else:
#         print("Failed to classify the question.")