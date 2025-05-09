from fastapi import APIRouter
from scripts.utils.schema import AskQuestion
from app.pipeline.graph import run

router = APIRouter()

@router.post("/ask")
async def ask_endpoint(request: AskQuestion):
    question = request.question

    if not question:
        return {"error": "Missing 'question' in request."}

    result = run(question)
    return {
        "answer": result.get("answer", "No answer generated."),
        "citations": result.get("Docs", [])
    }
