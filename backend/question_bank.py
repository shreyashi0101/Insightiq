import json


def load_questions():
    with open(
        "backend/data/questions.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def get_question_by_id(question_id):

    questions = load_questions()

    for q in questions:
        if q["id"] == question_id:
            return q

    return None