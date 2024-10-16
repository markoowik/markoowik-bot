import json


def validate_json(filename):
    try:
        with open(filename, "r") as file:
            questions = json.load(file)

        with open(filename, "w") as file:
            json.dump(questions, file, indent=4)

        print("JSON file has been validated and cleaned.")
    except json.JSONDecodeError as e:
        print(f"Error in JSON format: {str(e)}")
    except FileNotFoundError:
        print("File not found.")


validate_json("user_questions.json")
