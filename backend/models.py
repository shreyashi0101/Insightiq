from pydantic import BaseModel


class StudentAnswer(BaseModel):
    question_id: int
    student_answer: str
    reasoning: str = ""