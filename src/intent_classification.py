from model_loader import setup_model
import json
from prompt import intent_prompt

def load_and_process_json(file_path):
    """
    Load and process the JSON file, then return lesson content.
    """
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

def classify_question(model, question, lesson_content):
    """
    Classify the user's question and return the appropriate response.
    """
    prompt = f"""
    Question: {question}
    Lesson Content: {json.dumps(lesson_content)}

    Please classify the question and return the answer in the following JSON format:
    {{
        "class": "<classification>",
        "id_lesson": "<relevant_lesson_ids>",
        "answer": "<the appropriate answer if greeting or toxic>"
    }}
    """

    response = model.generate_content(prompt)
    response_text = response.text

    # Print the raw response for debugging
    # print(f"Raw response: {response_text}")

    # Try to extract JSON response if possible
    try:
        # Attempt to find the first '{' and last '}'
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
    file_path = 'output.json'
    lesson_content = load_and_process_json(file_path)

    # Example usage
    question = "logistic regression là gì?"
    result = classify_question(model, question, lesson_content)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Failed to classify the question.")
