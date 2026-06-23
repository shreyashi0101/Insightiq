from fastapi import FastAPI

from backend.question_bank import (
    load_questions,
    get_question_by_id
)

from backend.models import StudentAnswer

from backend.learning_dna import (
    update_skill,
    get_learning_dna
)

from backend.evaluator import (
    evaluate_with_ai
)

from backend.interviewer import (
    generate_probe
)

from backend.recommender import (
    get_weakest_skill
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "InsightIQ Running"
    }


@app.get("/questions")
def get_questions():
    return load_questions()


@app.get("/question/{question_id}")
def get_question(question_id: int):

    question = get_question_by_id(
        question_id
    )

    if question:
        return question

    return {
        "error": "Question not found"
    }


@app.get("/dna")
def get_dna():
    return get_learning_dna()


@app.get("/recommend")
def recommend():

    return {
        "recommended_skill":
        get_weakest_skill()
    }


@app.post("/evaluate")
def evaluate_answer(
    answer: StudentAnswer
):

    question = get_question_by_id(
        answer.question_id
    )

    if not question:

        return {
            "error": "Question not found"
        }

    is_correct = (
        str(answer.student_answer).strip()
        ==
        str(question["answer"]).strip()
    )

    if is_correct:

        dna = update_skill(
            question["skill"],
            True
        )

        return {

            "stage": "completed",

            "correct": True,

            "message":
            "Correct Answer!",

            "learning_dna":
            dna
        }

    probe = generate_probe(
        question["question"],
        answer.student_answer,
        "unknown"
    )

    return {

        "stage": "reasoning",

        "correct": False,

        "probe": probe
    }


@app.post("/diagnose")
def diagnose(
    answer: StudentAnswer
):

    question = get_question_by_id(
        answer.question_id
    )

    ai_result = evaluate_with_ai(
        question["question"],
        question["answer"],
        answer.student_answer,
        answer.reasoning,
        question["skill"]
    )

    dna = update_skill(
        question["skill"],
        False
    )

    return {

        "stage": "diagnosis",

        "question":
        question["question"],

        "student_answer":
        answer.student_answer,

        "correct_answer":
        question["answer"],

        "skill":
        question["skill"],

        "ai_analysis":
        ai_result,

        "learning_dna":
        dna,

        "next_recommended_skill":
        get_weakest_skill()
    }