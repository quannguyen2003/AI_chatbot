import google.generativeai as genai
import PyPDF2
import os
import re
import json

from PyPDF2 import PdfReader

def read_pdf(file_path):
    """
    Read PDF file and return its content as a string.
    """
    content = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                content += page.extract_text()
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading PDF file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return content

def read_txt(file_path):
    """
    Read TXT file and return its content as a string.
    """
    content = ""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
    return content

def process_content(content, subject, api_key):
    """
    Process content before saving to the database, including generating a summary using the Gemini API.
    """
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": 0.45,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    try:
        prompt = f"""
        Bạn là AI-summarise, một chatbot chuyên tổng hợp nội dung học tập. Nhiệm vụ của bạn là tóm tắt nội dung sau đây:

{content}

Yêu cầu cụ thể:

Đọc và phân tích kỹ nội dung được cung cấp.

Xác định 3 điểm thông tin quan trọng nhất từ nội dung.

Tạo một bản tóm tắt ngắn gọn gồm chính xác 3 câu. Mỗi câu cần:
Chứa một ý chính quan trọng từ nội dung
Được diễn đạt rõ ràng và súc tích
Cung cấp thông tin có giá trị và hữu ích cho người đọc

Đảm bảo 3 câu tóm tắt bao quát được những điểm chính yếu nhất của nội dung, giúp người đọc nắm bắt nhanh chóng trọng tâm.

Trình bày kết quả dưới dạng văn bản thuần túy.

Phản hồi chỉ bao gồm 3 câu tóm tắt trên 1 đoạn, không thêm bất kỳ nội dung nào khác.

Hãy thực hiện nhiệm vụ này một cách chính xác và hiệu quả, đảm bảo bản tóm tắt ngắn gọn nhưng vẫn cung cấp thông tin giá trị cao cho người đọc."""
        response = model.generate_content(prompt)
        print("API Response:", response)  # Print the entire response for debugging
        summary = response.text if response.text else "Summary not available."
    except Exception as e:
        print(f"An error occurred while generating summary: {e}")
        summary = "Summary not available."

    # Extract metadata from content (placeholders for actual extraction logic)
    author = re.search(r'Author:\s*(.*)', content)
    published_date = re.search(r'Date:\s*(.*)', content)

    author = author.group(1) if author else 'Unknown'
    published_date = published_date.group(1) if published_date else 'Unknown'

    status = True

    return {
        'content': content,
        'summary': summary,
        # 'author': author,
        # 'published_date': published_date,
        'status': status
        # 'subject': subject
    }

def save_to_json(data, output_file):
    """
    Save processed content to a JSON file in the specified format.
    """
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
        else:
            json_data = {}

        # Generate a unique key for the new entry
        new_key = f"ML{str(len(json_data) + 1).zfill(3)}"
        json_data[new_key] = {
            'content': data['content'],
            'summary': data['summary'],
            'status': data['status']
            # 'author': data['author'],
            # You can add more fields here if needed
        }

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(json_data, ensure_ascii=False, indent=4))
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")

def main(file_path, subject, api_key, output_file):
    """
    Main function to read, process, and save file content.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    file_extension = os.path.splitext(file_path)[-1].lower()
    content = ""

    if file_extension == '.pdf':
        content = read_pdf(file_path)
    elif file_extension == '.txt':
        content = read_txt(file_path)
    else:
        print(f"Unsupported file type: {file_extension}")
        return

    processed_data = process_content(content, subject, api_key)
    save_to_json(processed_data, output_file)

# Example usage:
if __name__ == "__main__":
    file_path = "/home/sagemaker-user/k_means.txt"  # Change this to your file path
    subject = "Sample Subject"
    api_key = "AIzaSyBqxphO1QKH-A2qV3gCXGBNARRVGvBz8Mc"  # Replace with your actual API key
    output_file = "output.json"  # Output file name

    main(file_path, subject, api_key, output_file)