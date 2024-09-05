import os
import google.generativeai as genai

# Configure the API key from the environment variable
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

# Create the model with the given configuration and system instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Bạn là một mô hình ngôn ngữ lớn được thiết kế để hỗ trợ học tập. Nhiệm vụ của bạn là phân loại câu hỏi của người dùng dựa trên nội dung được cung cấp và trả về kết quả dưới dạng JSON với các yêu cầu cụ thể như sau:\n\n"
        "Input:\nquestion: Đây là câu hỏi của người dùng.\nlesson_content: Một danh sách gồm các cặp id và summary của các bài học. Dùng danh sách này để xác định câu hỏi của người dùng phù hợp với bài học nào.\n"
        "Việc cần làm:\nPhân loại câu hỏi của người dùng vào một trong các lớp (class) sau:\n\n"
        "greeting: Nếu câu hỏi của người dùng là câu chào hỏi hoặc hỏi thăm về chatbot.\n\n"
        "Output: Trả về JSON với 2 key:\nclass: greeting\nanswer: Câu phản hồi lại nội dung người dùng nhắn, có thể sử dụng một số icon phù hợp để phản hồi thêm sinh động.\n"
        "toxic: Nếu câu hỏi chứa nội dung nhạy cảm, không phù hợp.\n\n"
        "Output: Trả về JSON với 2 key:\nclass: toxic\nanswer: Câu phản hồi lại nội dung của người dùng, cùng với đó là một câu phù hợp để kết thúc cuộc trò chuyện.\n"
        "study: Nếu câu hỏi liên quan đến học tập.\n\n"
        "Output: Trả về JSON với 3 key:\nclass: study\nanswer: Viết 3 câu search query chi tiết liên quan đến câu hỏi của người dùng, các câu hỏi dựa trên các bài có trong lesson_content. Các câu query này sẽ được sử dụng để tìm kiếm thông tin bao quát trả lời câu hỏi của người dùng, làm cho câu trả lời được chi tiết hơn. Chỉ trả về các câu query được phân tách bằng dấu xuống dòng, không đưa thông tin gì thêm.\n"
        "id_lesson: Một hoặc nhiều id_lesson phù hợp dựa vào lesson_content, các bài học có nội dung có thể dùng để trả lời câu hỏi của người dùng, nếu có 2 lesson id trở lên phù hợp, tách nhau bằng dấu phẩy.\n"
        "other: Nếu câu hỏi không liên quan đến các lớp trên.\n\n"
        "Output: Trả về JSON với 2 key:\nclass: other\nanswer: Câu trả lời phù hợp, cùng với đó là một câu dùng để kết thúc cuộc trò chuyện.\n\n"
        "Output:\nLuôn trả về kết quả dưới dạng JSON với các key như đã nêu ở trên:\n\n"
        "Đối với class greeting, toxic, other: Trả về JSON gồm 2 key là class và answer.\nĐối với class study: Trả về JSON gồm 3 key là class, answer, và id_lesson.\n"
        "Lưu ý: Các câu trả lời đều phải cùng ngôn ngữ với câu hỏi (thường là tiếng Việt)."
    ),
)

# Start a chat session with the initial history
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "lesson_content: {\n\"ML001\": \"Intro. to Machine learning\",\n\"ML002\": \"Linear regression\",\n\"ML003\": \"Logistic Regression\",\n\"ML004\": \"What is K-Mean\"\n}\n\nquestion: \"Tôi muốn tìm hiểu về machine learning và bài toán phân loại\"",
            ],
        },
        {
            "role": "model",
            "parts": [
                "{\"class\": \"study\", \"answer\": \"Machine learning và bài toán phân loại là gì?\\nMachine learning là gì, các bài toán phân loại thường gặp trong Machine Learning\\nCác kỹ thuật phân loại trong Machine Learning\", \"id_lesson\": \"ML001,ML003\"}"
            ],
        },
    ]
)

# Replace 'INSERT_INPUT_HERE' with your actual input
response = chat_session.send_message(
    "Tôi muốn biết về phương pháp phân cụm K-Mean."
)

# Print the response
print(response.text)
