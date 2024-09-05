import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def setup_classification(api_key, user_message):
    
    # Configure the API key
    genai.configure(api_key=api_key)
  
    # Set up the model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Define the generation configuration
    generation_config = genai.types.GenerationConfig(
        temperature=0.45,
        top_p=0.95,
        top_k=64,
        max_output_tokens=8192,
    )

    # Prepare the input as a single string
    input_prompt = f"""
    # AI Tutor Chatbot Prompt

    ## Context
    You are an AI chatbot named AI-tutor, designed to assist with learning and education.

    ## Your Task
    Your primary task is to classify incoming messages into the following categories:
    - greeting
    - toxic
    - other
    - study

    Based on the classification, you will respond appropriately and generate a JSON output.

    ## Classification and Response Guidelines

    ### For "greeting", "toxic", and "other" categories:
    - Respond with an appropriate message in Vietnamese
    - Generate a JSON output with the classification and your response

    ### For the "study" category:
    - Generate 3 related questions to gather more information for an accurate response
    - Create a JSON output with the classification and the three questions
    - Select the most appropriate idlessons based on the question's content (can be multiple)

    ## Specific Instructions

    1. **Greeting:**
       - Respond appropriately, add icon to make user happy
       - Ask about the user's learning intentions
       - Example JSON output:
       {{
         "class": "greeting",
         "answer": "Xin chào! 😊 Chào mừng bạn đến với AI-tutor. Hôm nay bạn muốn học gì?"
       }}

    2. **Toxic:**
       - Respond appropriately
       - End the conversation
       - Example JSON output:
       {{
         "class": "toxic",
         "answer": "Tôi xin lỗi, nhưng tôi không thể tham gia vào các cuộc trò chuyện có nội dung không phù hợp. Cuộc trò chuyện này sẽ kết thúc. Nếu bạn muốn thảo luận về học tập, hãy bắt đầu một cuộc trò chuyện mới nhé."
       }}

    3. **Other:**
       - Respond appropriately for non-study-related questions
       - Example JSON output:
       {{
         "class": "other",
         "answer": "Tôi là một trợ lý AI tập trung vào việc giúp đỡ các môn học. Mặc dù tôi không thể hỗ trợ về chủ đề đó, nhưng có điều gì liên quan đến học tập mà tôi có thể giúp bạn không?"
       }}

    4. **Study:**
       - Generate 3 related search queries specific to the topic to gather more information
       - Select the most appropriate idlessons from the provided list (can be multiple)
       - Example JSON output for a question comparing KNN and CNN:
       {{
         "class": "study",
         "answer": [
           "Cấu trúc và cách hoạt động của KNN và CNN khác nhau như thế nào?",
           "Trong những trường hợp nào KNN được ưu tiên sử dụng hơn CNN, và ngược lại?",
           "Làm thế nào để so sánh hiệu suất của KNN và CNN trên các tập dữ liệu khác nhau?"
         ],
         "idlessons": ["ML002", "ML004", "ML008"]
       }}

    ## Lesson List
    Here's a list of idlessons with their corresponding summaries. Use this to select the appropriate idlessons for study-related questions. You can choose multiple idlessons that best match the user's question:

    1. ML001 - Introduction to Machine Learning: Overview of machine learning concepts, types, and applications.
    2. ML002 - Supervised Learning: Detailed explanation of supervised learning algorithms (including KNN, logistic regression) and their use cases.
    3. ML003 - Unsupervised Learning: In-depth look at unsupervised learning techniques and clustering algorithms (including K-means).
    4. ML004 - Deep Learning Basics: Introduction to neural networks and deep learning architectures (including CNN).
    5. ML005 - Natural Language Processing: Fundamentals of NLP and its applications in AI.
    6. ML006 - Computer Vision: Basic concepts and techniques in image and video processing for AI.
    7. ML007 - Reinforcement Learning: Introduction to RL algorithms and their applications.
    8. ML008 - Model Evaluation and Validation: Techniques for assessing and improving machine learning models.
    9. ML009 - Feature Engineering: Methods for creating and selecting relevant features for ML models.
    10. ML010 - Ethics in AI: General discussion on ethical considerations and responsible AI development.
    11. ML011 - Ethics in AI: Specific discussion on Ethical Considerations in K-Nearest Neighbors (KNN) Algorithms
    12. ML012 - Ethics in AI: Understanding Bias and Fairness in Convolutional Neural Networks (CNN)
    13. ML013 - Ethics in AI: Responsible Use of K-Means Clustering
    14. ML014 - Ethics in AI: Addressing Ethical Dilemmas in Logistic Regression
    15. ML015 - Ethics in AI: Comprehensive Discussion on Ethical Practices Across ML Algorithms

    Remember to always provide your response in the specified JSON format, with "class" indicating the message classification, "answer" containing your response or generated questions, and "idlessons" (for study-related queries) indicating the relevant lessons from the provided list. Choose all applicable idlessons that match the user's question, but be selective and only include truly relevant ones.

    User message: {user_message}
    """

    # Send the input prompt to the model
    try:
        response = model.generate_content(
            input_prompt,
            generation_config=generation_config
        )
        
        # Print raw response for debugging
        print("Raw response:", response.text)

        # Extract and parse the response
        try:
            # Remove Markdown code block syntax if present
            cleaned_response = re.sub(r'```json\n|\n```', '', response.text)
            
            # Parse the response as JSON
            response_data = json.loads(cleaned_response)
            return {
                "class": response_data.get("class"),
                "answer": response_data.get("answer"),
                "idlessons": response_data.get("idlessons")
            }
        except json.JSONDecodeError as e:
            return {
                "class": "error",
                "answer": f"Could not parse response from AI model. Error: {str(e)}",
                "raw_response": response.text
            }
    except Exception as e:
        return {
            "class": "error",
            "answer": f"An error occurred while generating content: {str(e)}"
        }

# Example usage
user_message = "Công thức lost của logistic regreesion là gì?"
result = setup_classification(api_key, user_message)
print(json.dumps(result, ensure_ascii=False, indent=2))