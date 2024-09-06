import json
import os

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)

def load_lessons(file_path):
    """Load lessons from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_lessons(lessons, file_path):
    """Save lessons to a JSON file with proper formatting."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(lessons, file, ensure_ascii=False, indent=2, cls=CustomJSONEncoder)

def delete_lesson(file_path, lesson_id_to_delete):
    """Delete a lesson based on its ID."""
    # Load existing lessons
    lessons = load_lessons(file_path)
    
    # Check if the lesson exists
    if lesson_id_to_delete in lessons:
        # Remove the lesson
        # deleted_lesson = lessons.pop(lesson_id_to_delete)

        lessons[lesson_id_to_delete]['status'] = False
        
        # Save the updated lessons
        save_lessons(lessons, file_path)
        
        print(f"Lesson with ID {lesson_id_to_delete} has been deleted.")
        # print(f"Deleted lesson details: {deleted_lesson}")
        return True
    else:
        print(f"No lesson found with ID {lesson_id_to_delete}")
        return False

# Example usage
if __name__ == "__main__":
    file_path = 'output.json'  # Make sure this path is correct
    lesson_id_to_delete = "ML004"  # Replace with the actual ID you want to delete
    delete_lesson(file_path, lesson_id_to_delete)
