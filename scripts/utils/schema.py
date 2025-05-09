from pydantic import BaseModel


class AskQuestion(BaseModel):
    """
    Pydantic model for the question input.
    """
    question: str