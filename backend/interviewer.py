from backend.gemini_service import model

def generate_probe(
    question,
    student_answer,
    misconception
):

    try:

        prompt = f"""
Student solved:

Question:
{question}

Answer:
{student_answer}

Detected misconception:
{misconception}

Ask ONE short Socratic follow-up question.
"""

        response = model.generate_content(
            prompt
        )

        return response.text.strip()

    except Exception:

        return (
            "Can you explain your reasoning "
            "step by step?"
        )