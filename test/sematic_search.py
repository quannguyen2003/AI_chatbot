import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the model for semantic search
semantic_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Example mapping of lesson descriptions to lesson IDs
lessons = {
    105: "Introduction to K-Nearest Neighbors (KNN) algorithm",
    106: "Advanced techniques in KNN including distance metrics",
    107: "Introduction to logistic regression and its applications",
    108: "Advanced logistic regression: regularization and optimization",
    109: "Support Vector Machine (SVM) fundamentals",
    110: "Advanced SVM techniques and kernel methods",
    # Add more lessons as needed
}

def find_lessons_semantic_search(user_message):
    # Encode the user message and all lesson descriptions
    user_embedding = semantic_model.encode(user_message)
    lesson_embeddings = semantic_model.encode(list(lessons.values()))

    # Calculate cosine similarity between user message and lesson descriptions
    similarities = util.cos_sim(user_embedding, lesson_embeddings)[0].cpu().numpy()
    
    # Find the top 2 most similar lessons
    top_indices = np.argsort(similarities)[-2:][::-1]
    top_lessons = [(list(lessons.keys())[i], similarities[i]) for i in top_indices]

    return top_lessons

def setup_classification(api_key, user_message):
    
    # Configure the API key
    genai.configure(api_key=api_key)
  
    # Define the generation configuration
    generation_config = {
        "temperature": 0.45,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    # Create the GenerativeModel
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="""
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
        """
    )

    # Start a chat session
    chat_session = model.start_chat(history=[])

    # Send a message and get the response
    response = chat_session.send_message(user_message)

    # Extract the text from the response object
    response_text = response.text  # Assuming 'response.text' or similar attribute contains the actual content

    # Parse the response as JSON
    try:
        response_data = json.loads(response_text)

        # If the classification is "study", find relevant lessons using semantic search
        if response_data.get("class") == "study":
            lessons_found = find_lessons_semantic_search(user_message)
            if lessons_found:
                related_lessons = [{"id_bài_học": lesson_id, "name": lessons[lesson_id]} for lesson_id, _ in lessons_found]
                response_data["response"] = f"Dựa trên câu hỏi của bạn, tôi đề xuất hai bài học sau:\nles1: {related_lessons[0]['name']}\nles2: {related_lessons[1]['name']}"
                response_data["lessons"] = related_lessons

        return response_data
    except json.JSONDecodeError:
        return {"class": "error", "answer": "Could not parse response from AI model."}

# Usage example:
user_message = "Can you help me with KNN?"
result = setup_classification(api_key, user_message)
print(json.dumps(result, ensure_ascii=False, indent=2))
