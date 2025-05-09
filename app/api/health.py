from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    """
    Health check endpoint for the application.

    Returns:
        dict: A dictionary containing the status of the application.
    """
    return {"status": "ok"}