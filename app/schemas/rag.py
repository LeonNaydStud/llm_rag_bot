from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=3, ge=1, le=5)


class AnswerResponse(BaseModel):
    question: str
    answer: str
