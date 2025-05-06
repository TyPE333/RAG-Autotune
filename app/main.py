from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from app.pipeline.graph import run


class Question(BaseModel):
    """
    Pydantic model for the question input.
    """
    question: str

app = FastAPI()

@app.get("/health")
async def health():
    """
    Health check endpoint for the application.

    Returns:
        dict: A dictionary containing the status of the application.
    """
    return {"status": "ok"}

@app.post("/ask")
async def ask(question: Question):
    """
    Endpoint to ask a question and get an answer.

    Args:
        question (str): The question to be asked.

    Returns:
        dict: A dictionary containing the answer to the question.

    Raises:
        HTTPException: If the question is not provided.
    """
    if not question:
        raise HTTPException(status_code=400, detail="Question not provided")
    
    pipeline_output = run(question.question)
    print("Pipeline Output:", pipeline_output)
    output_dict = dict()

    if "answer" not in pipeline_output:
        raise HTTPException(status_code=500, detail="Error in pipeline")
    if "citations" not in pipeline_output:
        raise HTTPException(status_code=500, detail="Error in pipeline")
    
    output_dict["answer"] = pipeline_output
    output_dict["citations"] = pipeline_output["citations"]

    return output_dict

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)