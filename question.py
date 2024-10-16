import json

def save_question_to_file(chat_id, user_name, user_question, user_profile_link):
    question_data = {
        "chat_id": chat_id,
        "user_name": user_name,
        "question": user_question,
        "profile_link": user_profile_link,
        "answered": False
    }
    try:
        # Read existing questions
        with open("user_questions.json", "r") as file:
            questions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        questions = []

    questions.append(question_data)

    try:
        # Write all questions back to the file
        with open("user_questions.json", "w") as file:
            json.dump(questions, file, indent=4)
        return "Ваш вопрос сохранен!"
    except Exception as e:
        return f"Произошла ошибка при сохранении вопроса: {str(e)}"

def get_unanswered_questions():
    try:
        with open("user_questions.json", "r") as file:
            questions = json.load(file)
        return [q for q in questions if not q["answered"]]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def mark_question_as_answered(chat_id, user_question):
    try:
        with open("user_questions.json", "r") as file:
            questions = json.load(file)
        for question in questions:
            if question["chat_id"] == chat_id and question["question"] == user_question:
                question["answered"] = True
        with open("user_questions.json", "w") as file:
            json.dump(questions, file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
