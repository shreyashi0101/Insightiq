import json

from backend.gemini_service import model


def evaluate_with_ai(
    question,
    correct_answer,
    student_answer,
    reasoning,
    skill
):

    if str(student_answer).strip() == str(correct_answer).strip():

        return {
            "is_correct": True,
            "misconception": None,
            "learning_gap": None,
            "confidence": 1.0
        }

    try:

        prompt = f"""
You are an expert educational diagnostician.

Question:
{question}

Correct Answer:
{correct_answer}

Student Answer:
{student_answer}

Student Reasoning:
{reasoning}

Primary Skill:
{skill}

The student's answer is incorrect.

Analyze the reasoning and identify the true misconception.

Return ONLY JSON.

{{
    "is_correct": false,
    "misconception": "short label",
    "learning_gap": "short label",
    "confidence": 0.95
}}
"""

        response = model.generate_content(
            prompt
        )

        result = response.text.strip()

        if result.startswith("```json"):
            result = result.replace(
                "```json",
                ""
            )

        if result.endswith("```"):
            result = result.replace(
                "```",
                ""
            )

        result = result.strip()

        return json.loads(result)

    except Exception as e:

        print("Gemini Error:", str(e))

        return {
            "is_correct": False,
            "misconception": (
                "Unable to analyze reasoning"
            ),
            "learning_gap": skill,
            "confidence": 0.5
        }