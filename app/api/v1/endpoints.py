from fastapi import APIRouter, HTTPException
from app.schemas.rag import QuestionRequest, AnswerResponse
from app.services.rag_service import answer_question

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    try:
        answer = answer_question(
            question=request.question,
            top_k=request.top_k,
        )

        return AnswerResponse(
            question=request.question,
            answer=answer,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
