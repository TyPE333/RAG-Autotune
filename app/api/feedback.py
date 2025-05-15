from fastapi import APIRouter
from scripts.utils.schema import FeedbackRequest
from app.pipeline.feedback.logger import FeedbackLogger


router = APIRouter()

@router.post("/feedback")
async def feedback_endpoint(request: FeedbackRequest):
    """
    Endpoint to handle feedback for the question-answering system.

    Args:
        request (FeedbackRequest): The feedback request containing the question, retrieved document IDs, and label.

    Returns: A dictionary containing a success message.
        
    """
    # Here you would typically process the feedback, e.g., store it in a database
    # For now, we'll just return a success message
    feedback = {
        "question": request.question,
        "retrieved_doc_ids": request.retrieved_doc_ids,
        "label": request.label
    }
    # Log the feedback
    logger = FeedbackLogger()
    logger.insert(feedback)

    return {"message": "Feedback received successfully."}
